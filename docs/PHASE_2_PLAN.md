# Phase 2: Basic E-Commerce (Implementation Plan)

**Phase Objective:** Enable transactional capabilities, user management, and specific optical e-commerce features (lens selection) to transform the catalog into a functioning store.

---

## ✅ Task 2.1: User Accounts (Authentication) [COMPLETED]
*   **Goal:** Secure user registration, login, and profile management.
*   **Sub-tasks:**
    *   `apps.accounts` creation.
    *   Custom `User` model (Phone, Verification).
    *   Registration View (split Name, auto-login).
    *   Login/Logout Views (Custom redirects).
    *   Profile View (Update details).
    *   **Admin Feature:** "Login without password" option for specific users.

---

## ⏳ Task 2.2: Shopping Cart [PENDING]
*   **Goal:** Allow users to collect products before inquiring/purchasing.
*   **Sub-tasks:**
    *   Create `apps.cart`.
    *   Session-based cart storage (Database-backed for persistency).
    *   `Cart` and `CartItem` models.
    *   Views: `add_to_cart`, `remove_from_cart`, `update_quantity`.
    *   Template: `cart_detail.html` (Summary table).
    *   Context Processor for cart count bubble in Navbar.

---

## ⏳ Task 2.3: Lens Selection Logic [PENDING]
*   **Goal:** Optical-specific customization during "Add to Cart".
*   **Sub-tasks:**
    *   Create `apps.lenses` (if complex) or extend `apps.catalog`.
    *   Models: `LensType` (Single Vision, Bifocal, Zero Power), `LensCoating` (Blue-cut, Anti-glare).
    *   Update Product Detail: Select Frame Color -> Select Lens Type -> Add to Cart.
    *   Price calculation logic (`Base Frame Price` + `Lens Price`).

---

## ⏳ Task 2.4: Checkout Flow (Cash on Delivery) [PENDING]
*   **Goal:** Convert Cart into a confirmed Order.
*   **Sub-tasks:**
    *   Create `apps.orders`.
    *   Address Form (Shipping Details).
    *   Checkout View: Summary + Confirm Button.
    *   Order Model creation (`Order`, `OrderItem`).
    *   Stock deduction logic.

---

## ⏳ Task 2.5: User Order History [PENDING]
*   **Goal:** Allow users to track status.
*   **Sub-tasks:**
    *   `My Orders` page in Profile.
    *   Admin Order Management (Change status: Pending -> Processing -> Shipped).

---

## ⏳ Task 2.6: Search Functionality [PENDING]
*   **Goal:** Find products quickly.
*   **Sub-tasks:**
    *   Search bar in Navbar.
    *   `search_results` view filtering by Name, Description, and Category.
