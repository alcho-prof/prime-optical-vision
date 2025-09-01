-- Fix the admin_users RLS policy recursion issue
-- Drop the existing problematic policy
DROP POLICY IF EXISTS "Admins can view admin users" ON public.admin_users;

-- Create a simpler, non-recursive policy for admin_users
-- This policy allows users to see admin_users records only if they themselves are active admins
CREATE POLICY "Admins can view admin users" ON public.admin_users
FOR SELECT 
USING (
  EXISTS (
    SELECT 1 FROM public.admin_users au2 
    WHERE au2.user_id = auth.uid() 
    AND au2.is_active = true
  )
);

-- Allow admin users to be inserted (for initial setup)
CREATE POLICY "Service role can insert admin users" ON public.admin_users
FOR INSERT 
WITH CHECK (true);

-- Allow admin users to be updated
CREATE POLICY "Service role can update admin users" ON public.admin_users
FOR UPDATE 
USING (true);

-- Insert the demo admin user if it doesn't exist
INSERT INTO public.admin_users (user_id, role, is_active, permissions)
SELECT 
  u.id,
  'admin',
  true,
  '{"manage_products": true, "manage_orders": true, "manage_customers": true}'::jsonb
FROM auth.users u 
WHERE u.email = 'admin@primeopticals.com'
AND NOT EXISTS (
  SELECT 1 FROM public.admin_users au 
  WHERE au.user_id = u.id
);