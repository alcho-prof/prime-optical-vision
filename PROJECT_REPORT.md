# Project Activity Report

This document records all user requests, system actions, file modifications, and specific code changes executed during the session.

---

## 1. Request: Delete Frontend
**User Command:** "delete the frondend folder with all the files"  
**Date:** 2025-12-14

### Actions Taken
*   Executed shell command to remove the directory.

### Files Changed
*   **Deleted Directory:** `frontend/` (and all contained files).

---

## 2. Request: Delete Backend
**User Command:** "delete the backend folder"  
**Date:** 2025-12-14

### Actions Taken
*   Executed shell command to remove the directory.

### Files Changed
*   **Deleted Directory:** `backend/` (and all contained files).

---

## 3. Request: Architecture Planning
**User Command:** "Design and plan a basic yet scalable optical business website..."  
**Date:** 2025-12-14

### Actions Taken
*   Analyzed requirements for "Prime Optical Website".
*   Drafted architectural blueprint focusing on Modular Monolith Django structure.

### Files Changed
*   **Created File:** `ARCHITECTURE_PLAN.md`
    *   *Content:* Added detailed Role analysis, System Architecture (Django + MySQL), Database Schema design, and Development Phases.

---

## 4. Request: Project Scaffolding
**User Command:** "use django template for client layer ... use this as root folder structure"  
**Date:** 2025-12-14

### Actions Taken
*   Installed Django via `pip`.
*   Created `scaffold.py` script to generate the requested folder structure automatically.
*   Refactored standard Django `startproject` structure to match the "Modular" design (separating `apps`, `config`, `settings`).

### Files Changed
*   **Created Directory:** `backend/`
*   **Modified File:** `backend/config/settings/base.py`
    *   *Change:* Updated `BASE_DIR` to point to the correct root.
    *   *Change:* Added `sys.path.insert(0, ...)` to include the new `apps/` directory.
    *   *Change:* Added local apps (`apps.core`, `apps.users`, `apps.catalog`, etc.) to `INSTALLED_APPS`.
    *   *Change:* Configured `TEMPLATES['DIRS']` to `[BASE_DIR / 'templates']`.
    *   *Change:* Defined `STATICFILES_DIRS` and `MEDIA_ROOT`.
*   **Modified File:** `backend/manage.py`
    *   *Change:* Changed default settings module to `'config.settings.dev'`.
*   **Modified File:** `backend/config/wsgi.py` & `backend/config/asgi.py`
    *   *Change:* Changed default settings module to `'config.settings.dev'`.
*   **Database:** Initialized `db.sqlite3` via migrations.

---

## 5. Request: Admin & User Authentication
**User Command:** "create the backend for admin and users providing login"  
**Date:** 2025-12-14

### Actions Taken
*   Implemented Custom User Model to support future extensions (phone number, etc.).
*   Reset database to apply the custom auth model.
*   Created Superuser (`admin`).
*   Created Login templates.

### Files Changed
*   **Created File:** `backend/apps/users/models.py`
    *   *Content:* Defined `class User(AbstractUser)` with `phone_number` and `is_verified` fields.
*   **Created File:** `backend/apps/users/admin.py`
    *   *Content:* Registered `User` model using `UserAdmin` to make it visible in the Admin Panel.
*   **Modified File:** `backend/config/settings/base.py`
    *   *Change:* Added `AUTH_USER_MODEL = 'users.User'`.
    *   *Change:* Added `LOGIN_REDIRECT_URL = 'home'` and `LOGOUT_REDIRECT_URL = 'home'`.
*   **Modified File:** `backend/config/urls.py`
    *   *Change:* Added `path('accounts/', include('django.contrib.auth.urls'))`.
    *   *Change:* Added root path `path('', ...)` serving the home template.
*   **Created File:** `backend/templates/registration/login.html`
    *   *Content:* created a standard login form.
*   **Created File:** `backend/templates/pages/home.html`
    *   *Content:* Added conditional logic to show "Login" or "Logout / Admin" links based on user state.

---

## 6. Request: Phase 1 Architecture Planning
**User Command:** "Build a stable, production-ready digital catalog platform... PHASE 1 – Digital Catalog & Brand Presence (MVP)"  
**Date:** 2025-12-14

### Actions Taken
*   Defined strictly scoped Phase 1 requirements (No Auth, No Cart, No Payments).
*   Chose **Django Templates** over React for SEO and simplicity in Phase 1.
*   Designed data models for Catalog (Category, Product, Variant) and Inquiries.
*   Outlined App responsibilities (`core`, `catalog`, `content`, `lenses`, `inquiries`).

### Files Changed
*   **Created File:** `PHASE_1_ARCHITECTURE.md`
    *   *Content:* Detailed blueprint for the MVP phase, covering Architecture, Folder Structure, Data Models, and Workflows.

---

## 7. Request: Implement Core & Catalog Models
**User Command:** "Implement Core + Catalog Models... 1️⃣ core/models.py ... 2️⃣ catalog/models.py"  
**Date:** 2025-12-14

### Actions Taken
*   Implemented `TimeStampedModel` in `core` app.
*   Implemented `Category`, `Product`, and `ProductVariant` in `catalog` app.
*   Installed `Pillow` library for image handling.
*   Applied migrations.
*   Registered models in `catalog/admin.py` with inline variants.

### Files Changed
*   **Created File:** `backend/apps/core/models.py`
    *   *Content:* Abstract `TimeStampedModel` with `created_at` and `updated_at`.
*   **Created File:** `backend/apps/catalog/models.py`
    *   *Content:* 
        *   `Category`: Hierarchical with self-referencing ForeignKey.
        *   `Product`: Linked to Category, includes `price_range` (textual).
        *   `ProductVariant`: Linked to Product, includes color, image, and `in_stock` flag.
*   **Created File:** `backend/apps/catalog/admin.py`
    *   *Content:* `ProductAdmin` with filter, search, and `ProductVariantInline`.
*   **Modified File:** `backend/apps/catalog/migrations/0001_initial.py` (Generated)
*   **System:** Installed `Pillow`.

---

## 8. Request: Fix Server Port Conflict
**User Command:** "check the terminal and run" (Response to port already in use error)  
**Date:** 2025-12-14

### Actions Taken
*   Detected port 8000 was occupied by a detached process.
*   Killed the specific process using `lsof` and `kill`.
*   Restarted the Django development server successfully.
