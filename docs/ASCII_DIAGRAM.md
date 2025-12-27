# Prime Optical Vision - ASCII Codebase Diagram

## System Architecture (High-Level)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRIME OPTICAL VISION                                  │
│                     E-Commerce Platform for Eyewear                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
        ┌───────▼────────┐   ┌───────▼────────┐   ┌───────▼────────┐
        │   FRONTEND     │   │    BACKEND     │   │   DATABASE     │
        │   LAYER        │   │    LAYER       │   │   LAYER        │
        └────────────────┘   └────────────────┘   └────────────────┘
```

## Detailed Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Browser    │  │   Mobile     │  │   Tablet     │  │   Desktop    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND LAYER                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  HTML Templates (Django Template Engine)                             │  │
│  │  • base.html                  • product_list.html                    │  │
│  │  • product_detail.html        • cart_detail.html                     │  │
│  │  • checkout.html              • order_confirmation.html              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Static Assets                                                        │  │
│  │  • CSS (Stylesheets)          • JavaScript (Interactivity)           │  │
│  │  • Images (Assets)            • Fonts (Typography)                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        URL ROUTING LAYER                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  config/urls.py (Main URL Configuration)                             │  │
│  │  • /accounts/     → accounts.urls                                    │  │
│  │  • /catalog/      → catalog.urls                                     │  │
│  │  • /cart/         → cart.urls                                        │  │
│  │  • /orders/       → orders.urls                                      │  │
│  │  • /billing/      → billing.urls                                     │  │
│  │  • /appointments/ → appointments.urls                                │  │
│  │  • /virtual-tryon/→ virtual_tryon.urls                               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND LAYER (Django Apps)                          │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   accounts   │  │   catalog    │  │     cart     │  │    orders    │   │
│  │              │  │              │  │              │  │              │   │
│  │ • User Auth  │  │ • Products   │  │ • Shopping   │  │ • Order Mgmt │   │
│  │ • Profile    │  │ • Categories │  │   Cart       │  │ • Tracking   │   │
│  │ • Login      │  │ • Brands     │  │ • Session    │  │ • History    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   billing    │  │ appointments │  │virtual_tryon │  │prescriptions │   │
│  │              │  │              │  │              │  │              │   │
│  │ • Razorpay   │  │ • Scheduling │  │ • AR Try-On  │  │ • Rx Upload  │   │
│  │ • Payments   │  │ • Booking    │  │ • Face Det.  │  │ • Validation │   │
│  │ • Invoices   │  │ • Calendar   │  │ • Capture    │  │ • Storage    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │    lenses    │  │  inquiries   │  │    users     │  │     core     │   │
│  │              │  │              │  │              │  │              │   │
│  │ • Lens Types │  │ • Support    │  │ • User Mgmt  │  │ • Utilities  │   │
│  │ • Coatings   │  │ • Contact    │  │ • Profiles   │  │ • Helpers    │   │
│  │ • Options    │  │ • Messages   │  │ • Settings   │  │ • Tags       │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA ACCESS LAYER                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Django ORM (Object-Relational Mapping)                              │  │
│  │  • Model Definitions          • Query Optimization                   │  │
│  │  • Relationships              • Migrations                           │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATABASE LAYER                                      │
│                                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   User   │  │ Product  │  │  Order   │  │   Cart   │  │ Payment  │     │
│  │  Table   │  │  Table   │  │  Table   │  │  Table   │  │  Table   │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │             │             │             │            │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐     │
│  │Appoint-  │  │Prescrip- │  │  Lens    │  │ Inquiry  │  │ TryOn    │     │
│  │  ment    │  │  tion    │  │ Option   │  │          │  │ Session  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                                              │
│  Database: MySQL (Production) / SQLite (Development)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                                     │
│  ┌──────────────────────────┐         ┌──────────────────────────┐         │
│  │    Razorpay API          │         │    Email Service         │         │
│  │  • Payment Gateway       │         │  • SMTP Server           │         │
│  │  • Order Creation        │         │  • Notifications         │         │
│  │  • Payment Verification  │         │  • Confirmations         │         │
│  └──────────────────────────┘         └──────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
USER REQUEST FLOW
═════════════════

1. Product Browsing
   ┌──────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ User │─────▶│ Catalog  │─────▶│ Product  │─────▶│ Template │
   │      │      │  View    │      │  Model   │      │ Render   │
   └──────┘      └──────────┘      └──────────┘      └──────────┘
                                                            │
                                                            ▼
                                                      ┌──────────┐
                                                      │   HTML   │
                                                      │ Response │
                                                      └──────────┘

2. Shopping Cart
   ┌──────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ User │─────▶│   Cart   │─────▶│   Cart   │─────▶│ Session  │
   │      │      │  View    │      │  Model   │      │  Update  │
   └──────┘      └──────────┘      └──────────┘      └──────────┘

3. Checkout & Payment
   ┌──────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ User │─────▶│  Order   │─────▶│ Billing  │─────▶│ Razorpay │
   │      │      │  View    │      │  View    │      │   API    │
   └──────┘      └──────────┘      └──────────┘      └──────────┘
                                                            │
                                                            ▼
                                                      ┌──────────┐
                                                      │ Payment  │
                                                      │  Page    │
                                                      └──────────┘
                                                            │
                                                            ▼
   ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   │  Order   │◀─────│ Payment  │◀─────│ Verify   │◀─────│ Callback │
   │Confirmed │      │  Update  │      │ Payment  │      │          │
   └──────────┘      └──────────┘      └──────────┘      └──────────┘

4. Virtual Try-On
   ┌──────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ User │─────▶│ Virtual  │─────▶│   Face   │─────▶│  Frame   │
   │      │      │  Tryon   │      │ Detection│      │ Overlay  │
   └──────┘      └──────────┘      └──────────┘      └──────────┘
                                                            │
                                                            ▼
                                                      ┌──────────┐
                                                      │  Capture │
                                                      │  & Save  │
                                                      └──────────┘
```

