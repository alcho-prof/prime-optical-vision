-- RLS Policies for categories (public read)
CREATE POLICY "Anyone can view active categories" ON public.categories
  FOR SELECT USING (is_active = true);

-- RLS Policies for product_categories (public read)
CREATE POLICY "Anyone can view product categories" ON public.product_categories
  FOR SELECT USING (true);

-- RLS Policies for inventory (public read for availability)
CREATE POLICY "Anyone can view inventory" ON public.inventory
  FOR SELECT USING (true);

-- RLS Policies for cart (users can manage their own cart)
CREATE POLICY "Users can view their own cart" ON public.cart
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own cart items" ON public.cart
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own cart items" ON public.cart
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own cart items" ON public.cart
  FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for admin_users (admins only)
CREATE POLICY "Admins can view admin users" ON public.admin_users
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.admin_users au 
      WHERE au.user_id = auth.uid() AND au.is_active = true
    )
  );

-- RLS Policies for payment_transactions (users see own, admins see all)
CREATE POLICY "Users can view their own transactions" ON public.payment_transactions
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.orders o 
      WHERE o.id = payment_transactions.order_id AND o.user_id = auth.uid()
    )
  );

-- Create functions for triggers with secure search path
CREATE OR REPLACE FUNCTION update_inventory_on_order()
RETURNS TRIGGER 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  -- Reserve inventory when order is placed
  IF NEW.status = 'confirmed' AND OLD.status = 'pending' THEN
    UPDATE public.inventory 
    SET quantity_reserved = quantity_reserved + (
      SELECT COALESCE(SUM(oi.quantity), 0) 
      FROM public.order_items oi 
      WHERE oi.order_id = NEW.id
    )
    WHERE product_id IN (
      SELECT oi.product_id 
      FROM public.order_items oi 
      WHERE oi.order_id = NEW.id
    );
  END IF;
  
  -- Release reserved inventory and reduce available when shipped
  IF NEW.status = 'shipped' AND OLD.status = 'confirmed' THEN
    UPDATE public.inventory 
    SET 
      quantity_available = quantity_available - oi.quantity,
      quantity_reserved = quantity_reserved - oi.quantity
    FROM public.order_items oi
    WHERE oi.order_id = NEW.id AND inventory.product_id = oi.product_id;
  END IF;
  
  RETURN NEW;
END;
$$;

-- Create trigger for inventory management
DROP TRIGGER IF EXISTS update_inventory_trigger ON public.orders;
CREATE TRIGGER update_inventory_trigger
  AFTER UPDATE ON public.orders
  FOR EACH ROW
  EXECUTE FUNCTION update_inventory_on_order();

-- Insert default categories
INSERT INTO public.categories (name, description) VALUES
  ('Eyeglasses', 'Prescription and reading glasses'),
  ('Sunglasses', 'UV protection and fashion sunglasses'),
  ('Contact Lenses', 'Daily, weekly, and monthly contact lenses'),
  ('Frames', 'Optical frames without lenses'),
  ('Computer Glasses', 'Blue light blocking glasses'),
  ('Reading Glasses', 'Over-the-counter reading glasses')
ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_category ON public.products(category);
CREATE INDEX IF NOT EXISTS idx_products_featured ON public.products(featured);
CREATE INDEX IF NOT EXISTS idx_products_active ON public.products(is_active);
CREATE INDEX IF NOT EXISTS idx_inventory_product ON public.inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_cart_user ON public.cart(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_user ON public.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON public.orders(status);

-- Enable realtime for real-time sync
ALTER PUBLICATION supabase_realtime ADD TABLE public.products;
ALTER PUBLICATION supabase_realtime ADD TABLE public.orders;
ALTER PUBLICATION supabase_realtime ADD TABLE public.inventory;
ALTER PUBLICATION supabase_realtime ADD TABLE public.cart;