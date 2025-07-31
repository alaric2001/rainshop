from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean
from sqlalchemy.orm import declarative_base
from app.database import engine

Base = declarative_base()

class SalesHeader(Base):
    __tablename__ = 'sales_header'

    sales_id = Column(String(36), primary_key=True)
    sales_time = Column(DateTime, nullable=False)
    sales_no = Column(String(50), unique=True, default='TUNAI')
    sales_total = Column(Float, default=None)
    sales_paym = Column(String(20), default='TUNAI')
    totalitem = Column(String(200), default=None)

    # Relasi ke SalesLine
    #lines = relationship("SalesLine", back_populates="header", cascade="all, delete-orphan")


class SalesLine(Base):
    __tablename__ = 'sales_line'

    sales_line_id = Column(String(36), primary_key=True)
    sales_id = Column(String(36), nullable=False)
    item_id = Column(String(36), nullable=False)
    item_price = Column(Float, default=None)
    qty = Column(Integer, nullable=False)
    subtotal = Column(Float, default=None)

    # Relasi balik ke SalesHeader
    #header = relationship("SalesHeader", back_populates="lines")
    

class VwSalesLine(Base):
    __tablename__ = "vw_sales_line"
    __table_args__ = {'autoload_with': engine}  # jika kamu pakai engine + reflect
    __mapper_args__ = {
        "primary_key": ["sales_line_id","sales_id","item_id"]  # karena view tidak punya PK, kamu harus tentukan manual
    }

    item_id = Column(String(36))
    item_name = Column(String(100))
    isactive = Column(Boolean)
    item_price = Column(Float)
    qty = Column(Integer)
    subtotal = Column(Float)
    image_id = Column(String(36))
