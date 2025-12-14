# Prime Optical - System Architecture Architecture

**Status:** Live Development (Phase 1)  
**Architecture Style:** Modular Monolith (Django)

This document reflects the currently implemented architecture and the forward-looking plan for Prime Optical.

---

## 🏗️ 1. Architecture Overview (Modular Monolith)

We utilize a **Modular Monolith** pattern. All business logic is strictly separated into distinct Django "Apps" (`backend/apps/`), but deployed as a single unit to minimize operational complexity while maintaining clear boundaries for potential future splitting (microservices).

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Client** | Django Templates | Server-Side Rendering (SSR) for maximum SEO and performance. |
| **App Server** | Django 5.x | Handles routing, business logic, and security. |
| **Database** | SQLite (Dev) / MySQL (Prod) | Relational data integrity. |
| **Static/Media** | Local / S3 | Images handled via `Pillow` and standard Django storage. |
| **Notifications** | Console / SMTP | Email backend for lead generation logic. |

---

## 📂 2. Backend Directory Structure

| Path | Purpose |
| :--- | :--- |
| **`config/`** | Project-wide configuration (Settings, URL routing, WSGI). |
| **`apps/core/`** | Shared utilities (e.g., `TimeStampedModel`). |
| **`apps/catalog/`** | Product management (PIM), Categories, Inventory logic. |
| **`apps/inquiries/`** | Lead capture system (Forms, Email triggers). |
| **`apps/content/`** | Static marketing content (Home, About, Contact). |
| **`apps/users/`** | Authentication and Authorization (Admin-focused for Phase 1). |
| **`templates/`** | Global and App-specific HTML templates. |

---

## 🗄️ 3. App Responsibilities & Domain Model

| App | Responsibility | Key Models | Notes |
| :--- | :--- | :--- | :--- |
| **Core** | Base functionality | `models.TimeStampedModel` | Abstract base for all other models. |
| **Catalog** | Product Information Management | `Category`, `Product`, `ProductVariant` | Supports hierarchy and variants (color/size). |
| **Inquiries** | Lead Generation / Conversion | `Inquiry` | Replaces "Cart" + "Checkout" in Phase 1. |
| **Users** | User Identity | `User` (Custom Model) | Extends `AbstractUser` with phone numbers. |

---

## 📊 4. Database Schema (Implemented)

| Table | Columns | Relationships |
| :--- | :--- | :--- |
| **core_user** | `username`, `email`, `phone_number`, `is_verified` | None |
| **catalog_category** | `name`, `slug`, `image`, `is_active` | `parent` (Self-Referential FK) |
| **catalog_product** | `name`, `slug`, `price_range`, `is_active` | `category` (FK) |
| **catalog_productvariant** | `color_name`, `image`, `in_stock` | `product` (FK) |
| **inquiries_inquiry** | `customer_name`, `phone_number`, `message` | `product` (FK) |

---

## 📅 5. Development Roadmap

| Phase | Goal | Key Features | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Digital Catalog (MVP)** | • Browse Products<br>• Lead Generation (Inquiry Form)<br>• Admin Panel<br>• Console Emails | 🟢 **DONE** |
| **Phase 2** | **Basic E-Commerce** | • User Login/Signup<br>• Shopping Cart<br>• Lens Selection (Single Vision)<br>• Store Pickup / COD | ⚪ **Planned** |
| **Phase 3** | **Advanced Optical** | • Prescription Upload logic<br>• Online Payments<br>• Appointment Booking<br>• Virtual Try-On integration | ⚪ **Future** |

---

## 💻 6. Technology Stack (Current)

| Component | Choice | Justification |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Robust, standard for backend logic. |
| **Framework** | Django 5.x | "Batteries-included" (Admin, Auth, ORM, Forms). |
| **Frontend** | Django Templates + CSS | SEO-first approach. Avoids JS complexity for static content. |
| **Database** | SQLite (Dev) | Zero-config setup for rapid MVP development. |
| **Email** | Console Backend | Verifiable locally without external SMTP credentials. |
