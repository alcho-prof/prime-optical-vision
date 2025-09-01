-- Enhanced products table with optical-specific fields
ALTER TABLE public.products ADD COLUMN IF NOT EXISTS 
  frame_type TEXT,
  lens_type TEXT,
  frame_material TEXT,
  frame_color TEXT,
  lens_power TEXT,
  uv_protection BOOLEAN DEFAULT false,
  anti_glare BOOLEAN DEFAULT false,
  scratch_resistant BOOLEAN DEFAULT false,
  featured BOOLEAN DEFAULT false,
  discount_percentage INTEGER DEFAULT 0,
  original_price NUMERIC,
  sku TEXT UNIQUE;

-- Create categories table
CREATE TABLE IF NOT EXISTS public.categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create product_categories junction table
CREATE TABLE IF NOT EXISTS public.product_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES public.products(id) ON DELETE CASCADE,
  category_id UUID REFERENCES public.categories(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(product_id, category_id)
);

-- Create inventory tracking table
CREATE TABLE IF NOT EXISTS public.inventory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES public.products(id) ON DELETE CASCADE,
  quantity_available INTEGER NOT NULL DEFAULT 0,
  quantity_reserved INTEGER NOT NULL DEFAULT 0,
  low_stock_threshold INTEGER DEFAULT 5,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Enhanced orders table
ALTER TABLE public.orders ADD COLUMN IF NOT EXISTS 
  customer_email TEXT,
  customer_phone TEXT,
  order_notes TEXT,
  tracking_number TEXT,
  estimated_delivery TIMESTAMPTZ,
  actual_delivery TIMESTAMPTZ;

-- Create cart table for persistent shopping carts
CREATE TABLE IF NOT EXISTS public.cart (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  product_id UUID REFERENCES public.products(id) ON DELETE CASCADE,
  quantity INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(user_id, product_id)
);

-- Create admin_users table for admin authentication
CREATE TABLE IF NOT EXISTS public.admin_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL DEFAULT 'admin' CHECK (role IN ('admin', 'super_admin', 'manager')),
  permissions JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(user_id)
);

-- Create payment_transactions table
CREATE TABLE IF NOT EXISTS public.payment_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES public.orders(id) ON DELETE CASCADE,
  payment_method TEXT NOT NULL,
  payment_status TEXT NOT NULL DEFAULT 'pending',
  transaction_id TEXT,
  amount NUMERIC NOT NULL,
  currency TEXT DEFAULT 'INR',
  payment_gateway TEXT,
  gateway_response JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Enable RLS on all new tables
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.product_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.inventory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cart ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment_transactions ENABLE ROW LEVEL SECURITY;

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

-- Create functions for triggers
CREATE OR REPLACE FUNCTION update_inventory_on_order()
RETURNS TRIGGER AS $$
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
$$ LANGUAGE plpgsql;

-- Create trigger for inventory management
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