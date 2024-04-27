from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PyPDF2
import qrcode
import io
from flask import send_file
from PIL import Image


def generateAlumniReference():
    # Load existing PDF
    existing_pdf = 'Veridaq_Badges/alumni_template.pdf'  # Path to existing PDF file
    output_pdf = 'generated_badges/modified_pdf.pdf'

    # Register Montserrat font
    montserrat_font_path = 'static/Montserrat-ExtraBold.ttf'  # Path to Montserrat font file
    pdfmetrics.registerFont(TTFont("Montserrat-ExtraBold", montserrat_font_path))
    montserrat_font_path = 'static/Montserrat-Bold.ttf'  # Path to Montserrat font file
    pdfmetrics.registerFont(TTFont("Montserrat-Bold", montserrat_font_path))
    montserrat_font_path = 'static/Montserrat-Regular.ttf'  # Path to Montserrat font file
    pdfmetrics.registerFont(TTFont("Montserrat-Regular", montserrat_font_path))
    montserrat_font_path = 'static/Montserrat-Italic.ttf'  # Path to Montserrat font file
    pdfmetrics.registerFont(TTFont("Montserrat-Italic", montserrat_font_path))

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
        c.setFont("Montserrat-ExtraBold", 20)

        # Set text color to white
        c.setFillColor("white")  # White color

        # Draw "Hello" on the page
        c.drawString(25.2, 560.24, "TOMIWA PHILIP")

        c.setFont("Montserrat-Bold", 14)
        c.drawString(200.28, 522.6, "FUT606474")
        c.drawString(107.4, 495.76, "Kogi Association")

        c.setFont("Montserrat-Regular", 14)
        c.setFillColor("black") 

        c.drawString(363.6, 363.12, "Yes")
        c.drawString(363.6, 326.4, "Alumni")
        c.drawString(363.6, 288.24, "Great member")

        c.setFont("Montserrat-Bold", 14)
        c.drawString(24.48, 175.8, "KOGI Association")
        c.drawString(24.48, 154.92, "Bola Tinubu")

        c.setFont("Montserrat-Italic", 14)
        c.drawString(24.48, 136.2, "Secretary")
        c.drawString(24.48, 75, "12-04-6 12:30PM")

        c.setFont("Montserrat-Bold", 14)

        c.setFillColor("white")
        c.drawString(462.24, 640.04, "Veridaq-1345")

        # Generate QR code and embed it into the PDF
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=4)
        qr.add_data('http://veridaq.com')  # Replace 'http://your-link.com' with your actual link
        qr.make(fit=True)
        img = qr.make_image(fill_color="black")
        img.save('qrcode/qrcode.png')
        c.drawInlineImage('qrcode/qrcode.png', 412.88, 85.76)


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