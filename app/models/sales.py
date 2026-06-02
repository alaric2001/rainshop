from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean, Index
from app.database import Base, engine


class SalesHeader(Base):
    __tablename__ = 'sales_header'
    __table_args__ = (
        Index('ix_tanggal', 'sales_time'),
    )

    sales_id   = Column(String(36), primary_key=True)
    sales_time = Column(DateTime, nullable=False)
    sales_no   = Column(String(50), unique=True, default='TUNAI')
    sales_total = Column(Float, default=None)
    sales_paym  = Column(String(20), default='TUNAI')
    totalitem   = Column(String(200), default=None)


class SalesLine(Base):
    __tablename__ = 'sales_line'
    __table_args__ = (
        Index('ix_item_id', 'item_id'),
    )

    sales_line_id = Column(String(36), primary_key=True)
    sales_id      = Column(String(36), nullable=False)
    item_id       = Column(String(36), nullable=False)
    item_price    = Column(Float, default=None)
    qty           = Column(Integer, nullable=False)
    subtotal      = Column(Float, default=None)


class VwSalesLine(Base):
    __tablename__ = "vw_sales_line"
    __table_args__ = {'autoload_with': engine}
    __mapper_args__ = {
        "primary_key": ["sales_line_id", "sales_id", "item_id"]
    }

    item_id    = Column(String(36))
    item_name  = Column(String(100))
    isactive   = Column(Boolean)
    item_price = Column(Float)
    qty        = Column(Integer)
    subtotal   = Column(Float)
    image_id   = Column(String(36))
