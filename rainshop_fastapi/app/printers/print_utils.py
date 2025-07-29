from escpos.printer import Serial

def print_receipt(text: str):
    try:
        printer = Serial(devfile='COM5', baudrate=9600, timeout=1)  # Ganti dengan COM port printer kamu
        printer.text(text + "\n")
        printer.cut()
        return {"status": "success", "message": "Printed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
