# Prime Optical Vision - Digital Catalog & Lead Gen Platform

**Version:** 1.0 (Phase 1 MVP)  
**Status:** Live Development

A scalable, modular Django-based platform for Prime Optical. This project replaces the initial frontend-only prototype with a robust backend-driven architecture.

---

## 🏗️ System Architecture (Modular Monolith)

| Module | Responsibility | Key Models/Components | Status |
| :--- | :--- | :--- | :--- |
| **config** | Project-wide settings, routing, and WSGI entry point | `urls.py`, `settings/` | ✅ Active |
| **apps.core** | Shared utilities and abstract base models | `TimeStampedModel` | ✅ Active |
| **apps.catalog** | Core product management and logic | `Category`, `Product`, `ProductVariant` | ✅ Active |
| **apps.inquiries** | Lead generation and contact management | `Inquiry`, `InquiryForm` | ✅ Active |
| **apps.users** | Authentication (Admin & Future Customer Auth) | `User` (Custom Auth Model) | ✅ Active |
| **apps.content** | Static pages (Home, About, Contact) | `home.html`, `about.html` | ✅ Active |

---

## 🛠️ Technology Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Backend Framework** | **Django 5.0+** | Rapid development, built-in Admin, strict security patterns. |
| **Language** | **Python 3.10+** | Enterprise standard, high maintainability. |
| **Database** | **SQLite (Dev) / MySQL (Prod)** | Proven relational data integrity. |
| **Frontend** | **Django Templates (SSR)** | Superior SEO for Catalog, faster initial load, simpler architecture. |
| **Styling** | **CSS3 (Grid/Flex)** | Lightweight, no build-step complexity for Phase 1. |
| **Email** | **Django SMTP Console** | Debug-friendly email notifications for dev environment. |

---

## 🚀 How to Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/alcho-prof/prime-optical-vision.git
    cd prime-optical-vision
    ```

2.  **Setup Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run Migrations:**
    ```bash
    cd backend
    python manage.py migrate
    ```

4.  **Create Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Start Server:**
    ```bash
    python manage.py runserver
    ```

*   **Public Site:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📁 Directory Structure

| Path | Description |
| :--- | :--- |
| `backend/apps/` | Contains all business logic apps (`catalog`, `inquiries`, etc). |
| `backend/config/` | Project configuration and settings split (`dev`, `prod`). |
| `backend/templates/` | Global template files (`base.html`) and app sub-folders. |
| `backend/static/` | Static assets (CSS, Images, JS). |
| `backend/media/` | User-uploaded content (Product images). |

---

## ✅ Phase 1 Deliverables Checklist

| Feature | Description | Status |
| :--- | :--- | :--- |
| **Product Catalog** | Hierarchical Categories, Products, and Variants | ✔️ Complete |
| **Read-Only Views** | Product List and Detail pages with SEO-friendly URLs | ✔️ Complete |
| **Lead Generation** | Inquiry form on Product Page (replaces Cart) | ✔️ Complete |
| **Admin Panel** | Full management for Catalog and Inquiries | ✔️ Complete |
| **Email Notifs** | System sends email to Admin upon new inquiry | ✔️ Complete |
| **Security** | Inactive products/categories are hidden; CSRF protection enabled | ✔️ Complete |
