from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from decimal import Decimal

app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELS (PART 2)
# =========================

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String(100))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    sku = db.Column(db.String(50), unique=True)
    price = db.Column(db.Numeric(10, 2))
    low_stock_threshold = db.Column(db.Integer, default=10)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=0)


class InventoryMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    movement_type = db.Column(db.String(50))  # sale / purchase
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))


class SupplierProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)


# =========================
# PART 1: CREATE PRODUCT API
# =========================

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Basic validation
    if not data or 'name' not in data or 'sku' not in data or 'price' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # SKU uniqueness check
        if Product.query.filter_by(sku=data['sku']).first():
            return jsonify({"error": "SKU already exists"}), 409

        # Create product
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(str(data['price'])),
            company_id=data.get('company_id', 1)
        )

        db.session.add(product)
        db.session.flush()  # get ID before commit

        # Optional inventory creation
        if 'warehouse_id' in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data.get('initial_quantity', 0)
            )
            db.session.add(inventory)

        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product_id": product.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =========================
# PART 3: LOW STOCK ALERT API
# =========================

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):

    alerts = []
    cutoff_date = datetime.utcnow() - timedelta(days=30)

    products = Product.query.filter_by(company_id=company_id).all()

    for product in products:

        inventories = Inventory.query.filter_by(product_id=product.id).all()

        for inv in inventories:

            # Get recent sales
            sales = InventoryMovement.query.filter(
                InventoryMovement.product_id == product.id,
                InventoryMovement.warehouse_id == inv.warehouse_id,
                InventoryMovement.movement_type == 'sale',
                InventoryMovement.created_at >= cutoff_date
            ).all()

            # Skip if no sales
            if not sales:
                continue

            total_sold = sum(abs(s.quantity) for s in sales)
            avg_daily_sales = total_sold / 30 if total_sold else 0

            # Check low stock
            if inv.quantity <= product.low_stock_threshold:

                days_left = int(inv.quantity / avg_daily_sales) if avg_daily_sales > 0 else None

                # Supplier info
                supplier_data = None
                sp = SupplierProduct.query.filter_by(product_id=product.id).first()

                if sp:
                    supplier = Supplier.query.get(sp.supplier_id)
                    if supplier:
                        supplier_data = {
                            "id": supplier.id,
                            "name": supplier.name,
                            "contact_email": supplier.contact_email
                        }

                alerts.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "sku": product.sku,
                    "warehouse_id": inv.warehouse_id,
                    "current_stock": inv.quantity,
                    "threshold": product.low_stock_threshold,
                    "days_until_stockout": days_left,
                    "supplier": supplier_data
                })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })


# =========================
# UTIL ROUTES
# =========================

@app.route('/')
def home():
    return {"message": "StockFlow API Running"}


@app.route('/init')
def init_db():
    db.create_all()
    return {"message": "Database initialized"}


# =========================
# RUN
# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
