# Client Deployment & Setup Guide - Prime Optical Vision

This guide provides step-by-step instructions for deploying the Prime Optical Vision application on a new machine. It covers two methods:
1. **Docker Deployment (Recommended)** - Easiest, handles all dependencies and database setup automatically.
2. **Manual Installation** - For environments where Docker cannot be used.

---

## Method 1: Docker Deployment (Recommended)

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 1. Extract Project Files
Unzip the provided project folder to a location on your computer (e.g., `Desktop/prime-optical-vision`).

### 2. Run the Application
1. Open your terminal (Command Prompt on Windows, Terminal on Mac).
2. Navigate to the project directory:
   ```bash
   cd path/to/prime-optical-vision
   ```
3. Start the system:
   ```bash
   docker-compose up --build
   ```
   *This process may take 5-10 minutes the first time as it downloads dependencies.*

### 3. Initialize Database (First Time Only)
Once the server is running (you'll see logs scrolling), open a **new** terminal window, navigate to the folder, and run:

1. **Apply Database Migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

2. **Create Admin User:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   *(Follow the prompts to set a username and password)*

3. **(Optional) Load Initial Data:**
   If provided, you can load fixtures here.

### 4. Access the Application
- **Website:** [http://localhost:8000](http://localhost:8000)
- **Admin Panel:** [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Method 2: Manual Installation

**Prerequisites:**
- **Python 3.10 or higher**: [Download Here](https://www.python.org/downloads/)
- **MySQL Server 8.0**: [Download Here](https://dev.mysql.com/downloads/mysql/)
- **Git** (Optional, for downloading code)

### 1. Database Setup
1. Open MySQL Workbench or your command line client.
2. Run the following SQL to create the database and user:
   ```sql
   CREATE DATABASE prime_optical_db CHARACTER SET utf8mb4;
   CREATE USER 'prime_optical_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON prime_optical_db.* TO 'prime_optical_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 2. Environment Configuration
1. Navigate to the project root folder.
2. Create a file named `.env` (no extension).
3. Paste the following configuration into it:
   ```env
   # General Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Settings
   DB_NAME=prime_optical_db
   DB_USER=prime_optical_user
   DB_PASSWORD=secure_password
   DB_HOST=localhost
   DB_PORT=3306
   
   # App Settings
   DJANGO_SETTINGS_MODULE=config.settings.development
   ```

### 3. Install Dependencies
1. Open Terminal/Command Prompt in the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Initialize Application
With the virtual environment active, run:

1. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
2. **Create Admin User:**
   ```bash
   python manage.py createsuperuser
   ```
3. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```

### 5. Start Server
```bash
python manage.py runserver
```
Access at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Troubleshooting

### "OperationalError: (2002, \"Can't connect to server...\")"
- **Docker:** Ensure the `db` service is running (`docker-compose ps`).
- **Manual:** Ensure MySQL Server is running locally and the credentials in `.env` match your MySQL setup.

### "ModuleNotFoundError: No module named 'django'"
- Ensure your virtual environment is activated (`source venv/bin/activate`).
- Ensure you ran `pip install -r requirements.txt`.

### 3D Models Not Loading (Virtual Try-On)
- Ensure the `media` folder contains the necessary `.glb` files.
- If using Docker, ensure the `media` volume is mounted correctly.
