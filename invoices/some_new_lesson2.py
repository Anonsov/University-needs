#!/usr/bin/env python3
"""
FinTrack Co. — Multi-Format Invoice Generator
Single-file implementation WITHOUT Pathlib or typing imports.
"""

import os
import abc
from datetime import datetime

# Optional libraries (for PDF and Excel)
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

try:
    import openpyxl
    from openpyxl import Workbook
    OPENPYXL_AVAILABLE = True
except Exception:
    OPENPYXL_AVAILABLE = False


# Ensure invoices folder exists
INVOICES_DIR = os.path.join(os.getcwd(), "invoices")
os.makedirs(INVOICES_DIR, exist_ok=True)


# ==========================================================
# ABSTRACT BASE CLASS
# ==========================================================
class InvoiceGenerator(abc.ABC):
    """Abstract base class for all invoice generators."""

    def __init__(self, client_name, items):
        """
        client_name: str
        items: list of {'name': str, 'price': float}
        """
        self.client_name = client_name
        self.items = list(items)

    def calculate_total(self):
        total = 0.0
        for item in self.items:
            try:
                total += float(item.get("price", 0.0))
            except Exception:
                raise ValueError(f"Invalid price in item: {item}")
        return total

    @abc.abstractmethod
    def generate_invoice(self, file_path=None):
        """Must be implemented by subclasses."""
        pass


# ==========================================================
# MIXIN FOR VAT
# ==========================================================
class TaxMixin:
    """Adds 10% VAT to total."""

    VAT_RATE = 0.10

    def total_with_vat(self):
        return self.calculate_total() * (1.0 + self.VAT_RATE)

    def vat_amount(self):
        return self.calculate_total() * self.VAT_RATE


# ==========================================================
# PDF IMPLEMENTATION
# ==========================================================
class PDFInvoiceGenerator(InvoiceGenerator):
    def generate_invoice(self, file_path=None):
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("reportlab not installed. Run: pip install reportlab")

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        if file_path is None:
            file_path = os.path.join(INVOICES_DIR, f"invoice_{self.client_name}_{timestamp}.pdf")

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawString(30 * mm, height - 30 * mm, f"Invoice — {self.client_name}")

        c.setFont("Helvetica", 9)
        c.drawString(30 * mm, height - 38 * mm, f"Generated on: {now}")

        y = height - 50 * mm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30 * mm, y, "Item")
        c.drawString(140 * mm, y, "Price")
        y -= 8 * mm

        c.setFont("Helvetica", 10)
        for item in self.items:
            c.drawString(30 * mm, y, str(item.get("name", "")))
            c.drawRightString(200 * mm, y, f"{float(item.get('price',0)):.2f}")
            y -= 6 * mm
            if y < 30 * mm:
                c.showPage()
                y = height - 30 * mm

        base_total = self.calculate_total()
        c.setFont("Helvetica-Bold", 11)
        y -= 8 * mm

        if isinstance(self, TaxMixin):
            vat = self.vat_amount()
            total = self.total_with_vat()
            c.drawString(30 * mm, y, "Subtotal:")
            c.drawRightString(200 * mm, y, f"{base_total:.2f}")
            y -= 6 * mm
            c.drawString(30 * mm, y, f"VAT (10%):")
            c.drawRightString(200 * mm, y, f"{vat:.2f}")
            y -= 6 * mm
            c.drawString(30 * mm, y, "Total:")
            c.drawRightString(200 * mm, y, f"{total:.2f}")
        else:
            c.drawString(30 * mm, y, "Total:")
            c.drawRightString(200 * mm, y, f"{base_total:.2f}")

        c.save()
        return file_path


# ==========================================================
# EXCEL IMPLEMENTATION
# ==========================================================
class ExcelInvoiceGenerator(InvoiceGenerator):
    def generate_invoice(self, file_path=None):
        if not OPENPYXL_AVAILABLE:
            raise RuntimeError("openpyxl not installed. Run: pip install openpyxl")

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        if file_path is None:
            file_path = os.path.join(INVOICES_DIR, f"invoice_{self.client_name}_{timestamp}.xlsx")

        wb = Workbook()
        ws = wb.active
        ws.title = "Invoice"

        ws.append(["Item Name", "Price"])
        for item in self.items:
            ws.append([item.get("name", ""), float(item.get("price", 0))])

        total = self.calculate_total()
        ws.append(["Total", total])

        if isinstance(self, TaxMixin):
            ws.append(["VAT (10%)", self.vat_amount()])
            ws.append(["Total (incl. VAT)", self.total_with_vat()])

        ws.append(["Generated On", str(now)])

        wb.save(file_path)
        return file_path


