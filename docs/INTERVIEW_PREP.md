# Prime Optical Vision - Interview Preparation Guide

This document provides a comprehensive deep-dive into the technical architecture, design decisions, technology stack, and alternatives considered for the Prime Optical Vision project. It is designed to help you confidently answer interview questions regarding *why* specific choices were made.

---

## 1. Project Overview & Architecture

### **Architecture: Monolithic (Django)**
The project follows a **Monolithic Architecture** using the Django framework.
- **Why?** Rapid development, simplicity, and tightness of integration. E-commerce requires complex relationships (Users ↔ Orders ↔ Payments ↔ Products), and Django's ORM handles these joins efficiently in a single codebase.
- **Alternative:** Microservices (Separating Auth, Product Service, Order Service).
  - *Comparison:* Microservices would add massive complexity (API Gateways, inter-service communication overhead, eventual consistency issues) which is overkill for a mid-sized e-commerce store.

### **Design Pattern: MVT (Model-View-Template)**
Django's standard pattern.
- **Model:** Defines data aggregation and database structure (ORM).
- **View:** Handles business logic and request processing.
- **Template:** Presentation layer (HTML/CSS).
- *Interview Note:* This is similar to MVC (Model-View-Controller), where View ≈ Controller and Template ≈ View.

---

## 2. Technology Stack & Justifications

### **A. Backend: Python & Django**
- **Why Python?** Extremely readable, huge ecosystem for Data Science (crucial for future AI recommendation features), and strictly typed via libraries.
- **Why Django?** "Batteries included." It provides Auth, Admin Panel, and ORM out-of-the-box. Security features (CSRF, SQL Injection protection) are built-in, which is vital for e-commerce.
- **Alternatives:**
  - *Node.js (Express):* Faster I/O for real-time chat, but requires manually stitching together DB drivers, ORMs, and security middlewares.
  - *Go (Golang):* Higher performance, but slower development speed and fewer pre-built e-commerce libraries.

### **B. Database: MySQL**
- **Why?** ACID compliance (Atomicity, Consistency, Isolation, Durability) is non-negotiable for financial transactions (orders/payments). It is battle-tested and widely supported.
- **Alternatives:**
  - *PostgreSQL:* Technically superior in handling complex queries and JSON, but MySQL is often the default infrastructure choice for many legacy hosting providers.
  - *MongoDB (NoSQL):* Good for flexible product attributes, but **BAD** for strict relational data like "Orders must belong to a valid User." Ensuring consistency in NoSQL is harder.

### **C. Frontend: HTML5, CSS3, Vanilla JS + Three.js**
- **Why Vanilla CSS?** Full control over "Glassmorphism" aesthetics without fighting framework overrides.
- **Why Three.js (Virtual Try-On)?** The industry standard for WebGL. It allows rendering 3D models directly in the browser without plugins.
- **Why MediaPipe (Face Tracking)?** Google's Machine Learning solution runs client-side (in the browser), meaning nearly zero latency and high privacy (video isn't sent to the server).
- **Alternatives:**
  - *React/Vue:* Would provide a smoother "App-like" feel (SPA), but hurts SEO (Search Engine Optimization) unless using Server-Side Rendering (Next.js). Django Templates serve simple Server-Side HTML which Google indexes perfectly.

### **D. Infrastructure: Docker**
- **Why?** "It works on my machine." Docker ensures the app runs exactly the same on your laptop, the client's laptop, and the AWS server.
- **Alternatives:**
  - *Virtual Machines (VMs):* Much heavier, slower to boot.
  - *Manual Config:* Error-prone ("python version mismatch" is a classic nightmare).

---

## 3. Project Modules & Workflow

### **A. Core Modules**

1.  **Authentication Module (`apps/accounts`)**
    *   **Role:** Manages user identity, registration, login (including Google OAuth), and profile management.
    *   **Tech:** `django.contrib.auth`, `django-allauth`.

2.  **Catalog Module (`apps/catalog`)**
    *   **Role:** Handles Products, Categories, Brands, and Inventory. Supports variants (e.g., Color/Size) and search.
    *   **Tech:** Custom Models with Slug fields for SEO-friendly URLs.

3.  **Virtual Try-On Module (`apps/virtual_tryon`)**
    *   **Role:** The unique selling point. Handles 3D model storage, face data caching, and serves the AR interface.
    *   **Tech:** `SpectacleFrame` model linked to Catalog, MediaPipe integration.

4.  **Cart & Order Module (`apps/orders`)**
    *   **Role:** Manages the shopping session (Cart) and permanent transaction records (Orders).
    *   **Tech:** Session-based cart (for guest users) -> Database Order (upon checkout).

