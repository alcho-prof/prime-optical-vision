# Prime Optical Website - Architectural Blueprint

**Project Name:** Prime Optical Website  
**Role:** Senior Software Architect  
**Date:** 2025-12-14  

---

## 1. Requirement Analysis & Risk Assessment

### Analysis
The goal is to build a foundational e-commerce platform for an optical business. The focus is on brand presence, product browsing, and basic transaction capabilities without the complexity of AR/AI features initially.

### Gaps & Risks Identified
1.  **Lens Prescription Complexity:** "Buying" eyewear is not standard e-commerce. It requires handling prescription data (Sphere, Cylinder, Axis, PD). 
    *   *Risk:* Simulating this too simply (just a text box) leads to errors. Building a full validator is complex.
    *   *Mitigation (Phase 1):* Allow users to upload a photo of their prescription or request a callback.
2.  **Payment Processing:** "Buy action" implies payments.
    *   *Risk:* Security and compliance (PCI-DSS).
    *   *Mitigation (Phase 1):* Cash on Delivery (COD) or Pay at Store. Phase 2 can integrate Stripe/Razorpay.
3.  **Inventory Sync:** No mention of stock management.
    *   *Risk:* Selling out-of-stock items.
    *   *Mitigation:* Simple boolean "In Stock" flag for Phase 1.

---

## 2. System Architecture

We will adopt a **Modular Monolith** approach using Django. This balances speed of development with future scalability. If the frontend becomes highly interactive later (AR features), we can decouple it easily.

### High-Level Components
1.  **Client Layer (Frontend):** 
    *   Responsive Web App (HTML5/CSS3/ES6+).
    *   Framework: React.js (via Vite) or Django Templates (HTMX for interactivity). *Recommendation: React for future AR integration.*
2.  **API Layer (Backend):**
    *   Django REST Framework (DRF) code-first APIs.
3.  **Data Layer:**
    *   MySQL Database.
    *   Media Storage (AWS S3 or Local handling for initial phase).

### Data Flow
`User` -> `CDN/Frontend` -> `API Gateway (Nginx)` -> `Django App` -> `MySQL`

---

## 3. Backend Structure (Django)

Proposed strict modular separation to ensure scalability:

```text
backend/
├── config/             # Project settings (Env specific)
├── apps/
│   ├── core/           # Shared utilities, base models
│   ├── users/          # Auth, Profile, Address management
│   ├── catalog/        # Categories, Products, Variants, Inventory
│   ├── lenses/         # specialized module for Lens types and Coatings
│   ├── cart/           # Basket logic, session handling
│   ├── orders/         # Order processing, Invoices
│   └── content/        # Banners, Pages (About/Contact), FAQs
└── manage.py
```

---

## 4. Database Schema Design (Entity-Relationship)

### Core Tables

**1. Catalog & Products**
*   `Category`: id, name, slug, parent_id (self-ref for hierarchy)
*   `Product`: id, name, category_fk, base_price, description, is_active
*   `ProductVariant`: id, product_fk, color, size, sku, stock_qty, image_url

**2. Specialized Optical Data**
*   `LensType`: id, name (e.g., Bifocal), description, price_modifier
*   `LensCoating`: id, name (e.g., Blue-cut), price_modifier
*   `Prescription` (Optional Phase 1): id, user_fk, image_upload, sphere_od, sphere_os...

**3. Sales & Users**
*   `AppUser`: id, email, phone, is_verified
*   `Cart`: id, user_fk, session_key
*   `CartItem`: id, cart_fk, variant_fk, lens_type_fk, quantity
*   `Order`: id, user_fk, total_amount, status (Pending, Processing, Completed), payment_method

---

## 5. Development Phases

### Phase 1: Digital Catalog & Branding (MVP)
*   **Goal:** Digital presence, product discovery, store direction.
*   **Features:**
    *   Home, About, Contact Pages.
    *   Product Listing with Filters (Gender, Category).
    *   Product Detail Page (Images, Description).
    *   "Inquiry" button (Sends WhatsApp/Email to admin).
    *   Admin Panel for managing catalog.

### Phase 2: Basic E-Commerce
*   **Goal:** Transaction capability.
*   **Features:**
    *   User Accounts (Login/Signup).
    *   Shopping Cart.
    *   Basic Lens selection (Single Vision vs Frame only).
    *   Checkout (COD / Pickup in Store).
    *   Order History.

### Phase 3: Advanced Optical Features (Future)
*   **Goal:** Full online optician experience.
*   **Features:**
    *   Prescription upload & validation logic.
    *   Virtual Try-On (AR).
    *   Payment Gateway integration.
    *   Appointment Booking for Eye Tests.

---

## 6. Best Practices Checklist

### Security
*   **HTTPS:** Mandatory for all traffic.
*   **Input Validation:** Sanitize all form inputs (Django does this well).
*   **Admin Security:** changing default admin URL, enforcing strong passwords.

### SEO (Search Engine Optimization)
*   **SSR/Prerendering:** Essential if using React.
*   **Meta Tags:** Dynamic OpenGraph tags for every product.
*   **Sitemap.xml:** Auto-generated structured data for eyewear.
*   **Performance:** Core Web Vitals focus (LCP, CLS).

### Performance
*   **Image Optimization:** Serve images in WebP format.
*   **Caching:** Redis caching for Product Lists (freq accessed, rarely changed).
*   **Database:** Indexing on frequent filter fields (price, category).
