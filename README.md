<div align="center">

# 📦 StockFlow - Inventory Management System

**Backend Engineering Case Study Submission**

> A backend system to manage products, warehouses, inventory, and low-stock alerts for B2B SaaS applications.

</div>

---

# 🧠 Overview

StockFlow enables businesses to:

* Manage products across multiple warehouses
* Track inventory levels
* Monitor stock movements
* Generate intelligent low-stock alerts

This project demonstrates:

* Debugging production issues
* Designing scalable database schema
* Implementing business-driven APIs

---

# ⚙️ Tech Stack

* Python
* Flask
* SQLAlchemy
* SQLite

---

# 🚀 Quick Start

```bash
pip install flask flask_sqlalchemy
python app.py
```

Initialize DB:

```
GET /init
```

---

# 🧩 Part 1: Code Review & Debugging

## 🔍 Issues, Root Cause & Impact

| Issue                         | Root Cause                               | Production Impact                 |
| ----------------------------- | ---------------------------------------- | --------------------------------- |
| No transaction handling       | Separate commits for product & inventory | Partial data, inconsistent system |
| SKU uniqueness not enforced   | No constraint or pre-check               | Duplicate products                |
| Price not handled as decimal  | Stored as float                          | Financial calculation errors      |
| No input validation           | Missing field checks                     | Garbage data                      |
| No error handling             | Unhandled DB exceptions                  | API crashes                       |
| No foreign key validation     | Warehouse not verified                   | Orphan records                    |
| Wrong product-warehouse model | Assumes single warehouse                 | Not scalable                      |
| No idempotency                | No request deduplication                 | Duplicate entries                 |

---

## ✅ Fixes Implemented (Aligned with Code)

### 1. Input Validation

* Ensures required fields (`name`, `sku`, `price`)
* Prevents invalid data entering system

---

### 2. SKU Uniqueness Enforcement

* Checked before insert
* Avoids duplicate product entries

---

### 3. Price Handling Using Decimal

* Used `Decimal` instead of float
* Ensures accurate financial calculations

---

### 4. Optional Warehouse Validation

* Inventory created only if warehouse provided
* Supports flexible workflows

---

### 5. Transaction Management (Key Fix)

* Used:

```python
db.session.flush()
db.session.commit()
```

✔ Ensures:

* Atomic operation
* No partial data

---

### 6. Product Creation + Flush

* `flush()` used to get product ID before commit
* Required for linking inventory

---

### 7. Conditional Inventory Creation

* Product can exist without inventory
* Matches real-world workflow

---

### 8. Error Handling

* Try/except with rollback
* Prevents crashes and ensures stability

---

#  Part 2: Database Design
SQL CODE File :
https://drive.google.com/file/d/1ekc4KBQcpp5i75xF7LClaeX0sAHRkQTS/view?usp=sharing

SQL RESULTS: https://drive.google.com/drive/folders/1KkNXtmcmrotIi2jBcp_VMTkKgiMIJavU?usp=sharing

## 📊 Schema

```
Company ──< Warehouse
Company ──< Product ──< Inventory
                       └── InventoryMovement
Product ──< SupplierProduct >── Supplier
```

---

## 🧠 Design Decisions

* **Inventory Table**

  * Supports many-to-many (product ↔ warehouse)

* **InventoryMovement**

  * Tracks stock changes (sales, purchase)
  * Used for analytics

* **Supplier Mapping**

  * Enables supplier lookup

* **Unique SKU**

  * Prevents duplicates

* **Decimal Price**

  * Avoids precision issues

---

## ❓ Requirement Gaps Identified

* Multiple suppliers per product?
* Need authentication?
* Reserved stock required?
* Bundle product handling?
* Expected system scale?

---

# ⚠️ Assumptions

* Threshold stored in product
* Recent sales = last 30 days
* One supplier returned
* No sales → no alert
* SQLite used for simplicity

---

# 🔌 Part 3: Low Stock Alerts API

## 📡 Endpoint

```
GET /api/companies/{company_id}/alerts/low-stock
```

---

## ⚙️ Logic

* Include only products:

  * With recent sales
  * Stock ≤ threshold

* Compute:

  * Average daily sales
  * Days until stockout

* Include:

  * Product
  * Warehouse
  * Supplier

---

## 📦 Sample Response

```json
{
  "alerts": [
    {
      "product_id": 1,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 1,
      "current_stock": 5,
      "threshold": 10,
      "days_until_stockout": 3,
      "supplier": {
        "id": 1,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}
```

---

# 🧠 Edge Cases Handling

| Edge Case              | Handling                              |
| ---------------------- | ------------------------------------- |
| No recent sales        | No alert generated                    |
| Avg daily sales = 0    | Returns `None`, avoids division error |
| No supplier            | Returns `null`                        |
| Multiple warehouses    | Evaluated separately                  |
| No products/warehouses | Returns empty list                    |
| Invalid input          | Returns error response                |

---

# 🧪 Testing Checklist

* [x] Product creation works
* [x] Duplicate SKU blocked
* [x] Low stock alerts correct
* [x] API handles invalid input
* [x] DB initializes correctly

---

# 📈 Future Improvements

* Authentication & authorization
* Pagination
* Multiple suppliers
* PostgreSQL
* Docker
* Real-time updates

---

# 💡 Approach Summary

* Focused on **clarity + correctness**
* Avoided over-engineering
* Covered **real-world scenarios**
* Designed **scalable base system**

---

# 👨‍💻 Author

**Abhishek Dani**

---

<div align="center">

🚀 Backend Engineering Case Study Submission

</div>
