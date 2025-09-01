-- First, let's create a default admin user directly in the auth.users table
-- This bypasses the email confirmation requirement

-- Insert admin user into auth.users table
INSERT INTO auth.users (
  instance_id,
  id,
  aud,
  role,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at,
  raw_app_meta_data,
  raw_user_meta_data,
  is_super_admin,
  confirmation_token,
  email_change_token_new,
  recovery_token
) VALUES (
  '00000000-0000-0000-0000-000000000000',
  gen_random_uuid(),
  'authenticated',
  'authenticated',
  'admin@primeopticals.com',
  crypt('admin123', gen_salt('bf')),
  now(),
  now(),
  now(),
  '{"provider": "email", "providers": ["email"]}',
  '{"full_name": "Prime Opticals Admin"}',
  false,
  '',
  '',
  ''
);

-- Create corresponding profile for the admin user
INSERT INTO public.profiles (user_id, email, full_name, role)
SELECT id, email, 'Prime Opticals Admin', 'admin'
FROM auth.users 
WHERE email = 'admin@primeopticals.com';

-- Make this user an admin in admin_users table
INSERT INTO public.admin_users (user_id, role, is_active)
SELECT id, 'super_admin', true 
FROM auth.users 
WHERE email = 'admin@primeopticals.com';

-- Insert some sample product data for testing
INSERT INTO public.products (
  name, 
  description, 
  price, 
  original_price,
  category, 
  brand, 
  image_url, 
  stock_quantity,
  frame_type,
  lens_type,
  frame_material,
  frame_color,
  uv_protection,
  anti_glare,
  scratch_resistant,
  featured,
  discount_percentage,
  sku,
  is_active
) VALUES 
(
  'Classic Black Frame Glasses',
  'Premium black acetate frame with anti-glare lenses perfect for daily use',
  2999,
  3999,
  'Eyeglasses',
  'Prime Vision',
  'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=400',
  25,
  'full-rim',
  'single-vision',
  'Acetate',
  'Black',
  true,
  true,
  true,
  true,
  25,
  'PV-BF-001',
  true
),
(
  'Aviator Sunglasses Gold',
  'Classic aviator style sunglasses with UV protection and polarized lenses',
  3499,
  4499,
  'Sunglasses',
  'Prime Sun',
  'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400',
  15,
  'rimless',
  'single-vision',
  'Metal',
  'Gold',
  true,
  false,
  true,
  true,
  22,
  'PS-AV-002',
  true
),
(
  'Blue Light Computer Glasses',
  'Protect your eyes from digital strain with our blue light blocking technology',
  1999,
  2499,
  'Computer Glasses',
  'Prime Tech',
  'https://images.unsplash.com/photo-1556306535-0f09a537f0a3?w=400',
  30,
  'full-rim',
  'computer',
  'TR90',
  'Blue',
  false,
  true,
  true,
  false,
  20,
  'PT-BL-003',
  true
),
(
  'Reading Glasses +2.00',
  'Comfortable reading glasses with +2.00 magnification',
  1299,
  1599,
  'Reading Glasses',
  'Prime Read',
  'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400',
  20,
  'half-rim',
  'single-vision',
  'Metal',
  'Silver',
  false,
  false,
  true,
  false,
  19,
  'PR-RD-004',
  true
),
(
  'Progressive Multifocal Glasses',
  'Advanced progressive lenses for seamless vision at all distances',
  5999,
  7999,
  'Eyeglasses',
  'Prime Vision',
  'https://images.unsplash.com/photo-1584199506938-9bb9d7b2ad7b?w=400',
  10,
  'full-rim',
  'progressive',
  'Titanium',
  'Brown',
  true,
  true,
  true,
  true,
  25,
  'PV-PG-005',
  true
);

-- Create inventory entries for all products
INSERT INTO public.inventory (product_id, quantity_available, quantity_reserved, low_stock_threshold)
SELECT id, stock_quantity, 0, 5
FROM public.products;

-- Link products to categories
INSERT INTO public.product_categories (product_id, category_id)
SELECT p.id, c.id
FROM public.products p
JOIN public.categories c ON p.category = c.name;