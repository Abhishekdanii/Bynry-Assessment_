from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True)
    company_id = Column(String(36))
    name = Column(String(255))
    sku = Column(String(100))
    price = Column(DECIMAL)
    low_stock_threshold = Column(Integer)


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(String(36), primary_key=True)
    product_id = Column(String(36), ForeignKey("products.id"))
    warehouse_id = Column(String(36))
    quantity = Column(Integer)


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(String(36), primary_key=True)
    company_id = Column(String(36))
    name = Column(String(255))


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    contact_email = Column(String(255))
