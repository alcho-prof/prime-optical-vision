# 🗄️ MySQL Database Setup - Prime Optical Vision

## Overview
This project now supports **MySQL** for production deployment while maintaining **SQLite** for local development.

---

## 🚀 Quick Start

### Automated Setup (Recommended)
```bash
./setup_mysql.sh
```

This single command will:
1. ✅ Check MySQL installation
2. ✅ Create database and user
3. ✅ Generate secure `.env` file
4. ✅ Test database connection

### Manual Setup
See [MYSQL_MIGRATION_GUIDE.md](docs/MYSQL_MIGRATION_GUIDE.md) for detailed instructions.

---

## 📋 Prerequisites

- **MySQL 5.7+** or **MySQL 8.0+**
- **Python 3.8+**
- **pip** package manager

### Install MySQL

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Ubuntu/Debian:**
```bash
sudo apt install mysql-server
sudo systemctl start mysql
```

**Windows:**
Download from [MySQL Downloads](https://dev.mysql.com/downloads/mysql/)

---

## ⚙️ Configuration

### Environment Variables
Copy the example file and configure:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
# Database
DB_NAME=prime_optical_db
DB_USER=prime_optical_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=your-generated-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
```

### Generate Secret Key
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 🔄 Development vs Production

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

---

## 📦 Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Run automated script
./setup_mysql.sh

# OR manually create database
mysql -u root -p
```

```sql
CREATE DATABASE prime_optical_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'prime_optical_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Run Migrations
```bash
cd backend
python manage.py migrate --settings=config.settings.production
```

### 4. Create Superuser
```bash
python manage.py createsuperuser --settings=config.settings.production
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput --settings=config.settings.production
```

---

## 🧪 Testing

### Test MySQL Connection
```bash
cd backend
python -c "
import os, django
from dotenv import load_dotenv
load_dotenv('../.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT VERSION()')
    print('✅ Connected! MySQL Version:', cursor.fetchone()[0])
"
```

### Run Test Suite
```bash
python manage.py test --settings=config.settings.development
```

---

## 📚 Documentation

- **[MYSQL_MIGRATION_GUIDE.md](docs/MYSQL_MIGRATION_GUIDE.md)** - Complete migration guide
- **[MYSQL_QUICKSTART.md](docs/MYSQL_QUICKSTART.md)** - Quick reference
- **[MYSQL_MIGRATION_SUMMARY.md](docs/MYSQL_MIGRATION_SUMMARY.md)** - What was changed
- **[PRODUCTION_READINESS_REPORT.md](docs/PRODUCTION_READINESS_REPORT.md)** - Full production report

---

## 🔐 Security Features

### Production Settings Include:
- ✅ **SSL Redirect** - Force HTTPS
- ✅ **Secure Cookies** - Session and CSRF cookies secure
- ✅ **HSTS** - HTTP Strict Transport Security
- ✅ **XSS Protection** - Cross-site scripting prevention
- ✅ **Content Type Sniffing Protection**
- ✅ **Clickjacking Protection**

### Database Security:
- ✅ Dedicated database user
- ✅ Limited privileges
- ✅ UTF-8MB4 charset
- ✅ Environment variable credentials

---

## 🔧 Common Commands

### Database Management
```bash
# Access MySQL shell
python manage.py dbshell --settings=config.settings.production

# Show migrations
python manage.py showmigrations --settings=config.settings.production

# Create migrations
python manage.py makemigrations --settings=config.settings.production
```

### Data Migration
```bash
# Export from SQLite
python manage.py dumpdata --settings=config.settings.development \
    --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.Permission \
    --indent=2 > data_backup.json

# Import to MySQL
python manage.py loaddata data_backup.json --settings=config.settings.production
```

### Backup MySQL
```bash
mysqldump -u prime_optical_user -p prime_optical_db > backup_$(date +%Y%m%d).sql
```

### Restore MySQL
```bash
mysql -u prime_optical_user -p prime_optical_db < backup_20251224.sql
```

---

## 🆘 Troubleshooting

### "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

**macOS issues:**
```bash
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
pip install mysqlclient
```

**Ubuntu issues:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
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

### "Access denied"
```sql
mysql -u root -p
GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📊 Project Structure

```
prime-optical-vision/
├── backend/
│   ├── config/
│   │   └── settings/
│   │       ├── base.py          # Common settings
│   │       ├── development.py   # SQLite (dev)
│   │       └── production.py    # MySQL (prod)
│   ├── manage.py                # Updated with .env loading
│   └── ...
├── docs/
│   ├── MYSQL_MIGRATION_GUIDE.md
│   ├── MYSQL_QUICKSTART.md
│   └── MYSQL_MIGRATION_SUMMARY.md
├── .env                         # Your config (gitignored)
├── .env.example                 # Template
├── setup_mysql.sh              # Automated setup
└── requirements.txt            # Includes mysqlclient
```

---

## ✅ Production Deployment Checklist

Before deploying to production:

- [ ] MySQL server installed and running
- [ ] Database and user created
- [ ] `.env` file configured with production values
- [ ] New `SECRET_KEY` generated
- [ ] `DEBUG=False` in `.env`
- [ ] `mysqlclient` installed successfully
- [ ] Migrations applied to MySQL
- [ ] Superuser created
- [ ] Static files collected
- [ ] Email settings configured (SMTP)
- [ ] Razorpay live keys configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Regular backups scheduled

---

## 🎯 Next Steps

1. ✅ **Setup MySQL** - Run `./setup_mysql.sh`
2. ✅ **Configure .env** - Add email and payment credentials
3. ✅ **Run migrations** - Apply database schema
4. ✅ **Create superuser** - Admin access
5. ✅ **Test locally** - Verify everything works
6. 🚀 **Deploy to production** - See deployment guide

---

## 💡 Tips

- **Use SQLite for development** - Faster and simpler
- **Use MySQL for production** - Scalable and robust
- **Keep .env secure** - Never commit to git
- **Regular backups** - Schedule daily MySQL dumps
- **Monitor performance** - Use Django Debug Toolbar in dev
- **Use migrations** - Never modify database directly

---

## 📞 Support

For detailed help, see:
- [MYSQL_MIGRATION_GUIDE.md](docs/MYSQL_MIGRATION_GUIDE.md) - Complete guide
- [MYSQL_QUICKSTART.md](docs/MYSQL_QUICKSTART.md) - Quick commands
- [Django MySQL Notes](https://docs.djangoproject.com/en/stable/ref/databases/#mysql-notes)

---

**Last Updated:** December 24, 2025  
**Status:** ✅ Production Ready
