-- Replace 'your-email@example.com' with the email you used to sign up
INSERT INTO public.admin_users (user_id, role, is_active)
SELECT id, 'super_admin', true 
FROM auth.users 
WHERE email = 'your-email@example.com';