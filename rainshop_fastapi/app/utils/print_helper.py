# from escpos.printer import Bluetooth #hanya compatible di LINUX tidak di WINDOWS
from escpos.printer import Serial
from datetime import datetime

# def print_bluetooth(bt_address: str, items: list, total: float):
#     try:
#         # Buat koneksi ke printer Bluetooth
#         p = Bluetooth(bt_address)  # ganti bt_address dgn alamat MAC printer kamu

#         p.set(align='center', width=2, height=2)
#         p.text("RainShop\n")
#         p.set(align='center', width=1, height=1)
#         p.text("Struk Pembelian\n")
#         p.text(datetime.now().strftime("%d/%m/%Y %H:%M") + "\n")
#         p.text("--------------------------------\n")
#         p.set(align='left')

#         for item in items:
#             line = f"{item['name'][:12]:12} {item['qty']:>3} x {item['price']:>5} = {item['qty'] * item['price']:>6}\n"
#             p.text(line)

#         p.text("--------------------------------\n")
#         p.set(align='right')
#         p.text(f"Total: Rp {total:,.0f}\n")
#         p.set(align='center')
#         p.text("\nTerima kasih\n")
#         p.text("www.rainshop.com\n")
#         p.cut()
#         return { "status": "success" }
#     except Exception as e:
#         return { "status": "error", "message": str(e) }

def print_serial(text: str):
    try:
        printer = Serial(devfile='COM5', baudrate=9600, timeout=1)  # Ganti dengan COM port printer kamu
        printer.text(text + "\n")
        printer.cut()
        return {"status": "success", "message": "Printed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
