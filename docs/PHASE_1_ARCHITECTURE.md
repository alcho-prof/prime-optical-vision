# Phase 1 Architecture: Digital Catalog & Lead Gen (MVP)

**Phase Objective:** Build a stable, SEO-friendly digital catalog to showcase eyewear products and capture customer interest via inquiries.

---

## 1. Functional Modules & Responsibilities

| App Name | Role | Responsibilities | Key Interactions |
| :--- | :--- | :--- | :--- |
| **core** | Infrastructure | Base abstract models (`TimeStampedModel`), Global Utils. | Inherited by all other apps. |
| **users** | Authentication | Store Admin accounts. (Customer auth disabled for Phase 1). | Manages `request.user` context. |
| **catalog** | Domain Logic | Manage Categories, Products, Variants. Logic for "Active" vs "Hidden" inventory. | Queries by `inquiries` app. |
| **inquiries** | Conversion | Handle "Contact Us" forms. Store Customer Name, Phone, and Interest. | Links to `Product` model. |
| **content** | Presentation | Static pages (Home, About). Landing page logic. | Entry point for users. |

---

## 2. Data Model Design (Schema)

| Model | App | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| **Category** | `catalog` | `name`, `slug`, `is_active` | `parent` (Self-ForeignKey) |
| **Product** | `catalog` | `name`, `slug`, `price_range`, `is_active` | `category` (FK) |
| **ProductVariant** | `catalog` | `color_name`, `image`, `in_stock` | `product` (FK) |
| **Inquiry** | `inquiries` | `customer_name`, `phone`, `message` | `product` (FK) |

---

## 3. Workflow Specifications

### A. User Browsing Flow
| Step | Action | System Response |
| :--- | :--- | :--- |
| 1 | **Home Page** | User lands on `/`. Sees Featured Categories. |
| 2 | **Catalog** | User clicks "Eyeglasses". System filters `Product.objects.filter(category='eyeglasses')`. |
| 3 | **Detail Views** | User clicks Product Card. System renders `/products/<slug>/`. |
| 4 | **Validation** | If Product or Category is inactive -> **404 Not Found**. |

### B. Inquiry Flow (Lead Gen)
| Step | Action | System Logic |
| :--- | :--- | :--- |
| 1 | **Form View** | User sees "Make an Inquiry" form on `product_detail.html`. |
| 2 | **Submission** | POST request sent to server. CSRF token verified. |
| 3 | **Validation** | Form validated (Name/Phone required). |
| 4 | **Persistence** | Inquiry saved to Database (`inquiries_inquiry` table). |
| 5 | **Notification** | `send_mail()` triggers console/SMTP email to Admin. |
| 6 | **Feedback** | Page reloads with "Thank You" success message. |

---

## 4. Key Limitations (Scope Control)

| Feature | Phase 1 Status | Reason |
| :--- | :--- | :--- |
| **User Sign Up** | ❌ Disabled | Focus is on guest browsing and quick conversion. |
| **Shopping Cart** | ❌ Disabled | Replaced by direct Inquiry Form. |
| **Online Payments** | ❌ Disabled | High complexity; business model relies on store visit. |
| **JS Frameworks** | ❌ Disabled | SEO and simplicity prioritized (Django Templates). |
