# Prime Optical Vision - Visual Codebase Diagram

## System Architecture Overview

```mermaid
graph TB
    User[👤 User] --> Frontend[Frontend Layer]
    
    Frontend --> Templates[HTML Templates]
    Frontend --> Static[CSS/JS Assets]
    
    Frontend --> Backend[Backend Layer - Django Apps]
    
    Backend --> Auth[accounts<br/>Authentication]
    Backend --> Catalog[catalog<br/>Products]
    Backend --> Cart[cart<br/>Shopping Cart]
    Backend --> Orders[orders<br/>Order Management]
    Backend --> Billing[billing<br/>Payments]
    Backend --> Appointments[appointments<br/>Scheduling]
    Backend --> VirtualTryon[virtual_tryon<br/>AR Try-On]
    Backend --> Prescriptions[prescriptions<br/>Rx Management]
    Backend --> Lenses[lenses<br/>Lens Selection]
    Backend --> Inquiries[inquiries<br/>Support]
    Backend --> Core[core<br/>Utilities]
    
    Auth --> DB[(Database)]
    Catalog --> DB
    Cart --> DB
    Orders --> DB
    Billing --> DB
    Appointments --> DB
    VirtualTryon --> DB
    Prescriptions --> DB
    
    Billing -.-> Razorpay[Razorpay API]
    Appointments -.-> Email[Email Service]
    
    style Frontend fill:#d5e8d4,stroke:#82b366
    style Backend fill:#fff2cc,stroke:#d6b656
    style DB fill:#dae8fc,stroke:#6c8ebf
    style VirtualTryon fill:#f8cecc,stroke:#b85450
    style Razorpay fill:#ffe6cc,stroke:#d79b00
    style Email fill:#ffe6cc,stroke:#d79b00
```

## Database Schema Relationships

```mermaid
erDiagram
    User ||--o{ Order : places
    User ||--o{ Cart : has
    User ||--o{ Appointment : books
    User ||--o{ Prescription : uploads
    User ||--o{ TryOnSession : creates
    
    Order ||--|{ OrderItem : contains
    Order ||--o{ Payment : has
    Order ||--|| ShippingAddress : has
    
    Cart ||--|{ CartItem : contains
    
    Product ||--o{ OrderItem : "ordered in"
    Product ||--o{ CartItem : "added to"
    Product ||--o{ ProductImage : has
    Product }o--|| Category : "belongs to"
    Product }o--|| Brand : "made by"
    
    Product ||--o{ LensOption : "available with"
    
    style User fill:#dae8fc
    style Order fill:#ffe6cc
    style Cart fill:#ffe6cc
    style Product fill:#d5e8d4
    style Payment fill:#f8cecc
```

## User Journey Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Catalog
    participant VirtualTryon
    participant Cart
    participant Orders
    participant Billing
    participant Razorpay
    
    User->>Frontend: Browse Products
    Frontend->>Catalog: Get Product List
    Catalog-->>Frontend: Display Products
    
    User->>VirtualTryon: Try On Glasses
    VirtualTryon->>VirtualTryon: Face Detection
    VirtualTryon-->>User: Show AR Preview
    
    User->>Cart: Add to Cart
    Cart->>Cart: Update Session
    Cart-->>User: Cart Updated
    
    User->>Orders: Checkout
    Orders->>Orders: Create Order
    
    Orders->>Billing: Initiate Payment
    Billing->>Razorpay: Create Order
    Razorpay-->>User: Payment Page
    
    User->>Razorpay: Complete Payment
    Razorpay->>Billing: Payment Callback
    Billing->>Billing: Verify Payment
    Billing->>Orders: Update Order Status
    Orders-->>User: Order Confirmation
