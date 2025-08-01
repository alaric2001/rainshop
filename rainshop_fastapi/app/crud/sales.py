import traceback
from sqlalchemy import text,delete
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
    rekord = None
    sales_no = None
    if frm.sales_id:
            sales_id=frm.sales_id
            
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

    updateHeader=False
    if sales_id==frm.sales_id:
        rekord = db.query(models.SalesHeader).filter_by(sales_id=frm.sales_id).first()
        if rekord:
            db.execute(
                delete(models.SalesLine).where(models.SalesLine.sales_id == sales_id)
            )
            updateHeader=True

    print('updateHeader : ',updateHeader)
    if updateHeader==True:
        rekord.sales_time = moment.now().date
        rekord.sales_total=sales_total
        rekord.sales_paym = frm.sales_paym
        rekord.totalitem = frm.totalitem
        sales_no= rekord.sales_no
    else:        
        sales_no = str(get_max_sales_no(db))
        header = schemas.sales.SalesHeaderCreate (
            sales_time = moment.now().date,
            sales_id = sales_id,
            sales_no = sales_no,
            sales_total=sales_total,
            sales_paym = frm.sales_paym,
            totalitem = frm.totalitem
        )
        objHeader = models.SalesHeader(**header.dict())
        db.add(objHeader)

    db.bulk_insert_mappings(models.SalesLine, objLines)
    db.commit()
    # db.refresh()

    return { "status": True , "sales_no": sales_no, "sales_id": sales_id }
 except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=f"Error saat Create sales: {str(e)}")

