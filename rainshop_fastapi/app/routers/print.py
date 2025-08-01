import moment
from fastapi import APIRouter, Body
from typing import Optional, List, Any
from pydantic import BaseModel

import usb.core
import usb.util
import usb.backend.libusb1
from escpos.printer import Usb,Serial
# from usb.backend import libusb1
from app.config import PRINTER_LIBUSB_PATH  # Sesuaikan dengan path config.py kamu

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

def format_harga(qty: int, price: float, subtotal: float, width=32):
    harga = (f"{price:,.0f}"+" x "+str(qty)).ljust(width - 10)
    subtotal = f"{subtotal:,.0f}".rjust(10)
    return f"{harga}{subtotal}\n"

def format_total(label: str, total: float):
    return f"{label.upper():<20}{'Rp':>2}{f'{total:,.0f}'.rjust(10)}\n"



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

    # backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\Users\\testl\\Documents\\RainShop\\rainshopGitHub\\rainshop\\rainshop_fastapi\\libusb-1.0.29\VS2022\\MS64\\dll\\libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: PRINTER_LIBUSB_PATH)
    # # Cari device printer
    # dev = usb.core.find(backend=backend, find_all=True)
    # for d in dev:
    #     print(f"Vendor ID: {hex(d.idVendor)}, Product ID: {hex(d.idProduct)}")

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

    
    now = moment.now()
    # Header
    printer.set(align='center', bold=True, width=2, height=2)
    printer.text("RAINSHOP\n")
    printer.set(align='center', bold=True)
    printer.text("Toko Pernak-Pernik\n")
    printer.set(align='center', bold=False)
    printer.text("Jl.Rawa Pulo No 101 RT01/08\n")
    printer.text("Ds.RawaPanjang - Bojong Gede\n")
    printer.text("--------------------------------\n")
    # Detail Item
    printer.set(align='left')
    for row in data.lines:
        namabarang = f"{row.item_name}\n"
        printer.text(namabarang)
        qtyHarga = format_harga(row.qty,row.item_price,row.subtotal)
        printer.text(qtyHarga)

    # Total
    printer.text("--------------------------------\n")
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

    printer.text(f"{'Cara Bayar':<20}{data.sales_paym:<6}{'------':>10}\n")
    printer.text(format_total("Total Bayar",data.paid_amount))
    printer.text(format_total("Uang Kembali",data.change_amount))

    # Footer
    printer.set(align='center')
    printer.text("\n")
    printer.text(now.format("ddd, DD MMM YYYY HH:mm"))
    printer.text("Terima Kasih\n\n")
    printer.cut()
    return {"status": "success", "message": "Printed successfully"}


@router.get("/print-test")
async def print_test():
    now = moment.now()
    data = {
        "sales_total": 47000,
        "paid_amount": 50000,
        "change_amount": 3000,
        "sales_paym": "TUNAI",
        "lines": [
            {"item_name": "DIY Poke Painting", "item_price": 8500, "qty": 2, "subtotal": 17000},
            {"item_name": "DIY Puzzle Form Besar", "item_price": 25000, "qty": 1, "subtotal": 25000}
        ]
    }

    # backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\Users\\testl\\Documents\\RainShop\\rainshopGitHub\\rainshop\\rainshop_fastapi\\libusb-1.0.29\VS2022\\MS64\\dll\\libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: PRINTER_LIBUSB_PATH)
    
    # Cari device printer
    dev = usb.core.find(backend=backend, find_all=True)
    for d in dev:
        print(f"Vendor ID: {hex(d.idVendor)}, Product ID: {hex(d.idProduct)}")

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
    printer.text("RAINSHOP\n")
    printer.set(align='center', bold=True)
    printer.text("Toko Pernak-Pernik\n")
    printer.set(align='center', bold=False)
    printer.text("Jl.Rawa Pulo No 101 RT01/08\n")
    printer.text("Ds.RawaPanjang - Bojong Gede\n")
    printer.text("--------------------------------\n")
    
    # Detail Item
    printer.set(align='left')
    for row in data["lines"]:
        printer.text(f"{row['item_name']}\n")
        printer.text(format_harga(row['qty'], row['item_price'], row['subtotal']))

    # Total
    printer.text("--------------------------------\n")
    printer.set(bold=True, align='right')
    printer.text(format_total("Total Belanja", data["sales_total"]))
    printer.text(f"{'Cara Bayar':<20}{data['sales_paym']:<6}{'------':>10}\n")
    printer.text(format_total("Total Bayar", data["paid_amount"]))
    printer.text(format_total("Uang Kembali", data["change_amount"]))

    # Footer
    printer.set(align='center')
    printer.text("\n")
    printer.text(now.format("ddd, DD MMM YYYY HH:mm"))
    printer.text("Terima Kasih\n\n")
    printer.cut()

    return {"status": "success", "message": "Printed successfully"}