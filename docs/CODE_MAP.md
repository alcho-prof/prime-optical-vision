# System Code Map & Error Traceability

| Feature Name | User-Visible Purpose | Folder Path | File Name | What This Code Does | Common Errors Seen | If Error Comes Here, Fix This |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **User Login** | Log in to the website | `backend/apps/accounts/` | `urls.py` | Routes the login URL to the view | Page not found (404) | Check `urlpatterns` for `login/` path |
| **User Login** | Log in to the website | `backend/config/settings/` | `base.py` | Configures auth backends and redirect URLs | Error "Multiple backends configured" | Specify `backend` in `login()` call or check `AUTHENTICATION_BACKENDS` |
| **Registration** | Create a new account | `backend/apps/accounts/` | `views.py` | Handles sign-up logic and auto-login | "Values mismatch", "Duplicate email" | Check `UserRegistrationForm` validation logic |
| **Registration** | Create a new account | `backend/apps/accounts/` | `forms.py` | Validates email format and password match | "Password too short", "Email exists" | Update `clean()` method in `UserRegistrationForm` |
| **User Profile** | View/Edit personal info | `backend/apps/accounts/` | `views.py` | Loads and saves user profile data | "Login required" redirect loop | Ensure `@login_required` decorator is present |
| **User Model** | Stores user data | `backend/apps/users/` | `models.py` | Defines table for Users (Email, Phone) | Migration errors, Field missing | Run `makemigrations` and `migrate` |
| **Product Catalog** | Browse products | `backend/apps/catalog/` | `models.py` | Defines Category, Product, Variant | Data not showing, Image missing | Check `is_active` flag or media folder permissions |
| **Base Template** | Main site layout | `backend/templates/` | `base.html` | Header, Footer, and Common Scripts | Nav links broken, CSS not loading | Check static file tags and `include` paths |
| **Project Config** | Global settings | `backend/config/` | `settings/base.py` | Installed apps, Database, Static files | "App not found", "Template Missing" | Check `INSTALLED_APPS` and `TEMPLATES['DIRS']` |

## Error → Fix Traceability

| Error Message / Symptom | Feature Affected | File to Check | Likely Cause | What to Change |
| :--- | :--- | :--- | :--- | :--- |
| `ValueError: You have multiple authentication backends configured...` | Registration / Login | `backend/apps/accounts/views.py` | `login()` called without backend arg when multiple exist | Add `backend='...'` argument to `login()` function call |
| `AttributeError: 'HttpResponse' object has no attribute 'is_bound'` | Automated Testing | `backend/apps/accounts/tests.py` | Test checking `response` instead of `response.context['form']` | Access form via `response.context['form']` before assertions |
| `ModuleNotFoundError: No module named 'django'` | System / Running | `requirements.txt` / Shell | Virtual environment not active | Activate venv: `source venv/bin/activate` |
| **Shopping Cart** | Manage items | `backend/apps/cart/` | `cart.py` | Session-based cart logic | Items not persisting | Check session middleware settings |
| **Lens Selection** | Choose lens type | `backend/apps/lenses/` | `models.py` | LensType model and Cart integration | Lenses not showing | Check `is_active` or template loop |
| **Variants** | Display colors | `backend/apps/catalog/` | `views.py` | ProductVariant creation | Variants missing | Create variants in Admin/Shell |
| **Checkout Flow** | Place order | `backend/apps/orders/` | `views.py` | Order Creation logic | Database error | Check model fields |
| **Order Management** | View orders | `backend/apps/orders/` | `views.py` | Admin & User views | Permission errors | Add login_required |
| **Order Admin** | Manage orders | `backend/apps/orders/` | `admin.py` | Admin configuration logic | Not showing in Admin | Register model in admin.py |
| **Basic Search** | Find products | `backend/apps/catalog/` | `views.py` | Q queries | No results | Check case sensitivity |
