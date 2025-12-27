# Prime Optical Vision - Codebase Architecture

## Project Overview
Prime Optical Vision is a comprehensive Django-based e-commerce platform for optical products with virtual try-on capabilities.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Prime Optical Vision                          │
│                   Django Web Application                         │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │Frontend │          │ Backend │          │Database │
   │Templates│          │  Apps   │          │ MySQL/  │
   │   CSS   │          │  Logic  │          │ SQLite  │
   │   JS    │          │  APIs   │          │         │
   └─────────┘          └─────────┘          └─────────┘
```

## Directory Structure

```
prime-optical-vision/
│
├── backend/                    # Main Django application
│   ├── apps/                   # Django applications (modular components)
│   │   ├── accounts/          # User authentication & profiles
│   │   ├── appointments/      # Eye exam scheduling
│   │   ├── billing/           # Payment processing (Razorpay)
│   │   ├── cart/              # Shopping cart functionality
│   │   ├── catalog/           # Product catalog & management
│   │   ├── content/           # CMS content management
│   │   ├── core/              # Core utilities & template tags
│   │   ├── inquiries/         # Customer inquiries & support
│   │   ├── lenses/            # Lens selection & customization
│   │   ├── orders/            # Order management & tracking
│   │   ├── prescriptions/     # Prescription management
│   │   ├── users/             # User management
│   │   └── virtual_tryon/     # AR virtual try-on feature
│   │
│   ├── config/                # Django project configuration
│   │   ├── settings.py        # Main settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py            # WSGI configuration
│   │
│   ├── static/                # Static files (CSS, JS, images)
│   │   ├── css/               # Stylesheets
│   │   ├── js/                # JavaScript files
│   │   └── images/            # Image assets
│   │
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template
│   │   ├── accounts/          # Account templates
│   │   ├── appointments/      # Appointment templates
│   │   ├── cart/              # Cart templates
│   │   ├── catalog/           # Product catalog templates
│   │   └── ...                # Other app templates
│   │
│   ├── media/                 # User-uploaded files
│   ├── manage.py              # Django management script
│   └── db.sqlite3             # Development database
│
├── docs/                      # Documentation
│   ├── PHASE_4_PLAN.md        # Development phase plans
│   ├── VIRTUAL_TRYON_DOCUMENTATION.md
│   └── CODE_MAP.md            # Code mapping documentation
│
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── .env.example               # Environment template
└── README.md                  # Project documentation
```

## Application Architecture

### Core Django Apps

#### 1. **accounts** - User Authentication
```
accounts/
├── models.py          # User profile models
├── views.py           # Login, register, profile views
├── forms.py           # Authentication forms
├── urls.py            # Account URL patterns
└── admin.py           # Admin configuration
```

**Key Features:**
- User registration and login
- Profile management
- Password reset
- User dashboard

#### 2. **catalog** - Product Management
```
catalog/
├── models.py          # Product, Category, Brand models
├── views.py           # Product listing, detail views
├── urls.py            # Catalog URL patterns
└── admin.py           # Product admin interface
```

**Key Models:**
- `Product`: Eyewear products
- `Category`: Product categories
- `Brand`: Eyewear brands
- `ProductImage`: Product images

#### 3. **cart** - Shopping Cart
```
cart/
├── models.py          # Cart, CartItem models
├── views.py           # Cart operations
├── urls.py            # Cart URL patterns
└── cart.py            # Cart session management
```

**Key Features:**
- Add/remove items
- Update quantities
- Cart persistence
- Price calculations

#### 4. **orders** - Order Management
```
orders/
├── models.py          # Order, OrderItem models
├── views.py           # Order creation, tracking
├── urls.py            # Order URL patterns
└── admin.py           # Order admin interface
```

**Key Models:**
- `Order`: Customer orders
- `OrderItem`: Individual order items
- `ShippingAddress`: Delivery addresses

#### 5. **billing** - Payment Processing
```
billing/
├── models.py          # Payment, Transaction models
├── views.py           # Payment gateway integration
├── urls.py            # Payment URL patterns
└── razorpay.py        # Razorpay integration
```

**Key Features:**
- Razorpay integration
- Payment verification
- Transaction tracking
- Invoice generation

#### 6. **appointments** - Scheduling
```
appointments/
├── models.py          # Appointment model
├── views.py           # Booking, management views
├── forms.py           # Appointment forms
└── urls.py            # Appointment URL patterns
```

**Key Features:**
- Eye exam scheduling
- Appointment management
- Calendar integration
- Email notifications

#### 7. **virtual_tryon** - AR Try-On
```
virtual_tryon/
├── models.py          # Try-on session models
├── views.py           # AR functionality
├── urls.py            # Try-on URL patterns
└── static/
    └── js/
        └── virtual-tryon.js  # AR implementation
