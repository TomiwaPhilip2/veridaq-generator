from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PyPDF2
import qrcode
import io
from flask import send_file

def generateWorkReference( 
        nameOfEmployee, employeeID, employeeStatus, nameOfInstitution, subType, 
        designation, department, period, jobFunctions, notableAchievement, personalitySummary, 
        nameOfAdmin, adminDesignation, currentDateTime, badgeID
    ):
    # Load existing PDF
    existing_pdf = 'Veridaq_Badges/work_template.pdf'  # Path to existing PDF file
    output_pdf = 'generated_badges/work_pdf.pdf'

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
        c.drawString(24.48, 782, nameOfEmployee)

        c.setFont("Montserrat-Bold", 14)
        c.drawString(124.46, 749, employeeID)
        c.drawString(155.48, 722, employeeStatus)
        c.drawString(100.48, 695, nameOfInstitution)

        c.setFont("Montserrat-Regular", 14)
        c.setFillColor("black") 

        c.drawString(167.04, 549, subType)
        c.drawString(167.04, 522, designation)
        c.drawString(167.04, 495, department)
        c.drawString(167.04, 470, period)
        c.drawString(167.04, 438, jobFunctions)
        c.drawString(167.04, 348, notableAchievement)
        c.drawString(167.04, 301, personalitySummary)

        c.setFont("Montserrat-Bold", 14)
        c.drawString(24.48, 165, nameOfInstitution)
        c.drawString(24.48, 146, nameOfAdmin)

        c.setFont("Montserrat-Italic", 14)
        c.drawString(24.48, 126, adminDesignation)
        c.drawString(24.48, 66, currentDateTime)

        c.setFont("Montserrat-Bold", 14)

        c.setFillColor("white")
        c.drawString(462.24, 816, badgeID)

        # Generate QR code and embed it into the PDF
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=4)
        qr.add_data('http://veridaq.com')  # Replace 'http://your-link.com' with your actual link
        qr.make(fit=True)
        img = qr.make_image(fill_color="black")
        img.save('qrcode/work_qrcode.png')
        c.drawInlineImage('qrcode/work_qrcode.png', 410, 67)


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