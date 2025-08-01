import traceback
from sqlalchemy import text
from sqlalchemy.orm import Session, selectinload  # atau joinedload
from fastapi import HTTPException
from app import models, schemas
from typing import List, Any
import moment
import uuid

def get_max_sales_no(db: Session) -> int:
    now = moment.now()
    result = db.execute(
        text("CALL usp_sales_nomorbaru(:sales_date)"),
        {"sales_date": now.format("YYYY-MM-DD")}
    )
    row = result.mappings().fetchone()
    print ('nomor sales; ',row["sales_no"])
    return row["sales_no"]

def create_sales(db: Session, frm: schemas.sales.SalesForm ):
 try:    
    objLines=[]
    sales_total=0
    sales_id = str(uuid.uuid4())
    for row in frm.lines:
        objLines.append(schemas.SalesLineBase(
            sales_line_id=str(uuid.uuid4()),
            sales_id=sales_id,
            item_id=row.item_id,
            item_price=row.item_price,
            qty=row.qty,
            subtotal=row.subtotal
        ))
        sales_total=sales_total+row.subtotal

    header = schemas.sales.SalesHeaderCreate (
        sales_time = moment.now().date,
        sales_id = sales_id,
        sales_no = str(get_max_sales_no(db)),
        sales_total=sales_total,
        sales_paym = frm.sales_paym,
        totalitem = frm.totalitem
    )
    objHeader = models.SalesHeader(**header.dict())
    db.add(objHeader)
    db.bulk_insert_mappings(models.SalesLine, objLines)

    db.commit()
    db.refresh(objHeader)

    return { "status": True , "sales_no": header.sales_no, "sales_id": sales_id }
 except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=f"Error saat Create sales: {str(e)}")

