# Phase 3 Implementation Plan: Advanced Optical Features

**Goal:** Implement advanced optical features including prescription management, online payments, appointment booking, and virtual try-on.

## 📋 Roadmap

### Task 3.1: Prescription Management (Refinement & Integration)
- [x] **Review:** Analyze existing `prescriptions` app.
- [x] **Feature:** Allow users to upload Rx images or enter values (OD/OS/Cyl/Axis/Add).
- [x] **Integration:** Link Prescription to Cart Item / Order Line Item.
- [x] **Validation:** Ensure prescription data is valid.
- [x] **Admin:** View and verify prescriptions in Django Admin.

### Task 3.2: Online Payments
- [x] **App:** Create/Configure `backend/apps/billing` (or similar).
- [x] **Integration:** Integrate Stripe (Skipped/Mocked for Development).
- [x] **Checkout:** Update checkout flow to include payment step.
- [x] **Webhooks:** Handle payment success/failure webhooks (N/A for Mock).

### Task 3.3: Appointment Booking
- [x] **App:** Create `backend/apps/appointments`.
- [x] **Models:** `Appointment` (User, Date, Time, Store/Location, Status).
- [x] **Views:** Booking form, User's appointment history.
- [x] **Admin:** Calendar view (optional) or list view to manage slots.

### Task 3.4: Virtual Try-On (Basic)
- [x] **Frontend:** Implement a simple webcam overlay or image upload feature in Product Detail page.
- [x] **Logic:** Client-side JS to overlay glasses frame on user's face (using simple SVG/Image positioning or a library if simple enough).

## 🛠️ Execution Steps

1.  **Analyze & Finalize Prescriptions (Task 3.1)**
    -   Check `models.py` for completeness.
    -   Check `views.py` vs `forms.py`.
    -   Ensure UI exists.

2.  **Payments (Task 3.2)**
    -   Set up `Billing` app.
    -   Mock payment flow for development.

3.  **Appointments (Task 3.3)**
    -   Scaffold app.
    -   Implement Booking Logic.

4.  **Try-On (Task 3.4)**
    -   Add "Try On" button to Product Detail.
    -   Modal with camera feed.
