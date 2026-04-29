"""
Setup test data for StockFlow API testing.
Run this file to populate database with sample data.
"""

from datetime import datetime, timedelta
from decimal import Decimal

from app import (
    app,
    db,
    Company,
    Warehouse,
    Product,
    Inventory,
    InventoryMovement,
    Supplier,
    SupplierProduct,
)


def setup_test_data():
    with app.app_context():

        print("Clearing old data...")
        db.drop_all()
        db.create_all()
        print("[OK] Database ready")

        # =========================
        # COMPANY
        # =========================
        print("\nCreating company...")
        company = Company(name="Demo Company")
        db.session.add(company)
        db.session.flush()

        # =========================
        # WAREHOUSES
        # =========================
        print("Creating warehouses...")
        w1 = Warehouse(company_id=company.id, name="Main Warehouse")
        w2 = Warehouse(company_id=company.id, name="Secondary Warehouse")

        db.session.add_all([w1, w2])
        db.session.flush()

        # =========================
        # PRODUCTS
        # =========================
        print("Creating products...")
        p1 = Product(
            company_id=company.id,
            name="Widget A",
            sku="WID-001",
            price=Decimal("100.00"),
            low_stock_threshold=20
        )

        p2 = Product(
            company_id=company.id,
            name="Gadget B",
            sku="GAD-001",
            price=Decimal("50.00"),
            low_stock_threshold=30
        )

        db.session.add_all([p1, p2])
        db.session.flush()

        # =========================
        # INVENTORY
        # =========================
        print("Creating inventory...")
        i1 = Inventory(product_id=p1.id, warehouse_id=w1.id, quantity=5)   # LOW STOCK
        i2 = Inventory(product_id=p1.id, warehouse_id=w2.id, quantity=50)  # OK
        i3 = Inventory(product_id=p2.id, warehouse_id=w1.id, quantity=10)  # LOW STOCK

        db.session.add_all([i1, i2, i3])
        db.session.flush()

        # =========================
        # SUPPLIERS
        # =========================
        print("Creating suppliers...")
        s1 = Supplier(
            company_id=company.id,
            name="ABC Supplier",
            contact_email="abc@supplier.com"
        )

        db.session.add(s1)
        db.session.flush()

        # =========================
        # SUPPLIER-PRODUCT LINK
        # =========================
        sp1 = SupplierProduct(
            supplier_id=s1.id,
            product_id=p1.id
        )

        db.session.add(sp1)
        db.session.flush()

        # =========================
        # SALES (Inventory Movement)
        # =========================
        print("Creating sales data...")
        now = datetime.utcnow()

        sales = [
            InventoryMovement(
                product_id=p1.id,
                warehouse_id=w1.id,
                movement_type="sale",
                quantity=-2,
                created_at=now - timedelta(days=10)
            ),
            InventoryMovement(
                product_id=p1.id,
                warehouse_id=w1.id,
                movement_type="sale",
                quantity=-3,
                created_at=now - timedelta(days=5)
            ),
            InventoryMovement(
                product_id=p2.id,
                warehouse_id=w1.id,
                movement_type="sale",
                quantity=-5,
                created_at=now - timedelta(days=3)
            ),
        ]

        db.session.add_all(sales)

        # =========================
        # COMMIT
        # =========================
        db.session.commit()

        print("\n" + "=" * 50)
        print("TEST DATA CREATED SUCCESSFULLY")
        print("=" * 50)

        print("\nTry this API:")
        print("http://127.0.0.1:5000/api/companies/1/alerts/low-stock")


if __name__ == "__main__":
    setup_test_data()