5.  **Payment Module (`apps/payments`)**
    *   **Role:** Interacts with Razorpay Gateway to securely process money.
    *   **Tech:** `razorpay` Python SDK, Webhooks (optional/future).

### **B. End-to-End User Workflow**

1.  **Discovery:** User lands on Home -> Browes Catalog (Filtered by Category/Brand).
2.  **Evaluation (Try-On):**
    *   User clicks "Try On" -> Camera activates.
    *   JavaScript fetches 3D model -> Aligns to face -> User sees themselves.
3.  **Decision:** User adds item to **Cart** (Session storage).
4.  **Checkout:**
    *   User proceeds to Checkout.
    *   **Auth Check:** If not logged in -> Redirect to Login/Signup -> Redirect back.
    *   **Address Input:** User selects shipping address.
5.  **Payment:**
    *   Backend creates Order (Status: Pending).
    *   Razorpay Popup opens -> User pays.
    *   Razorpay returns `payment_id` + `signature`.
    *   Backend verifies signature -> Updates Order (Status: Paid).
6.  **Fulfillment:** User sees "Success" page. Email notification sent.

---

## 4. Key Feature Deep-Dives

### **Feature 1: Virtual Try-On (The "Star" Feature)**

#### **A. How it works (High Level)**
1.  **Face Mesh:** MediaPipe detects 468 landmarks on the face (JavaScript).
2.  **PnP Algorithm:** We calculate the "Pose" (Rotation/Position) of the head based on the eyes and nose.
3.  **WebGL Overlay:** Three.js places a `.glb` 3D model on that calculated position.
4.  **Smoothing:** An Exponential Moving Average (EMA) filter is applied to prevent the glasses from "jittering".

#### **B. The Math Behind It (Technical)**
For the interview, explaining the math shows depth.

**1. Inter-Pupillary Distance (IPD) Scaling:**
*   **Concept:** We need to know how "big" the user's face is in the 3D world.
*   **Formula:** `Scale = (Distance(LeftEye, RightEye) / Reference_IPD) * Tuning_Factor`
    *   We measure the pixel distance between landmarks `33` (Left Eye) and `263` (Right Eye).
    *   We divide this by a reference constant (approx 63mm in 3D units).
    *   This gives us a scale factor to grow/shrink the glasses.

**2. Head Pose Estimation (Rotation Matrix):**
*   **Concept:** Determining where the face is looking (Yaw, Pitch, Roll).
*   **Vectors:**
    *   **Right Vector ($X$):** `Vector(LeftEye) - Vector(RightEye)` (normalized).
    *   **Up Vector ($Y$):** `Vector(MidEyes) - Vector(Chin)` (normalized).
    *   **Forward Vector ($Z$):** The *Cross Product* of $X$ and $Y$ ($X \times Y$). This creates a vector pointing strictly out of the face.
*   **Three.js Implementation:** We create a `Matrix4` basis using these three vectors. The glasses are then applied to this matrix, causing them to rotate exactly with the head.

**3. Smoothing (EMA - Exponential Moving Average):**
*   **Problem:** Webcam noise makes landmarks shake by 1-2 pixels every frame.
*   **Formula:** $P_{new} = \alpha \cdot P_{measured} + (1 - \alpha) \cdot P_{prev}$
    *   $\alpha$ (Alpha) is the smoothing factor (e.g., 0.5).
    *   If $\alpha$ is low (0.1), movement is very smooth but slow (laggy).
    *   If $\alpha$ is high (0.9), movement is responsive but jittery.
    *   We use ~0.5 for a balance.

---

## 5. Comparisons & Trade-offs

| Feature | Choice in Project | Alternative | Why we chose this? |
| :--- | :--- | :--- | :--- |
| **Rendering** | Server-Side (Django) | Client-Side (React/SPA) | Better SEO, simpler Authentication flow. |
| **Async Tasks** | Synchronous (Simple) | Celery/Redis | Kept it simple for deployment. If we had 1M emails to send, we'd add Celery. |
| **Search** | Database  `IContains` | Elasticsearch | Database search is "good enough" for <10,000 products. Elasticsearch is expensive and complex to maintain. |
| **Images** | Local Filesystem | AWS S3 / Cloudinary | Local is free and easiest for MVPs (Minimum Viable Products). Production should move to S3. |

---

## 6. Deployment Flow (CI/CD Concepts)
We use a **Containerized Workflow**:
1.  **Code:** Developer commits to Git.
2.  **Build:** Docker builds an image containing the OS, Python, and dependencies.
3.  **Run:** The `docker-compose` spins up the Web Container (Django) and the DB Container (MySQL) inside a private network.
4.  **benefit:** If the database crashes, it restarts automatically (`restart: always`). Data is persisted in Volumes so it isn't lost on restart.
