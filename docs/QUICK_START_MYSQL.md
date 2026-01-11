# Quick Start: MySQL Integration & Superuser Guide

This guide focuses specifically on connecting the application to a local MySQL database and creating an Admin (Superuser) account via the terminal.

## Prerequisites (macOS)
Before starting, ensure you have MySQL installed. If not:
```bash
brew install mysql pkg-config mysql-client
brew services start mysql
```

---

## Step 1: Create Database & User (SQL)
You need to create the empty database first.
1.  Open your terminal.
2.  Login to MySQL:
    ```bash
    mysql -u root
    ```
3.  Run these commands (copy-paste them one by one):
    ```sql
    -- 1. Create the Database
    CREATE DATABASE prime_optical_db CHARACTER SET utf8mb4;

    -- 2. Create the User (Change 'secure_password' to something you like)
    CREATE USER 'prime_optical_user'@'localhost' IDENTIFIED BY 'secure_password';

    -- 3. Grant Permissions
    GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';

    -- 4. Save Changes
    FLUSH PRIVILEGES;
    EXIT;
    ```

---

## Step 2: Connect Django to MySQL
1.  Go to the project root directory (where `manage.py` is).
2.  Open (or create) the `.env` file.
3.  Ensure these lines match the user you just created:
    ```ini
    DB_NAME=prime_optical_db
    DB_USER=prime_optical_user
    DB_PASSWORD=secure_password
    DB_HOST=localhost
    DB_PORT=3306
    ```

---

## Step 3: Initialize the Database
Now we need to create the tables in MySQL. Run these commands in your project terminal (with your virtual environment active):

1.  **Make Migrations** (Prepare the files):
    ```bash
    python manage.py makemigrations
    ```
2.  **Migrate** (Create tables in MySQL):
    ```bash
    python manage.py migrate
    ```

---

## Step 4: Create Superuser (Admin)
This enables you to log in to the Admin Panel.

1.  Run the command:
    ```bash
    python manage.py createsuperuser
    ```
2.  Follow the prompts:
    *   **Username:** (e.g., `admin`)
    *   **Email:** (e.g., `admin@example.com`)
    *   **Password:** (Type your password - it will remain invisible while typing)
    *   **Password (again):** (Type it again)
3.  If successful, it will say `Superuser created successfully.`

---

## Step 5: Run & Verify
1.  Start the server:
    ```bash
    python manage.py runserver
    ```
2.  Go to: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
3.  Log in with the **Superuser** credentials you just created.
