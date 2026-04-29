# 📦 StockFlow - Backend Engineering Assessment

This repository contains my solution to the Backend Engineering Intern assessment.  
The project simulates a **B2B SaaS Inventory Management System** supporting multi-warehouse operations, supplier management, and low-stock alerting.

---

# 🚀 Features

- ✅ Product creation with validation and transactional integrity
- ✅ Multi-warehouse inventory management
- ✅ Supplier integration for reordering
- ✅ Inventory audit logging support
- ✅ Low-stock alert API with business logic
- ✅ Stockout prediction based on sales data

---

# 🏗️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Other:** PyMySQL

---

# 🧠 Key Concepts Implemented

### 🔹 1. Transaction Management
Ensures atomic operations during product creation to prevent partial data inconsistencies.

### 🔹 2. Multi-Tenant Design
Schema supports multiple companies with isolated data using `company_id`.

### 🔹 3. Data Integrity
- Unique SKU enforcement
- Foreign key constraints
- Input validation

### 🔹 4. Scalable Database Design
- Separate inventory table for flexibility
- Inventory logs for auditability
- Many-to-many supplier mapping

### 🔹 5. Business Logic in API
Low-stock alerts consider:
- Product thresholds
- Recent sales activity
- Multi-warehouse inventory
- Supplier details

---

# 📂 Project Structure

backend/
│
├── app.py # Entry point
├── database.py # DB connection
├── models.py # ORM models
├── routes/
│ └── alerts.py # Low stock API
└── requirements.txt