```

## Application Structure

```mermaid
graph LR
    subgraph "Django Project"
        Config[config/<br/>Settings & URLs]
        
        subgraph "Apps"
            A1[accounts]
            A2[catalog]
            A3[cart]
            A4[orders]
            A5[billing]
            A6[appointments]
            A7[virtual_tryon]
            A8[prescriptions]
            A9[lenses]
            A10[inquiries]
            A11[core]
        end
        
        subgraph "Frontend"
            T[templates/]
            S[static/]
            M[media/]
        end
        
        subgraph "Data"
            DB[(Database)]
        end
    end
    
    Config --> A1
    Config --> A2
    Config --> A3
    Config --> A4
    Config --> A5
    Config --> A6
    Config --> A7
    Config --> A8
    Config --> A9
    Config --> A10
    Config --> A11
    
    A1 --> T
    A2 --> T
    A3 --> T
    A4 --> T
    A5 --> T
    A6 --> T
    A7 --> T
    
    T --> S
    
    A1 --> DB
    A2 --> DB
    A3 --> DB
    A4 --> DB
    A5 --> DB
    A6 --> DB
    A7 --> DB
    A8 --> DB
    
    style Config fill:#dae8fc
    style DB fill:#f8cecc
```

## Data Flow Architecture

```mermaid
flowchart TD
    Start([User Request]) --> Router{URL Router}
    
    Router -->|/catalog/| CatalogView[Catalog Views]
    Router -->|/cart/| CartView[Cart Views]
    Router -->|/orders/| OrderView[Order Views]
    Router -->|/billing/| BillingView[Billing Views]
    Router -->|/virtual-tryon/| TryonView[Virtual Tryon Views]
    Router -->|/appointments/| ApptView[Appointment Views]
    
    CatalogView --> ProductModel[(Product Model)]
    CartView --> CartModel[(Cart Model)]
    OrderView --> OrderModel[(Order Model)]
    BillingView --> PaymentModel[(Payment Model)]
    TryonView --> SessionModel[(TryOn Session)]
    ApptView --> ApptModel[(Appointment Model)]
    
    ProductModel --> Template[Render Template]
    CartModel --> Template
    OrderModel --> Template
    PaymentModel --> Template
    SessionModel --> Template
    ApptModel --> Template
    
    Template --> Response([HTTP Response])
    
    BillingView -.->|API Call| External[Razorpay API]
    External -.->|Callback| BillingView
    
    style Start fill:#d5e8d4
    style Response fill:#d5e8d4
    style External fill:#f8cecc
```

## Feature Modules

```mermaid
mindmap
  root((Prime Optical<br/>Vision))
    Frontend
      Templates
        Base Layout
        Product Pages
        Cart & Checkout
        User Dashboard
      Static Assets
        CSS Styles
        JavaScript
        Images
    Backend Apps
      Core Features
        User Auth
        Product Catalog
        Shopping Cart
        Order Management
      Payment
        Razorpay Integration
        Transaction Tracking
        Invoice Generation
      Premium Features
        Virtual Try-On
        AR Face Detection
        Lens Customization
      Services
        Appointments
        Prescriptions
        Customer Support
    Database
      User Data
      Products
      Orders
      Transactions
    External
      Payment Gateway
      Email Service
      Cloud Storage
```

## Technology Stack

```mermaid
graph TB
    subgraph "Frontend Technologies"
        HTML[HTML5]
        CSS[CSS3]
        JS[JavaScript]
        Bootstrap[Bootstrap Optional]
    end
    
    subgraph "Backend Technologies"
        Django[Django 4.x]
        Python[Python 3.x]
        DjangoORM[Django ORM]
    end
    
    subgraph "Database"
        MySQL[(MySQL)]
        SQLite[(SQLite Dev)]
    end
    
    subgraph "External Services"
        Razorpay[Razorpay API]
        Email[SMTP Email]
    end
    
    subgraph "AR/ML"
        MediaPipe[MediaPipe]
        TensorFlow[TensorFlow.js]
    end
    
    HTML --> Django
    CSS --> Django
    JS --> Django
    
    Django --> DjangoORM
    DjangoORM --> MySQL
    DjangoORM --> SQLite
    
    Django -.-> Razorpay
    Django -.-> Email
    
    JS --> MediaPipe
    JS --> TensorFlow
    
    style Django fill:#092e20,color:#fff
    style Python fill:#3776ab,color:#fff
    style MySQL fill:#4479a1,color:#fff
    style Razorpay fill:#0c2f8a,color:#fff
