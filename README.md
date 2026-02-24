# Full-Stack E-commerce Web Application (Python & Django)

A robust, production-ready E-commerce solution developed using the **Django MVC Framework**. This project features a secure user authentication system, relational database management, and a dynamic shopping cart architecture designed for scalability and performance.

**Project Theme:** Corporate Teal & Modern Orange.

---

## Project Visuals
| Home Page | Shopping Cart | Admin Dashboard |
|---|---|---|
| ![Home](https://via.placeholder.com/400x250?text=Home+Page+Screenshot) | ![Cart](https://via.placeholder.com/400x250?text=Cart+Page+Screenshot) | ![Admin](https://via.placeholder.com/400x250?text=Django+Admin+Screenshot) |
*(Note: Replace the placeholder links with actual screenshots from your project once uploaded to GitHub)*

---

## Technical Highlights & Features
* **User Authentication System:** Secure registration, login, and logout functionality using Django’s built-in `auth` system.
* **Dynamic Inventory Management:** Full CRUD (Create, Read, Update, Delete) capabilities via the Django Admin Dashboard.
* **Optimized Shopping Cart:** Per-user cart management with real-time quantity updates and session-based persistence.
* **Persistent Order History:** Snapshot-based order processing ensuring data integrity (capturing price at the time of purchase).
* **Global State Management:** Integrated a custom **Context Processor** to handle cart counts across all UI templates efficiently.

---

## Engineering Challenges & Solutions

### **Challenge 1: Optimizing UI Performance (Redundant Database Queries)**
* **Issue:** The "Cart Count" in the navigation bar was causing redundant queries on every page load, slowing down the application.
* **Solution:** Engineered a **Custom Context Processor** to fetch the cart count globally. This reduced code duplication and centralized the logic, improving overall application performance.

### **Challenge 2: Ensuring Data Integrity in Order History**
* **Issue:** If a product's price changed after a purchase, the user’s order history would show incorrect data if linked directly to the Product model.
* **Solution:** Developed an `OrderItem` model that captures a **snapshot** of the product name and price at the exact moment of checkout, ensuring accurate historical financial records.

---

##  System Architecture
```text
E-commerce-website/
├── manage.py                 # Project entry point
├── requirements.txt          # Production dependencies (Django, Pillow)
├── media/                    # Dynamic user-uploaded media (Product images)
├── ecommerce/                # Core Configuration (Settings, URLs, WSGI)
└── store/                    # Business Logic App
    ├── models.py             # Database Schema (Relational SQL)
    ├── views.py              # Controller Logic (Function-Based Views)
    ├── context_processors.py # Global Logic (Cart management)
    ├── static/               # Assets (CSS Variables, DOM Manipulation JS)
    └── templates/            # UI Layer (Base Layouts, Feature Templates)