# Codebase Structure & Function Reference

**Project:** Prime Optical Vision  
**Backend:** Django Modular Monolith

This document details the folder structure and key components within the codebase as of Phase 2 Task 2.1.

---

### 📂 Directory: `backend/config/` (Project Configuration)

| File | Type | Key Components | Description |
| :--- | :--- | :--- | :--- |
| `settings/base.py` | Config | `INSTALLED_APPS`, `AUTH_USER_MODEL`, `LOGIN_REDIRECT_URL` | Global project configurations. |
| `settings/dev.py` | Config | `DEBUG=True`, `EMAIL_BACKEND=console` | Development-specific overrides. |
| `urls.py` | Routing | `urlpatterns` | Main URL entry point, includes app urls. |
| `wsgi.py` | Entry | `application` | WSGI application callable for servers. |

---

### 📂 Directory: `backend/apps/core/` (Core Utilities)

| File | Type | Key Functions/Classes | Description |
| :--- | :--- | :--- | :--- |
| `models.py` | Model | `TimeStampedModel(models.Model)` | Abstract base model providing `created_at` and `updated_at`. |

---

### 📂 Directory: `backend/apps/users/` (User Model)

| File | Type | Key Functions/Classes | Description |
| :--- | :--- | :--- | :--- |
| `models.py` | Model | `User(AbstractUser)` | Custom user model with `phone_number`, `is_verified`, `can_login_no_password`. |
| `admin.py` | Admin | `CustomUserAdmin` | customized Admin with filters and custom fieldsets. |
| `forms.py` | Form | `CustomUserCreationForm` | Admin-side form handling optional passwords and validation. |

---

### 📂 Directory: `backend/apps/accounts/` (Auth & Profile)

| File | Type | Key Functions/Classes | Description |
| :--- | :--- | :--- | :--- |
| `urls.py` | Routing | `/login/`, `/register/`, `/profile/` | Routes for authentication views. |
| `views.py` | View | `register_view(request)` | Handles user signup and auto-login. |
|  | View | `profile_view(request)` | Handles updating user details (Phone, Name). |
| `forms.py` | Form | `UserRegistrationForm` | Frontend registration form (splits full name). |
|  | Form | `UserProfileForm` | Frontend profile update form. |
|  | Form | `CustomAuthenticationForm` | Login form with optional password field. |
| `backends.py` | Logic | `PasswordlessAuthBackend` | Custom backend to allow login without password if flag is set. |

---

### 📂 Directory: `backend/apps/catalog/` (Product Catalog)

| File | Type | Key Functions/Classes | Description |
| :--- | :--- | :--- | :--- |
| `models.py` | Model | `Category` | Recursive category tree. |
|  | Model | `Product` | Main product data (Price, Desc). |
|  | Model | `ProductVariant` | Color/SKU variations of a product. |
| `views.py` | View | `product_list(request)` | Lists active products. |
|  | View | `product_detail(request, slug)` | Shows product details + Inquiry form. Handles 404 for inactive items. |

---

### 📂 Directory: `backend/apps/inquiries/` (Lead Gen)

| File | Type | Key Functions/Classes | Description |
| :--- | :--- | :--- | :--- |
| `models.py` | Model | `Inquiry` | Stores customer messages linked to a Product. |
| `forms.py` | Form | `InquiryForm` | Simple name/phone/message form. |
| `admin.py` | Admin | `InquiryAdmin` | Read-only admin interface for viewing leads. |

---

### 📂 Directory: `backend/templates/` (Frontend)

| Path | Type | Key Components | Description |
| :--- | :--- | :--- | :--- |
| `base.html` | Layout | Navbar, `{% block content %}` | Main site shell. Includes Auth checks in Navbar. |
| `pages/home.html` | Page | Welcome, Feature Links | Landing page. |
| `accounts/` | Auth | `login.html`, `register.html`, `profile.html` | Auth UI forms. |
| `catalog/` | Catalog | `product_list.html`, `product_detail.html` | Product grid and detail views. |