```

**Key Features:**
- Face detection
- Frame overlay
- Photo capture
- Try-on history

#### 8. **prescriptions** - Prescription Management
```
prescriptions/
├── models.py          # Prescription model
├── views.py           # Upload, management views
├── forms.py           # Prescription forms
└── urls.py            # Prescription URL patterns
```

#### 9. **lenses** - Lens Selection
```
lenses/
├── models.py          # Lens types, coatings
├── views.py           # Lens selection views
└── urls.py            # Lens URL patterns
```

#### 10. **inquiries** - Customer Support
```
inquiries/
├── models.py          # Inquiry, Message models
├── views.py           # Contact form, support
├── forms.py           # Inquiry forms
└── urls.py            # Inquiry URL patterns
```

#### 11. **core** - Utilities
```
core/
├── templatetags/      # Custom template tags
├── middleware.py      # Custom middleware
└── utils.py           # Helper functions
```

## Data Flow Architecture

### 1. Product Browsing Flow
```
User Request
    ↓
URL Router (urls.py)
    ↓
Catalog Views
    ↓
Product Models (Database Query)
    ↓
Template Rendering
    ↓
HTTP Response (HTML)
```

### 2. Shopping Cart Flow
```
Add to Cart Request
    ↓
Cart View
    ↓
Session/Database Update
    ↓
Cart Model Update
    ↓
JSON/Redirect Response
```

### 3. Checkout Flow
```
Checkout Initiation
    ↓
Order Creation
    ↓
Payment Gateway (Razorpay)
    ↓
Payment Verification
    ↓
Order Confirmation
    ↓
Email Notification
```

### 4. Virtual Try-On Flow
```
Camera Access Request
    ↓
Face Detection (JavaScript)
    ↓
Frame Overlay Rendering
    ↓
Capture & Save
    ↓
Try-On Session Storage
```

## Database Schema

### Key Relationships

```
User (1) ──────── (M) Order
                        │
                        └── (M) OrderItem ──── (1) Product
                                                     │
                                                     ├── (1) Category
                                                     └── (1) Brand

User (1) ──────── (M) Cart
                        │
                        └── (M) CartItem ──── (1) Product

User (1) ──────── (M) Appointment

User (1) ──────── (M) Prescription

Order (1) ─────── (M) Payment