## Database Relationships

```
DATABASE SCHEMA
═══════════════

┌─────────────┐
│    User     │
│─────────────│
│ id (PK)     │
│ username    │
│ email       │
│ password    │
└──────┬──────┘
       │
       │ 1:M
       │
       ├────────────────┬────────────────┬────────────────┬────────────────┐
       │                │                │                │                │
       ▼                ▼                ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    Order    │  │    Cart     │  │ Appointment │  │Prescription │  │  TryOn      │
│─────────────│  │─────────────│  │─────────────│  │─────────────│  │  Session    │
│ id (PK)     │  │ id (PK)     │  │ id (PK)     │  │ id (PK)     │  │─────────────│
│ user_id(FK) │  │ user_id(FK) │  │ user_id(FK) │  │ user_id(FK) │  │ id (PK)     │
│ total       │  │ created_at  │  │ date        │  │ file        │  │ user_id(FK) │
│ status      │  └──────┬──────┘  │ time        │  │ verified    │  │ product_id  │
└──────┬──────┘         │         │ status      │  └─────────────┘  │ image       │
       │                │         └─────────────┘                   └─────────────┘
       │ 1:M            │ 1:M
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│  OrderItem  │  │  CartItem   │
│─────────────│  │─────────────│
│ id (PK)     │  │ id (PK)     │
│ order_id(FK)│  │ cart_id(FK) │
│product_id(FK)│  │product_id(FK)│
│ quantity    │  │ quantity    │
│ price       │  └──────┬──────┘
└──────┬──────┘         │
       │                │
       │                │
       └────────┬───────┘
                │
                ▼
         ┌─────────────┐
         │   Product   │
         │─────────────│
         │ id (PK)     │
         │ name        │
         │ price       │
         │category_id  │
         │ brand_id    │
         │ description │
         └──────┬──────┘
                │
                │ M:1
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Category   │   │    Brand    │
│─────────────│   │─────────────│
│ id (PK)     │   │ id (PK)     │
│ name        │   │ name        │
│ slug        │   │ logo        │
└─────────────┘   └─────────────┘


┌─────────────┐
│    Order    │
│─────────────│
│ id (PK)     │
└──────┬──────┘
       │
       │ 1:M
       │
       ▼
┌─────────────┐
│   Payment   │
│─────────────│
│ id (PK)     │
│ order_id(FK)│
│ amount      │
│ status      │
│ razorpay_id │
└─────────────┘
```

## Application Module Structure

