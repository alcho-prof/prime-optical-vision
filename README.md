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
| **Backend Framework** | **Django 6.0+** | Rapid development, built-in Admin, strict security patterns. |
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

## ✅ Project Roadmap & Status Checklist

### Phase 1: Digital Catalog & Brand Presence (MVP)
*Goal: Establish online presence, product discovery, and lead generation without e-commerce complexity.*

| Task ID | Feature | Description | Status |
| :---: | :--- | :--- | :---: |
| **1.1** | **System Setup** | Django scaffold, folder structure, Modular Monolith design. | ✅ Completed |
| **1.2** | **Authentication** | Custom User model, Admin panel setup, Superuser creation. | ✅ Completed |
| **1.3** | **Product Catalog** | Models for Categories, Products, Variants. | ✅ Completed |
| **1.4** | **Read-Only Views** | Product List and Detailed Product pages (SEO-friendly). | ✅ Completed |
| **1.5** | **Lead Generation** | Inquiry Form on product pages (Database + Email trigger). | ✅ Completed |
| **1.6** | **Static Content** | Home, About, Contact pages. | ✅ Completed |
| **1.7** | **Security** | CSRF protection, Inactive product masking, Secure admin. | ✅ Completed |
| **1.8** | **Basic Deployment** | Git version control, Requirements.txt, Environment configs. | ✅ Completed |

### Phase 2: Basic E-Commerce (Planned)
*Goal: Enable transactional capabilities and user accounts.*

| Task ID | Feature | Description | Status |
| :---: | :--- | :--- | :---: |
| **2.1** | **User Accounts** | Customer Registration, Login/Logout, Profile Management. | ⏳ Pending |
| **2.2** | **Shopping Cart** | Session-based cart, Add/Remove items, Update quantity. | ⏳ Pending |
| **2.3** | **Lens Selection** | Basic lens type selection (Single Vision, Zero Power) logic. | ⏳ Pending |
| **2.4** | **Checkout Flow** | Address selection, Order summary, "Cash on Delivery" support. | ⏳ Pending |
| **2.5** | **Order Management** | User order history, Admin order processing/status updates. | ⏳ Pending |
| **2.6** | **Basic Search** | Keyword search for products and categories. | ⏳ Pending |

### Phase 3: Advanced Optical Features (Future)
*Goal: Full-service optical platform with advanced prescription handling.*

| Task ID | Feature | Description | Status |
| :---: | :--- | :--- | :---: |
| **3.1** | **Prescription Logic** | Complex Rx validation (Sphere, Cylinder, Axis) & storage. | 🔮 Planned |
| **3.2** | **Payment Gateway** | Integration with Razorpay/Stripe for online payments. | 🔮 Planned |
| **3.3** | **Virtual Try-On** | AR integration to visualize frames on user photos. | 🔮 Planned |
| **3.4** | **Appointments** | Eye test booking system with doctor availability. | 🔮 Planned |
| **3.5** | **Advanced Analytics** | Sales reports, Most viewed products, User behavior tracking. | 🔮 Planned |
