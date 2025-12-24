# Deployment Guide: www.primeoptical.in

## Overview
This document outlines the steps to deploy the **Prime Optical Vision** project to your custom domain: `www.primeoptical.in`.

Since you are currently developing locally, you have two options:
1.  **Local Testing (Simulation):** Map the domain to your local machine (only visible to you).
2.  **Production Deployment:** Deploy the code to a cloud server (VPS/PaaS) and configure DNS.

---

## Option 1: Local Simulation (Hosts File)
If you just want to see "www.primeoptical.in" in your browser address bar while running `localhost`:

1.  **Edit Hosts File:**
    -   Open Terminal.
    -   Run: `sudo nano /etc/hosts`
    -   Add this line at the bottom:
        ```
        127.0.0.1 www.primeoptical.in
        ```
    -   Save (Ctrl+O) and Exit (Ctrl+X).

2.  **Update Django Settings:**
    -   Open `backend/config/settings/base.py`.
    -   Add the domain to `ALLOWED_HOSTS`:
        ```python
        ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.primeoptical.in']
        ```

3.  **Run Server:**
    -   `sudo python3 manage.py runserver 0.0.0.0:80` (requires sudo for port 80).
    -   Or keep running on port 8000 and visit `www.primeoptical.in:8000`.

---

## Option 2: Production Deployment (Recommended)
To make the site accessible to everyone on the internet:

### 1. Choose a Hosting Provider
-   **PaaS (Easier):** Railway, Render, Heroku, or Vercel.
-   **VPS (Full Control):** DigitalOcean, AWS EC2, or Hetzner.

### 2. Prepare the Code
-   Ensure `requirements.txt` is up-to-date (`pip freeze > requirements.txt`).
-   Create a `Procfile` (for Heroku/Render) or `gunicorn` config.
-   Set `DEBUG = False` in production settings.
-   Set `ALLOWED_HOSTS = ['www.primeoptical.in', 'primeoptical.in']`.

### 3. Deploy (Example: Railway/Render)
-   Connect your GitHub repository.
-   Add Environment Variables (`SECRET_KEY`, `DATABASE_URL`, `RAZORPAY_KEY_ID`, etc.).
-   Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
-   Start Command: `gunicorn config.wsgi:application`

### 4. Configure DNS
-   Go to your domain registrar (GoDaddy, Namecheap, etc.).
-   **A Record:** Point `@` to the Server/Load Balancer IP.
-   **CNAME Record:** Point `www` to `@` (or the specific PaaS domain, e.g., `prime-optical.onrender.com`).

---

## Next Steps for Development (Phase 3)
We are proceeding with:
1.  **Appointments:** UI is ready at `/appointments/`.
2.  **Virtual Try-On:** Implemented on Product Detail page.
