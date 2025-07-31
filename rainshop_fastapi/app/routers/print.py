from fastapi import APIRouter, Body
from typing import Optional, List, Any
from pydantic import BaseModel
from app.utils.print_helper import print_serial
# from app.utils.print_helper import print_serial, print_blutooth
from escpos.printer import Serial
import moment

import usb.core
import usb.util

import usb.backend.libusb1
from escpos.printer import Usb
from usb.backend import libusb1

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

@router.post("/print-debug")
async def receive_any_json(payload: Any = Body(...)):
    print("Received payload:", payload)  # Debug log
    return {"received": payload}

@router.post("/print-struk")
async def print_struk(data: SalesForm):
    printer = Serial(devfile='USB003', baudrate=9600, timeout=1)  # Ganti dengan COM port printer kamu
    
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
    printer.text(now.format("ddd, DD MMM YYYY HH:mm"))
    printer.cut()    # lakukan konversi Data menjadi text yg siap cetak
    return {"status": "success", "message": "Printed successfully"}


@router.post("/print-test")
async def print_test(data: PrintData):


    # Cari device printer
    # dev = usb.core.find(find_all=True)
    # backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\Users\\testl\\Downloads\\drive-download-20250731T143303Z-1-001\\libusb-1.0.29\\VS2022\\MS64\\dll\\libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\Users\\testl\\Documents\\RainShop\\rainshopGitHub\\rainshop\\rainshop_fastapi\\libusb-1.0.29\VS2022\\MS64\\dll\\libusb-1.0.dll")
    dev = usb.core.find(backend=backend, find_all=True)

    for d in dev:
        # print(f"Vendor ID: {hex(d.idVendor)}, Product ID: {hex(d.idProduct)}")
        print(f"Vendor ID: {hex(d.idVendor)}, Product ID: {hex(d.idProduct)}")

    now = moment.now()

    # printer = Serial(devfile='USB003')  # Ganti dengan COM port printer kamu
    
    try:
        printer = Usb(0x0483, 0x70b, backend=backend)  # Gunakan vendor & product ID yang kamu temukan
    except Exception as e:
        return {"status": "error", "message": f"Gagal konek ke printer: {str(e)}"}

    device = usb.core.find(idVendor=0x0483, idProduct=0x070b, backend=backend)
    if device is None:
        print("Printer not found")
    else:
        print("Printer found!")
        print(f"Manufacturer: {usb.util.get_string(device, device.iManufacturer)}")

    # Header
    printer.set(align='center', bold=True, width=2, height=2)
    printer.text(center_text("RAINSHOP", bold=True, double_size=True))
    printer.text(center_text("Toko Pernak-Pernik",bold=True, double_size=False))
    printer.set(align='center', bold=False)
    printer.text("Jl.Rawa Pulo No 101 RT01/08\n")
    printer.text("Ds.RawaPanjang - Bojong Gede\n")
    printer.text(line_separator)
    printer.text(data.text)

    return {"status": "success", "message": "Printed successfully"}