```

## Deployment Architecture

```mermaid
graph TB
    User[👤 Users] --> LB[Load Balancer]
    
    LB --> Web1[Web Server 1<br/>Gunicorn]
    LB --> Web2[Web Server 2<br/>Gunicorn]
    
    Web1 --> Django[Django Application]
    Web2 --> Django
    
    Django --> Cache[(Redis Cache)]
    Django --> DB[(MySQL Database)]
    Django --> Storage[Media Storage]
    
    Django -.-> Razorpay[Razorpay API]
    Django -.-> Email[Email Service]
    
    Static[Static Files] --> CDN[CDN/Nginx]
    CDN --> User
    
    style User fill:#d5e8d4
    style LB fill:#ffe6cc
    style Django fill:#092e20,color:#fff
    style DB fill:#4479a1,color:#fff
    style Razorpay fill:#0c2f8a,color:#fff
```

## File Organization

```
prime-optical-vision/
│
├── 📁 backend/
│   ├── 📁 apps/
│   │   ├── 📦 accounts/         # User authentication
│   │   ├── 📦 catalog/          # Product management
│   │   ├── 📦 cart/             # Shopping cart
│   │   ├── 📦 orders/           # Order processing
│   │   ├── 📦 billing/          # Payment handling
│   │   ├── 📦 appointments/     # Scheduling
│   │   ├── 📦 virtual_tryon/    # AR try-on
│   │   ├── 📦 prescriptions/    # Rx management
│   │   ├── 📦 lenses/           # Lens options
│   │   ├── 📦 inquiries/        # Support
│   │   └── 📦 core/             # Utilities
│   │
│   ├── 📁 config/               # Django settings
│   ├── 📁 templates/            # HTML templates
│   ├── 📁 static/               # CSS, JS, images
│   ├── 📁 media/                # User uploads
│   └── 📄 manage.py             # Django CLI
│
├── 📁 docs/                     # Documentation
├── 📄 requirements.txt          # Dependencies
├── 📄 .env                      # Environment vars
└── 📄 README.md                 # Project info
```

## Key Features Matrix

| Feature | App | Status | Priority |
|---------|-----|--------|----------|
| User Registration | accounts | ✅ Complete | High |
| Product Catalog | catalog | ✅ Complete | High |
| Shopping Cart | cart | ✅ Complete | High |
| Checkout | orders | ✅ Complete | High |
| Payment Gateway | billing | ✅ Complete | High |
| Order Tracking | orders | ✅ Complete | High |
| Virtual Try-On | virtual_tryon | 🔄 In Progress | Premium |
| Appointments | appointments | ✅ Complete | Medium |
| Prescriptions | prescriptions | ✅ Complete | Medium |
| Lens Selection | lenses | ✅ Complete | Medium |
| Customer Support | inquiries | ✅ Complete | Low |
| Search | catalog | 🔄 Basic | Medium |

## API Endpoints Summary

### Authentication
- `POST /accounts/register/` - Register new user
- `POST /accounts/login/` - User login
- `GET /accounts/profile/` - View profile

### Catalog
- `GET /catalog/` - List products
- `GET /catalog/product/<id>/` - Product details
- `GET /catalog/category/<slug>/` - Category products

### Cart & Orders
- `POST /cart/add/` - Add to cart
- `GET /cart/` - View cart
- `POST /orders/create/` - Create order
- `GET /orders/<id>/` - Order details

### Payments
- `POST /billing/create-order/` - Initialize payment
- `POST /billing/verify/` - Verify payment

### Features
- `GET /virtual-tryon/` - AR interface
- `POST /appointments/book/` - Book appointment
- `POST /prescriptions/upload/` - Upload prescription

---

**Generated**: December 27, 2025  
**Version**: 1.0  
**Tool**: Code Diagram Generator
