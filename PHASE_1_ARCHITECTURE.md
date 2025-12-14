# Phase 1 Architecture Blueprint: Prime Optical (Digital Catalog)

**Role:** Senior Software Architect  
**Projects Phase:** Phase 1 – Digital Catalog & Brand Presence (MVP)  
**Date:** 2025-12-14  

---

## 1. Phase-1 Architecture Overview

We will strictly adhere to a **Modular Monolith** architecture pattern. This foundation allows for distinct business domains (Catalog, Content, Lenses) to coexist within a single Django deployment while remaining decoupled enough for future micro-services extraction or complex integrations (like ERP/Inventory systems) in later phases.

**Selected Frontend Strategy:** **Django Templates (Server-Side Rendering)**  
*   **Justification:**
    *   **SEO:** Critical for a "Brand Presence" site. SSR guarantees content indexability without complex hydration or pre-rendering setups required by React/Next.js.
    *   **Performance:** Faster First Contentful Paint (FCP) for mobile users on varied connections.
    *   **Simplicity:** Reduces devops complexity (no separate Node.js server or build pipelines). Ideal for a read-heavy, low-interactivity Catalog.

### Django Apps & Responsibilities

1.  **`core`**: 
    *   **Responsibility:** System-wide utilities, abstract base models (TimeStampedModel), and global configuration.
2.  **`content`**: 
    *   **Responsibility:** Static/Marketing pages (Home, About, Contact). Stores business hours, locations, and SEO metadata for static pages.
3.  **`catalog`**: 
    *   **Responsibility:** The core engine. Manages Categories, Products, and Variants. Handles product retrieval and filtering logic.
4.  **`lenses`**: 
    *   **Responsibility:** Educational content management. Stores data about Lens Types and Coatings strictly for display/information purposes.
5.  **`inquiries`**: 
    *   **Responsibility:** Replaces "Orders". Handles the "Contact Us" or "Inquire about this product" form submissions. Stores leads in the DB and triggers email notifications.

---

## 2. Folder & File Structure

We utilize a "src-like" structure where all functional apps reside in an `apps/` directory to keep the root clean.

```text
product_root/
├── manage.py
├── .env                        # Environment variables (Secrets)
├── requirements.txt
├── config/                     # Project Configuration
│   ├── settings/               # Split settings (base, dev, prod)
│   ├── urls.py                 # Main URL routing (Dispatcher)
│   └── wsgi.py                 # Entry point
│
├── apps/                       # Domain Logic
│   ├── core/
│   │   ├── models.py           # Abstract Base Models
│   │   └── utils.py
│   ├── catalog/
│   │   ├── models.py           # Category, Product, ProductVariant
│   │   ├── services.py         # Business logic (get_related_products, etc)
│   │   ├── admin.py            # Optimized Admin panels
│   │   └── views.py            # Read-Only Views
│   ├── lenses/
│   ├── inquiries/
│   │   ├── forms.py            # InquiryForm
│   │   └── emails.py           # Email notification logic
│   └── content/
│
├── static/                     # Global Static (CSS/JS)
│   ├── css/                    # Optimized CSS 
│   ├── js/                     # Minimal interaction scripts
│   └── images/                 # Theme assets
│
└── templates/                  # Presentation Layer
    ├── base.html               # Main Skeleton (SEO tags, Header, Footer)
    ├── components/             # Reusable chunks (ProductCard, Navbar)
    ├── catalog/
    │   ├── product_list.html
    │   └── product_detail.html
    └── pages/                  # Home, About, Contact
```

---

## 3. Data Model Design (Phase 1)

### App: `catalog`

**1. Category**
*   **Purpose:** Organizing products hierarchy (e.g., Men > Eyeglasses).
*   `name` (CharField): Display name.
*   `slug` (SlugField): SEO friendly URL part.
*   `parent` (ForeignKey): Self-referential for sub-categories.
*   `is_active` (BooleanField): To hide seasonal categories.

