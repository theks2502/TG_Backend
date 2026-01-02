from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import uuid
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../public/invoice_template.jpg"))

def generate_invoice(data , amount):
    file_name = f"invoice_{uuid.uuid4().hex[:8]}.pdf"
    invoices_folder = os.path.abspath(os.path.join(BASE_DIR, "../invoices"))
    os.makedirs(invoices_folder, exist_ok=True)

    file_path = os.path.join(invoices_folder, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.drawImage(TEMPLATE_PATH, 0, 0, width=width, height=height)

    invoice_no = f"INV-{uuid.uuid4().hex[:6].upper()}"
    submitted_date = getattr(data, "submitted_at", None)
    date_text = str(submitted_date.date()) if submitted_date else "N/A"

    # USER NAME UNDER LOGO
    # c.drawString(28 * mm, 257 * mm, data.full_name)

    # INVOICE NO AND DATE
    c.drawString(149 * mm, 198 * mm, invoice_no)
    c.drawString(137 * mm, 187 * mm, date_text)

    # BILL TO NAME
    c.drawString(52 * mm, 198 * mm, data.full_name)

    # PACKAGE DETAILS
    # c.drawString(25 * mm, 185 * mm, "1 Day Adventure Trek")
    c.drawString(124 * mm, 142 * mm, "1")
    c.drawString(145 * mm, 142 * mm,str(amount+60))
    c.drawString(173 * mm, 142 * mm, str(amount+60))

    # OTHERS (UPI)
    # c.drawString(25 * mm, 172 * mm, "UPI")
    # c.drawString(170 * mm, 172 * mm, "939")

    # SUMMARY (RIGHT SIDE)
    c.drawString(170 * mm, 104 * mm, str(amount+60))   # Subtotal
    c.drawString(170 * mm, 89 * mm, "6%")     # Discount
    c.drawString(170 * mm, 71 * mm, str(amount))   # Total

    # PAYMENT DETAILS
    c.drawString(75 * mm, 76 * mm, "UPI")
    c.drawString(75 * mm, 66 * mm, str(amount))
    c.drawString(75 * mm, 54 * mm, "0")

    c.save()
    return file_path