# ==========================================================
# HTML IMPLEMENTATION
# ==========================================================
class HTMLInvoiceGenerator(InvoiceGenerator):
    def generate_invoice(self, file_path=None):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        if file_path is None:
            file_path = os.path.join(INVOICES_DIR, f"invoice_{self.client_name}_{timestamp}.html")

        total = self.calculate_total()
        items_html = ""
        for item in self.items:
            items_html += f"<tr><td>{item.get('name')}</td><td style='text-align:right'>{float(item.get('price',0)):.2f}</td></tr>"

        if isinstance(self, TaxMixin):
            vat = self.vat_amount()
            total_vat = self.total_with_vat()
            totals_html = f"""
            <tr><td><strong>Subtotal</strong></td><td style='text-align:right'>{total:.2f}</td></tr>
            <tr><td><strong>VAT (10%)</strong></td><td style='text-align:right'>{vat:.2f}</td></tr>
            <tr><td><strong>Total</strong></td><td style='text-align:right'>{total_vat:.2f}</td></tr>
            """
        else:
            totals_html = f"<tr><td><strong>Total</strong></td><td style='text-align:right'>{total:.2f}</td></tr>"

        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Invoice - {self.client_name}</title></head>
<body>
<h1>Invoice — {self.client_name}</h1>
<p>Generated on: {now}</p>
<table border="1" cellspacing="0" cellpadding="5">
<tr><th>Item</th><th>Price</th></tr>
{items_html}
{totals_html}
</table>
</body>
</html>"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        return file_path


# ==========================================================
# FACTORY & VAT VARIANTS
# ==========================================================
class InvoiceFactory:
    registry = {}

    @classmethod
    def register(cls, name, generator_cls):
        cls.registry[name.lower()] = generator_cls

    @classmethod
    def get_generator(cls, fmt, client_name, items):
        key = fmt.lower()
        if key not in cls.registry:
            raise ValueError(f"Unknown format: {fmt}")
        gen_cls = cls.registry[key]
        return gen_cls(client_name, items)


# Register base formats
InvoiceFactory.register("pdf", PDFInvoiceGenerator)
InvoiceFactory.register("excel", ExcelInvoiceGenerator)
InvoiceFactory.register("html", HTMLInvoiceGenerator)

# VAT variants
class PDFInvoiceWithVAT(TaxMixin, PDFInvoiceGenerator): pass
class ExcelInvoiceWithVAT(TaxMixin, ExcelInvoiceGenerator): pass
class HTMLInvoiceWithVAT(TaxMixin, HTMLInvoiceGenerator): pass

InvoiceFactory.register("pdf_vat", PDFInvoiceWithVAT)
InvoiceFactory.register("excel_vat", ExcelInvoiceWithVAT)
InvoiceFactory.register("html_vat", HTMLInvoiceWithVAT)


# ==========================================================
# BUSINESS LOGIC LAYER
# ==========================================================
class InvoiceManager:
    """Handles export operation, independent of format."""

    def __init__(self, generator):
        self.generator = generator

    def export_invoice(self, file_path=None):
        path = self.generator.generate_invoice(file_path)
        print(f"[OK] Invoice generated at: {path}")
        return path


# ==========================================================
# MAIN EXECUTION
# ==========================================================
def main():
    print("=== FinTrack Multi-Format Invoice Generator ===")
    print(f"Invoices will be saved in: {INVOICES_DIR}\n")

    client = "ACME_Corp"
    items = [
        {"name": "Web Design", "price": 300},
        {"name": "Backend API", "price": 950},
        {"name": "Hosting", "price": 50}
    ]

    formats = ["pdf", "excel", "html", "pdf_vat", "excel_vat", "html_vat"]

    for fmt in formats:
        try:
            generator = InvoiceFactory.get_generator(fmt, client, items)
            manager = InvoiceManager(generator)
            manager.export_invoice()
        except Exception as e:
            print(f"[Error] Failed for {fmt}: {e}")

    print("\nAll invoices generated. Check the 'invoices' folder.")


if __name__ == "__main__":
    client_name = input("Enter client name: ")
    items = []

    print("Enter invoice items (type 'done' when finished):")
    while True:
        name = input("Item name: ")
        if name.lower() == "done":
            break
        price = float(input("Item price: "))
        items.append({"name": name, "price": price})

    print("Choose format: pdf / excel / html")
    fmt = input("Enter format: ").lower()

    if fmt == "pdf":
        generator = PDFInvoiceGenerator(client_name, items)
    elif fmt == "excel":
        generator = ExcelInvoiceGenerator(client_name, items)
    elif fmt == "html":
        generator = HTMLInvoiceGenerator(client_name, items)
    else:
        raise ValueError("Unsupported format")

    manager = InvoiceManager(generator)
    manager.export_invoice()

