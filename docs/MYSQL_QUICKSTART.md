# Quick Start Guide - MySQL Setup

## 🚀 Quick Setup (Automated)

### Option 1: Automated Setup Script (Recommended)
```bash
# Run the automated setup script
./setup_mysql.sh
```

This script will:
- ✅ Check if MySQL is installed and running
- ✅ Create database and user
- ✅ Generate `.env` file with secure SECRET_KEY
- ✅ Test database connection

---

## 🛠️ Manual Setup

### Step 1: Install MySQL
```bash
# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt install mysql-server
sudo systemctl start mysql
```

### Step 2: Create Database
```bash
mysql -u root -p
```

```sql
CREATE DATABASE prime_optical_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'prime_optical_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Create .env File
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
DB_NAME=prime_optical_db
DB_USER=prime_optical_user
DB_PASSWORD=your_password
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations
```bash
cd backend

# For production (MySQL)
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py migrate

# For development (SQLite)
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py migrate
```

---

## 🔄 Switching Between Databases

### Development (SQLite)
```bash
cd backend
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver
```

### Production (MySQL)
```bash
cd backend
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py runserver
```

### Or use --settings flag:
```bash
python manage.py runserver --settings=config.settings.development
python manage.py runserver --settings=config.settings.production
```

---

## 📝 Common Commands

### Create Superuser
```bash
# Development
python manage.py createsuperuser --settings=config.settings.development

# Production
python manage.py createsuperuser --settings=config.settings.production
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput --settings=config.settings.production
```

### Run Tests
```bash
python manage.py test --settings=config.settings.development
```

### Database Shell
```bash
# MySQL
python manage.py dbshell --settings=config.settings.production

# SQLite
python manage.py dbshell --settings=config.settings.development
```

---

## 🔍 Verify Setup

### Test MySQL Connection
```bash
cd backend
python -c "
import os
import django
from dotenv import load_dotenv

load_dotenv('../.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT VERSION()')
    print('✅ MySQL Version:', cursor.fetchone()[0])
"
```

### Check Database Tables
```bash
python manage.py showmigrations --settings=config.settings.production
```

---

## 🆘 Troubleshooting

### "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### "Can't connect to MySQL server"
```bash
# Check if MySQL is running
brew services list  # macOS
sudo systemctl status mysql  # Linux

# Start MySQL
brew services start mysql  # macOS
sudo systemctl start mysql  # Linux
```

### "Access denied for user"
```sql
-- Re-grant privileges
mysql -u root -p
GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📚 Documentation

- **Full Migration Guide:** `docs/MYSQL_MIGRATION_GUIDE.md`
- **Production Readiness:** `docs/PRODUCTION_READINESS_REPORT.md`
- **Environment Variables:** `.env.example`

---

**Last Updated:** December 24, 2025
