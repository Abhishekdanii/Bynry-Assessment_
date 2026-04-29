from flask import Blueprint, jsonify
from sqlalchemy import text
from database import SessionLocal

alerts_bp = Blueprint("alerts", __name__)


def estimate_stockout_days(db, product_id):
    """
    Estimate how many days before stock runs out
    """

    avg_sales = db.execute(text("""
        SELECT AVG(quantity)
        FROM sales
        WHERE product_id = :pid
    """), {"pid": product_id}).scalar()

    if not avg_sales or avg_sales == 0:
        return None

    current_stock = db.execute(text("""
        SELECT SUM(quantity)
        FROM inventory
        WHERE product_id = :pid
    """), {"pid": product_id}).scalar()

    if not current_stock:
        return None

    return int(current_stock / avg_sales)


@alerts_bp.route('/api/companies/<company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):

    db = SessionLocal()

    try:
        query = text("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.sku,
            w.id AS warehouse_id,
            w.name AS warehouse_name,
            i.quantity AS current_stock,
            p.low_stock_threshold AS threshold,
            s.id AS supplier_id,
            s.name AS supplier_name,
            s.contact_email
        FROM products p
        JOIN inventory i ON p.id = i.product_id
        JOIN warehouses w ON i.warehouse_id = w.id
        LEFT JOIN product_suppliers ps ON p.id = ps.product_id
        LEFT JOIN suppliers s ON ps.supplier_id = s.id
        WHERE p.company_id = :company_id
          AND i.quantity < p.low_stock_threshold
          AND EXISTS (
              SELECT 1 FROM sales sa
              WHERE sa.product_id = p.id
              AND sa.created_at >= NOW() - INTERVAL 30 DAY
          )
        """)

        results = db.execute(query, {"company_id": company_id})

        alerts = []

        for row in results:
            alerts.append({
                "product_id": row.product_id,
                "product_name": row.product_name,
                "sku": row.sku,
                "warehouse_id": row.warehouse_id,
                "warehouse_name": row.warehouse_name,
                "current_stock": row.current_stock,
                "threshold": row.threshold,
                "days_until_stockout": estimate_stockout_days(db, row.product_id),
                "supplier": {
                    "id": row.supplier_id,
                    "name": row.supplier_name,
                    "contact_email": row.contact_email
                }
            })

        return {
            "alerts": alerts,
            "total_alerts": len(alerts)
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        db.close()
