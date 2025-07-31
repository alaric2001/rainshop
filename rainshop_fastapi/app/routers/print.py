from fastapi import APIRouter, Body
from typing import Optional, List, Any
from pydantic import BaseModel
from app.utils.print_helper import print_serial
# from app.utils.print_helper import print_serial, print_blutooth
from escpos.printer import Serial
import moment

BT_ADDRESS = '';


router = APIRouter()

class PrintData(BaseModel):
    text: str


class SalesLine(BaseModel):
    sales_line_id: Optional[str] = None
    sales_id: Optional[str] = None
    item_id: str
    item_price: float
    qty: int
    subtotal: Optional[float] = None
    item_name: str
    item_price_skrg: Optional[float] = None
    item_stock: Optional[int] = None
    isactive: Optional[bool] = None
    image_id: Optional[str] = None  

class SalesForm(BaseModel):
    sales_id: Optional[str] = None
    sales_no: Optional[str] = None
    sales_total: Optional[float] = None
    sales_paym: Optional[str] = "TUNAI"
    totalitem: Optional[str] = None
    lines: List[SalesLine] = []  



def format_item(name: str, price: float, width=32):
    nama = name.ljust(width - 12)
    harga = f"{price:,.0f}".rjust(12)
    return f"{nama}{harga}\n"

def format_harga(qty: int, price: float, width=32):
    nama = ("qty."+str(qty)).ljust(width - 12)
    harga = f"{price:,.0f}".rjust(12)
    return f"{nama}{harga}\n"

def format_total(label: str, total: float):
    return f"{label.upper():<20}{'Rp':>2}{f'{total:,.0f}'.rjust(10)}\n"

def line_separator(char='-'):
    return char * 32 + "\n"

def center_text(text: str, bold=False, double_size=False):
    # Bisa pakai tag khusus untuk ESC/POS, atau markup sendiri
    prefix = ""
    if bold: prefix += "<b>"
    if double_size: prefix += "<ds>"
    return f"{prefix}{text.center(32)}\n"



# @router.post("/print")
# def print(data: PrintData):
#     result = print_blutooth(BT_ADDRESS,data.text)
#     return result

# @router.post("/print-debug")
# async def receive_any_json(payload: Any = Body(...)):
#     print("Received payload:", payload)  # Debug log
#     return {"received": payload}

@router.post("/print-struk")
async def print_struk(data: SalesForm):
    printer = Serial(devfile='COM5', baudrate=9600, timeout=1)  # Ganti dengan COM port printer kamu
    
    now = moment.now()
    # Header
    printer.set(align='center', bold=True, width=2, height=2)
    printer.text(center_text("RAINSHOP", bold=True, double_size=True))
    printer.text(center_text("Toko Pernak-Pernik",bold=True, double_size=False))
    printer.set(align='center', bold=False)
    printer.text("Jl.Rawa Pulo No 101 RT01/08\n")
    printer.text("Ds.RawaPanjang - Bojong Gede\n")
    printer.text(line_separator)
    # Detail Item
    printer.set(align='left')
    for row in data.lines:
        printer.text(f"{row.item_name}\n")
        printer.text(format_harga(row.qty,row.subtotal))

    # Total
    printer.text(line_separator)
    printer.set(bold=True, align='right')
    printer.text(format_total("Total Belanja",data.sales_total))
    printer.text(format_total("Total Bayar",data.paid_amount))
    printer.text(format_total("Uang Kembali",data.change_amount))

    # Footer
    printer.set(align='center')
    printer.text("\n")
    printer.text("Terima Kasih\n")
    printer.text(now.format("ddd, YYYY-MM-DD HH:mm"))
    printer.cut()    # lakukan konversi Data menjadi text yg siap cetak
    return {"status": "success", "message": "Printed successfully"}


@router.post("/print-test")
async def print_struk(text: PrintData):
    now = moment.now()

    printer = Serial(devfile='COM5', baudrate=9600, timeout=1)  # Ganti dengan COM port printer kamu

    # Header
    printer.set(align='center', bold=True, width=2, height=2)
    printer.text(center_text("RAINSHOP", bold=True, double_size=True))
    printer.text(center_text("Toko Pernak-Pernik",bold=True, double_size=False))
    printer.set(align='center', bold=False)
    printer.text("Jl.Rawa Pulo No 101 RT01/08\n")
    printer.text("Ds.RawaPanjang - Bojong Gede\n")
    printer.text(line_separator)
    printer.text(text)
    printer.text(now.format("ddd, YYYY-MM-DD HH:mm"))

    return {"status": "success", "message": "Printed successfully"}