```
DJANGO APPS BREAKDOWN
═════════════════════

accounts/
├── models.py ────────── User, Profile
├── views.py ─────────── LoginView, RegisterView, ProfileView
├── forms.py ─────────── LoginForm, RegisterForm
├── urls.py ──────────── /login/, /register/, /profile/
└── admin.py ─────────── UserAdmin

catalog/
├── models.py ────────── Product, Category, Brand, ProductImage
├── views.py ─────────── ProductListView, ProductDetailView
├── urls.py ──────────── /catalog/, /product/<id>/
└── admin.py ─────────── ProductAdmin, CategoryAdmin

cart/
├── models.py ────────── Cart, CartItem
├── views.py ─────────── CartView, AddToCartView, RemoveFromCartView
├── cart.py ──────────── Cart Session Manager
├── urls.py ──────────── /cart/, /add/<id>/, /remove/<id>/
└── admin.py ─────────── CartAdmin

orders/
├── models.py ────────── Order, OrderItem, ShippingAddress
├── views.py ─────────── OrderCreateView, OrderDetailView, OrderListView
├── urls.py ──────────── /create/, /order/<id>/, /history/
└── admin.py ─────────── OrderAdmin

billing/
├── models.py ────────── Payment, Transaction
├── views.py ─────────── PaymentView, VerifyPaymentView
├── razorpay.py ──────── Razorpay Integration
├── urls.py ──────────── /create-order/, /verify/
└── admin.py ─────────── PaymentAdmin

appointments/
├── models.py ────────── Appointment
├── views.py ─────────── AppointmentBookView, AppointmentListView
├── forms.py ─────────── AppointmentForm
├── urls.py ──────────── /book/, /list/
└── admin.py ─────────── AppointmentAdmin

virtual_tryon/
├── models.py ────────── TryOnSession
├── views.py ─────────── VirtualTryOnView, SaveSessionView
├── static/js/ ───────── virtual-tryon.js (AR Logic)
├── urls.py ──────────── /tryon/, /save/
└── admin.py ─────────── TryOnSessionAdmin

prescriptions/
├── models.py ────────── Prescription
├── views.py ─────────── UploadPrescriptionView, PrescriptionListView
├── forms.py ─────────── PrescriptionForm
└── urls.py ──────────── /upload/, /list/

lenses/
├── models.py ────────── LensType, LensCoating, LensOption
├── views.py ─────────── LensSelectionView
└── urls.py ──────────── /select/

inquiries/
├── models.py ────────── Inquiry, Message
├── views.py ─────────── ContactView, InquiryListView
├── forms.py ─────────── ContactForm
└── urls.py ──────────── /contact/, /inquiries/

core/
├── templatetags/ ────── Custom template tags
├── middleware.py ────── Custom middleware
└── utils.py ─────────── Helper functions
```

## Technology Stack

```
TECHNOLOGY LAYERS
═════════════════

┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │   HTML5    │  │    CSS3    │  │ JavaScript │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                      │
│  ┌────────────────────────────────────────────────┐     │
│  │              Django 4.x Framework              │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │     │
│  │  │  Views   │  │  Models  │  │Templates │     │     │
│  │  └──────────┘  └──────────┘  └──────────┘     │     │
│  └────────────────────────────────────────────────┘     │
│                   Python 3.x                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                          │
│  ┌────────────────────────────────────────────────┐     │
│  │              Django ORM                        │     │
│  └────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────┐     │
│  │  MySQL (Production) / SQLite (Development)     │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  INTEGRATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Razorpay    │  │    SMTP      │  │  MediaPipe   │  │
│  │     API      │  │    Email     │  │  (AR/ML)     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Feature Status Matrix

```
FEATURE IMPLEMENTATION STATUS
══════════════════════════════

Core Features:
  [✓] User Authentication       (accounts)
  [✓] Product Catalog           (catalog)
  [✓] Shopping Cart             (cart)
  [✓] Checkout Process          (orders)
  [✓] Payment Gateway           (billing)
  [✓] Order Management          (orders)

Additional Features:
  [✓] Appointment Booking       (appointments)
  [✓] Prescription Upload       (prescriptions)
  [✓] Lens Selection            (lenses)
  [✓] Customer Support          (inquiries)
  [~] Virtual Try-On            (virtual_tryon) - In Progress
  [~] Advanced Search           (catalog) - Basic Implementation

Premium Features:
  [ ] AI Recommendations
  [ ] Multi-language Support
  [ ] Progressive Web App
  [ ] Social Integration
  [ ] Advanced Analytics

Legend:
  [✓] Complete
  [~] In Progress
  [ ] Planned
```

## Quick Reference Guide

```
COMMON OPERATIONS
═════════════════

Start Development Server:
  $ cd backend
  $ python manage.py runserver

Run Migrations:
  $ python manage.py makemigrations
  $ python manage.py migrate

Create Superuser:
  $ python manage.py createsuperuser

Collect Static Files:
  $ python manage.py collectstatic

Run Tests:
  $ python manage.py test

Access Admin Panel:
  http://localhost:8000/admin/

Main URLs:
  /                     → Home Page
  /catalog/             → Product Listing
  /cart/                → Shopping Cart
  /orders/              → Order Management
  /virtual-tryon/       → AR Try-On
  /appointments/        → Book Appointment
```

---

**Generated**: December 27, 2025  
**Version**: 1.0  
**Maintainer**: Development Team
