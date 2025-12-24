#!/bin/bash

# MySQL Setup Script for Prime Optical Vision
# This script helps set up MySQL database for production

set -e  # Exit on error

echo "🚀 Prime Optical Vision - MySQL Setup Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if MySQL is installed
echo "📋 Checking MySQL installation..."
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}❌ MySQL is not installed${NC}"
    echo ""
    echo "Please install MySQL first:"
    echo "  macOS:   brew install mysql"
    echo "  Ubuntu:  sudo apt install mysql-server"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ MySQL is installed${NC}"
fi

# Check if MySQL is running
echo "📋 Checking if MySQL is running..."
if ! pgrep -x mysqld > /dev/null; then
    echo -e "${YELLOW}⚠️  MySQL is not running${NC}"
    echo "Starting MySQL..."
    
    # Try to start MySQL based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start mysql
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo systemctl start mysql
    fi
    
    sleep 3
    
    if pgrep -x mysqld > /dev/null; then
        echo -e "${GREEN}✅ MySQL started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start MySQL${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ MySQL is running${NC}"
fi

echo ""
echo "📝 Database Configuration"
echo "========================="
read -p "Enter database name [prime_optical_db]: " DB_NAME
DB_NAME=${DB_NAME:-prime_optical_db}

read -p "Enter database user [prime_optical_user]: " DB_USER
DB_USER=${DB_USER:-prime_optical_user}

read -sp "Enter database password: " DB_PASSWORD
echo ""

if [ -z "$DB_PASSWORD" ]; then
    echo -e "${RED}❌ Password cannot be empty${NC}"
    exit 1
fi

read -p "Enter MySQL root password (leave empty if no password): " -s MYSQL_ROOT_PASSWORD
echo ""

echo ""
echo "🔧 Creating database and user..."

# Create SQL commands
SQL_COMMANDS="
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
"

# Execute SQL commands
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    echo "$SQL_COMMANDS" | mysql -u root
else
    echo "$SQL_COMMANDS" | mysql -u root -p"$MYSQL_ROOT_PASSWORD"
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database and user created successfully${NC}"
else
    echo -e "${RED}❌ Failed to create database and user${NC}"
    exit 1
fi

echo ""
echo "📄 Creating .env file..."

# Check if .env already exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    read -p "Do you want to overwrite it? (y/N): " OVERWRITE
    if [[ ! $OVERWRITE =~ ^[Yy]$ ]]; then
        echo "Skipping .env creation"
        exit 0
    fi
fi

# Generate SECRET_KEY
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Create .env file
cat > .env << EOF
# Django Settings
SECRET_KEY=${SECRET_KEY}
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# Database Configuration (MySQL)
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (Update with your SMTP settings)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@primeoptical.in

# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_live_YourLiveKeyId
RAZORPAY_KEY_SECRET=YourLiveKeySecret
EOF

echo -e "${GREEN}✅ .env file created${NC}"

echo ""
echo "🔍 Testing database connection..."

# Test connection
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "USE ${DB_NAME}; SELECT 'Connection successful!' AS status;" 2>/dev/null
else
    mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "USE ${DB_NAME}; SELECT 'Connection successful!' AS status;" 2>/dev/null
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database connection successful${NC}"
else
    echo -e "${RED}❌ Database connection failed${NC}"
    exit 1
fi

echo ""
echo "✅ MySQL Setup Complete!"
echo "======================="
echo ""
echo "Next steps:"
echo "1. Update .env file with your email and Razorpay credentials"
echo "2. Install Python dependencies: pip install -r requirements.txt"
echo "3. Run migrations: cd backend && python manage.py migrate --settings=config.settings.production"
echo "4. Create superuser: python manage.py createsuperuser --settings=config.settings.production"
echo "5. Collect static files: python manage.py collectstatic --settings=config.settings.production"
echo ""
echo "Database Details:"
echo "  Name: ${DB_NAME}"
echo "  User: ${DB_USER}"
echo "  Host: localhost"
echo "  Port: 3306"
echo ""
