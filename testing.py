import io
from flask import Flask, send_file
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PyPDF2

app = Flask(__name__)

@app.route('/generate_pdf')
def generate_pdf():
    # Load existing PDF
    existing_pdf = 'Veridaq_Badges/doc_template.pdf'  # Path to existing PDF file
    output_pdf = 'modified_pdf.pdf'

    # Register Montserrat font
    montserrat_font_path = 'static/Montserrat-ExtraBold.ttf'  # Path to Montserrat font file
    pdfmetrics.registerFont(TTFont("Montserrat", montserrat_font_path))

    # Open the modified PDF
    with open(existing_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Get the first (and only) page of the PDF
        page = reader.pages[0]

        # Create a canvas to draw on the page
        packet = io.BytesIO()
        c = canvas.Canvas(packet)

        # Set font to Montserrat and font size
        c.setFont("Montserrat", 32)

        # Set text color to white
        c.setFillColor("white")  # White color

        # Draw "Hello" on the page
        c.drawString(23.76, 765.08, "Covenant University")

        # Save the canvas to the PDF writer
        c.save()

        # Merge the modified page with the existing page
        overlay = PyPDF2.PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

        # Write the modified PDF to a file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
    
    modified_pdf = "modified_pdf.pdf"

    # Open the modified PDF
    with open(modified_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Get the first (and only) page of the PDF
        page = reader.pages[0]

        # Create a canvas to draw on the page
        packet = io.BytesIO()
        c = canvas.Canvas(packet)

        # Set font to Montserrat and font size
        c.setFont("Montserrat", 32)

        # Set text color to white
        c.setFillColor("white")  # White color

        # Draw "Hello" on the page
        c.drawString(23.04, 695.64, "Tomiwa Philip")

        # Save the canvas to the PDF writer
        c.save()

        # Merge the modified page with the existing page
        overlay = PyPDF2.PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

        # Write the modified PDF to a file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    # Send the modified PDF as a response
    return send_file(output_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