Product (1) ───── (M) ProductImage
```

## Technology Stack

### Backend
- **Framework**: Django 4.x
- **Language**: Python 3.x
- **Database**: MySQL (Production), SQLite (Development)
- **ORM**: Django ORM

### Frontend
- **Templates**: Django Templates
- **CSS**: Custom CSS + Bootstrap (optional)
- **JavaScript**: Vanilla JS + AR libraries
- **AR**: MediaPipe / TensorFlow.js (for virtual try-on)

### Payment Integration
- **Gateway**: Razorpay
- **Features**: Order creation, payment verification

### Deployment
- **Server**: WSGI (Gunicorn/uWSGI)
- **Static Files**: WhiteNoise / Nginx
- **Media Files**: Local storage / Cloud storage

## API Endpoints

### Authentication
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout
- `GET /accounts/profile/` - User profile

### Catalog
- `GET /catalog/` - Product listing
- `GET /catalog/product/<id>/` - Product detail
- `GET /catalog/category/<slug>/` - Category products

### Cart
- `POST /cart/add/<product_id>/` - Add to cart
- `POST /cart/remove/<item_id>/` - Remove from cart
- `GET /cart/` - View cart

### Orders
- `POST /orders/create/` - Create order
- `GET /orders/<order_id>/` - Order detail
- `GET /orders/history/` - Order history

### Payments
- `POST /billing/create-order/` - Create Razorpay order
- `POST /billing/verify-payment/` - Verify payment

### Appointments
- `POST /appointments/book/` - Book appointment
- `GET /appointments/list/` - View appointments

### Virtual Try-On
- `GET /virtual-tryon/` - Try-on interface
- `POST /virtual-tryon/save/` - Save try-on session

## Security Features

1. **CSRF Protection**: Django CSRF middleware
2. **Authentication**: Django authentication system
3. **Password Hashing**: PBKDF2 algorithm
4. **SQL Injection Prevention**: ORM parameterized queries
5. **XSS Protection**: Template auto-escaping
6. **HTTPS**: Enforced in production
7. **Environment Variables**: Sensitive data in .env

## Development Workflow

### Phase 1: Foundation
- ✅ Project setup
- ✅ Database configuration
- ✅ Basic models

### Phase 2: Core Features
- ✅ User authentication
- ✅ Product catalog
- ✅ Shopping cart
- ✅ Checkout process

### Phase 3: Advanced Features
- ✅ Payment integration
- ✅ Order management
- ✅ Appointment booking

### Phase 4: Premium Features
- 🔄 Virtual try-on
- 🔄 Advanced search
- 🔄 Recommendations
- 🔄 Analytics

## Configuration Files

### settings.py
- Database configuration
- Installed apps
- Middleware
- Static/media files
- Security settings

### urls.py
- URL routing
- App URL includes
- Admin URLs

### .env
- Secret keys
- Database credentials
- API keys (Razorpay)
- Debug settings

## Static Assets Organization

```
static/
├── css/
│   ├── base.css              # Global styles
│   ├── product-list.css      # Product listing
│   ├── product-detail.css    # Product detail
│   ├── cart.css              # Shopping cart
│   ├── checkout.css          # Checkout page
│   └── virtual-tryon.css     # AR try-on
│
├── js/
│   ├── main.js               # Global scripts
│   ├── product-detail.js     # Product interactions
│   ├── cart.js               # Cart operations
│   └── virtual-tryon.js      # AR functionality
│
└── images/
    ├── logo.png
    ├── placeholder.jpg
    └── icons/
```

## Testing Strategy

1. **Unit Tests**: Model and utility testing
2. **Integration Tests**: View and form testing
3. **Functional Tests**: End-to-end workflows
4. **Manual Testing**: UI/UX validation

## Performance Optimization

1. **Database Indexing**: Key fields indexed
2. **Query Optimization**: select_related, prefetch_related
3. **Caching**: Template fragment caching
4. **Static Files**: Compression and CDN
5. **Image Optimization**: Thumbnails and lazy loading

## Future Enhancements

1. **Mobile App**: React Native / Flutter
2. **AI Recommendations**: ML-based suggestions
3. **Advanced Analytics**: User behavior tracking
4. **Multi-language Support**: i18n implementation
5. **Progressive Web App**: PWA features
6. **Social Integration**: Social login and sharing

## Maintenance & Monitoring

1. **Logging**: Django logging framework
2. **Error Tracking**: Sentry integration (planned)
3. **Performance Monitoring**: Django Debug Toolbar
4. **Backup Strategy**: Database backups
5. **Version Control**: Git with feature branches

---

**Last Updated**: December 27, 2025
**Version**: 1.0
**Maintainer**: Development Team
