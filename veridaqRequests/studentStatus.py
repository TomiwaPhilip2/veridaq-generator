from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PyPDF2
import qrcode
import io
from flask import send_file
from PIL import Image
import requests
from io import BytesIO


def generateStudentStatus(
        nameOfStudent, studentID, nameOfInstitution, passportUrl, categoryOfStudy, currentLevel,
        courseOfStudy, faculty, yearOfEntryAndExit, nameOfAdmin, adminDesignation, currentDateTime,
        badgeID
):
    # Load existing PDF
    existing_pdf = 'Veridaq_Badges/student_template.pdf'  # Path to existing PDF file
    output_pdf = 'generated_badges/student_pdf.pdf'

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
        c.drawString(25.2, 783, nameOfStudent)

        c.setFont("Montserrat-Bold", 14)
        c.drawString(107.56, 736, studentID)
        c.drawString(105.68, 709, nameOfInstitution)

        # URL of the image
        url = passportUrl

        # Send a GET request to the URL to download the image
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the image from the response content
            image = Image.open(BytesIO(response.content))

            # Now you can work with the image as needed
            resized_image = image.resize((148, 140))

            resized_image.save("images/student_resized_image.jpg")

        else:
            print("Failed to download the image")
            return "Unable to download or read image from remote url", 400

        c.drawInlineImage('images/student_resized_image.jpg', 24.04, 413)

        c.setFont("Montserrat-Regular", 14)
        c.setFillColor("black") 

        c.drawString(220.64, 362, categoryOfStudy)
        c.drawString(220.64, 336, currentLevel)
        c.drawString(220.64, 307, courseOfStudy)
        c.drawString(220.64, 282, faculty)
        c.drawString(220.64, 256, yearOfEntryAndExit)

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
        img.save('qrcode/student_qrcode.png')
        c.drawInlineImage('qrcode/student_qrcode.png', 410, 67)


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