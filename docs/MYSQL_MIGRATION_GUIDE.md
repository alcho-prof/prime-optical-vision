# MySQL Database Migration Guide

## Overview
This guide walks you through migrating from SQLite to MySQL for production deployment.

---

## Prerequisites

### 1. Install MySQL Server
**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**Windows:**
Download and install from: https://dev.mysql.com/downloads/mysql/

---

## Step 1: Install MySQL Client Library

```bash
# Install mysqlclient (already added to requirements.txt)
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient`, you may need:

**macOS:**
```bash
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
pip install mysqlclient
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

---

## Step 2: Create MySQL Database and User

```bash
# Login to MySQL as root
mysql -u root -p

# Or if no password is set:
mysql -u root
```

**Run these SQL commands:**
```sql
-- Create database
CREATE DATABASE prime_optical_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'prime_optical_user'@'localhost' IDENTIFIED BY 'your_strong_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'prime_optical_user';

-- Exit
EXIT;
```

---

## Step 3: Configure Environment Variables

### Create `.env` file in project root:
```bash
cp .env.example .env
```

### Edit `.env` with your actual values:
```env
# Django Settings
SECRET_KEY=your-actual-secret-key-generate-new-one
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# Database Configuration
DB_NAME=prime_optical_db
DB_USER=prime_optical_user
DB_PASSWORD=your_strong_password_here
DB_HOST=localhost
DB_PORT=3306

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@primeoptical.in

# Razorpay
RAZORPAY_KEY_ID=rzp_live_YourLiveKeyId
RAZORPAY_KEY_SECRET=YourLiveKeySecret
```

**Generate a new SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Step 4: Update Django Settings

The settings are now split into:
- `config/settings/base.py` - Common settings
- `config/settings/development.py` - SQLite for local dev
- `config/settings/production.py` - MySQL for production

### For Development (SQLite):
```bash
export DJANGO_SETTINGS_MODULE=config.settings.development
# or
python manage.py runserver --settings=config.settings.development
```

### For Production (MySQL):
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
# or
python manage.py runserver --settings=config.settings.production
```

---

## Step 5: Load Environment Variables

### Update `manage.py` to load .env:
The file should already have `python-dotenv` configured. Verify it contains:

```python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)
```

---

## Step 6: Run Migrations

### Using Production Settings (MySQL):
```bash
cd backend

# Set environment
export DJANGO_SETTINGS_MODULE=config.settings.production

# Create migrations
python manage.py makemigrations

# Apply migrations to MySQL
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

## Step 7: Data Migration (Optional)

### If you have existing SQLite data to migrate:

**Option 1: Using Django's dumpdata/loaddata**
```bash
# 1. Export data from SQLite
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.Permission \
    --indent=2 > data_backup.json

# 2. Load data into MySQL
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py loaddata data_backup.json
```

**Option 2: Manual migration for specific apps**
```bash
# Export specific apps
python manage.py dumpdata catalog orders users --indent=2 > app_data.json

# Load into MySQL
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py loaddata app_data.json
```

---

## Step 8: Test MySQL Connection

### Create a test script `test_mysql.py`:
```python
import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL Connection Successful!")
        print(f"MySQL Version: {version[0]}")
except Exception as e:
    print(f"❌ MySQL Connection Failed: {e}")
```

**Run:**
```bash
cd backend
python test_mysql.py
```

---

## Step 9: Verify Everything Works

```bash
cd backend
export DJANGO_SETTINGS_MODULE=config.settings.production

# Run server
python manage.py runserver

# Run tests
python manage.py test

# Check database tables
python manage.py dbshell
```

**In MySQL shell:**
```sql
SHOW TABLES;
SELECT COUNT(*) FROM auth_user;
EXIT;
```

---

## Step 10: Create Logs Directory

```bash
mkdir -p backend/logs
touch backend/logs/django_errors.log
```

---

## Production Deployment Checklist

- [ ] MySQL server installed and running
- [ ] Database and user created
- [ ] `.env` file configured with production values
- [ ] New SECRET_KEY generated
- [ ] `mysqlclient` installed successfully
- [ ] Migrations applied to MySQL
- [ ] Superuser created
- [ ] Static files collected
- [ ] Data migrated (if applicable)
- [ ] MySQL connection tested
- [ ] Logs directory created
- [ ] `.env` added to `.gitignore`
- [ ] Email settings configured
- [ ] Razorpay live keys configured

---

## Troubleshooting

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### Error: "Can't connect to MySQL server"
```bash
# Check MySQL is running
brew services list  # macOS
sudo systemctl status mysql  # Linux

# Verify credentials
mysql -u prime_optical_user -p prime_optical_db
```

### Error: "Access denied for user"
```sql
-- Re-grant privileges
GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Unknown database"
```sql
-- Recreate database
CREATE DATABASE prime_optical_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## Switching Between Development and Production

### Development (SQLite):
```bash
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver
```

### Production (MySQL):
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py runserver
```

### Or use --settings flag:
```bash
python manage.py runserver --settings=config.settings.development
python manage.py runserver --settings=config.settings.production
```

---

## Security Notes

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use strong passwords** for database users
3. **Generate new SECRET_KEY** for production
4. **Use environment variables** for all sensitive data
5. **Enable SSL** for MySQL connections in production
6. **Regular backups** of MySQL database

---

## Backup MySQL Database

### Manual Backup:
```bash
mysqldump -u prime_optical_user -p prime_optical_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore from Backup:
```bash
mysql -u prime_optical_user -p prime_optical_db < backup_20251224_120000.sql
```

### Automated Backup Script:
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u prime_optical_user -p prime_optical_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
```

---

**Last Updated:** December 24, 2025  
**Version:** 1.0  
**Status:** ✅ Ready for Implementation
