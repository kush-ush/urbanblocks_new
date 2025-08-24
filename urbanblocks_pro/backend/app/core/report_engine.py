from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(report_data, filename="report.pdf"):
    path = os.path.join("data", filename)
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, "UrbanBlocks Layout Report")
    c.drawString(100, 730, f"Score: {report_data.get('score', 'N/A')}")
    c.drawString(100, 710, f"Summary: {report_data.get('summary', '')}")
    c.save()
    return path