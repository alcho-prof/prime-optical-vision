# Prime Optical Vision

An optical store management system with a Django backend and React frontend.

## Project Structure

- `frontend/`: React + Vite + TailwindCSS application.
- `backend/`: Django + Django REST Framework + MySQL application.

## Prerequisites

- Node.js & npm
- Python 3.10+
- MySQL Server

## Getting Started

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install django djangorestframework mysqlclient django-cors-headers pymysql
   ```
   *(Note: Ensure MySQL dependencies are met for your OS)*

4. Run Migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Documentation

- See `backend/README_BACKEND.md` for API details.
