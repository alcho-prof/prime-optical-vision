-- Prime Optical Vision - Database Setup Script
-- Run this script in DBeaver to create the database and user

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS prime_optical_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Step 2: Create the database user
CREATE USER IF NOT EXISTS 'prime_optical_user'@'localhost' 
    IDENTIFIED BY 'prime_optical_2024';

-- Step 3: Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON prime_optical_db.* 
    TO 'prime_optical_user'@'localhost';

-- Step 4: Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Step 5: Verify the database was created
SHOW DATABASES LIKE 'prime_optical_db';

-- Step 6: Verify the user was created
SELECT User, Host FROM mysql.user WHERE User = 'prime_optical_user';

-- Step 7: Show granted privileges
SHOW GRANTS FOR 'prime_optical_user'@'localhost';