**2. Product**
*   **Purpose:** The main entity representing a frame style.
*   `name` (CharField): E.g., "Ray-Ban Aviator Classic".
*   `slug` (SlugField): Unique URL identifier.
*   `category` (ForeignKey): Link to Category.
*   `description` (TextField): Full marketing copy.
*   `price_range` (CharField): Textual (e.g., "₹2000 - ₹5000") since we aren't transacting yet, or a nullable DecimalField for "Starting At".
*   `is_featured` (BooleanField): For Home page promotion.

**3. ProductVariant**
*   **Purpose:** Specific SKUs (Color/Size).
*   `product` (ForeignKey): Parent Product.
*   `color_name` (CharField): E.g., "Matte Black".
*   `image` (ImageField): Specific image for this variant.
*   `in_stock` (BooleanField): **Simple Availability Flag**.

### App: `lenses`

**4. LensType**
*   **Purpose:** Educational content.
*   `name`: "Bifocal", "Progressive".
*   `description`: Explanation of benefits.
*   `recommended_for`: Text field (e.g., "Reading & Distance").

**5. LensCoating**
*   **Purpose:** Educational content.
*   `name`: "Blue Cut", "Anti-Glare".
*   `benefit`: Description of why a user needs it.

---

## 4. Workflow Explanation

### A. User Browsing Workflow
1.  **Entry:** User lands on Home Page -> Sees "Featured Categories".
2.  **Discovery:** Clicks "Eyeglasses". System queries `Product.objects.filter(category='eyeglasses', is_active=True)`.
3.  **Detail:** User clicks a product card. System renders `product_detail.html`.
    *   Displays Description, Price Range.
    *   Shows Variants (Colors) as a simple image gallery.
    *   Shows "Lens Compatibility" info (fetched from static context or generic relation).

### B. Inquiry Workflow (The Conversion Goal)
1.  **Action:** User clicks "Inquire about this Frame" on the Product Detail Page.
2.  **Interaction:** A Modal or Form appears.
3.  **Input:** User enters Name, Phone, and optional Message.
4.  **Process:**
    *   Form validated in `inquiries` app.
    *   Data saved to `Inquiry` model.
    *   **Notification:** System sends email to Store Admin with "Lead: [Product Name] - [Customer Phone]".
5.  **Feedback:** User sees "Thank you! We will call you shortly."

### C. Admin Management Workflow
1.  **Login:** Staff logs into standard Django Admin (path `/admin/`).
2.  **Product Entry:** Admin goes to Catalog -> Add Product.
    *   Fills basic details.
    *   Adds Variants inline (images, colors) on the *same* screen.
    *   Sets `is_active=True` to publish.
3.  **Lead Management:** Admin checks "Inquiries" section to see list of interested customers.

---

## 5. Admin Panel Design (Django Admin)

We will heavily customize the default admin for usability.

*   **ProductAdmin:**
    *   **List Display:** Image Thumbnail, Name, Category, Is Active, In Stock Status.
    *   **Filters:** CategoryFilter, StockStatusFilter.
    *   **Search:** By Name, SKU.
    *   **Inlines:** `ProductVariantInline` (allows adding colors/images directly inside the Product page).

*   **InquiryAdmin:**
    *   **List Display:** Date, Customer Name, Phone, Product Interested.
    *   **Read-Only:** Staff should not be able to edit inquiries, only view/delete.

---

## 6. Non-Functional Considerations

### SEO Strategy (Priority #1)
*   **Title Tags:** Format `"{Product Name} | Buy at Prime Optical"`.
*   **Open Graph:** All product pages must have `og:image` and `og:description` for WhatsApp/Facebook sharing.
*   **Sitemap:** Auto-generate `sitemap.xml` listing all active product URLs.

### Performance
*   **Image Optimization:** Use `Sorl-thumbnail` or Django's image tools to resize variant images on the fly. Do not serve raw 5MB uploads.
*   **Caching:** Enable Per-View caching for the Home Page and Product Lists (TTL: 15 mins).

### Security
*   **CSRF Protection:** Enabled on all Inquiry forms.
*   **Content Security Policy (CSP):** Restrict script sources (prevent XSS).
*   **Admin URL:** Change default `admin/` to something obscure (e.g., `staff-portal/`) to reduce brute-force noise.
