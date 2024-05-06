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


def generateMemberReference(
        memberName, memberID, nameOfInstitution, passportUrl, memberSince, moreInfo, nameOfOrganization,
        nameOfAdmin, adminDesignation, currentDateTime, badgeID
):
    # Load existing PDF
    existing_pdf = 'Veridaq_Badges/member_template.pdf'  # Path to existing PDF file
    output_pdf = 'generated_badges/member_pdf.pdf'

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
        c.drawString(24.48, 620, memberName)

        c.setFont("Montserrat-Bold", 14)
        c.drawString(142.56, 582, memberID)

        c.setFont("Montserrat-Bold", 12)
        c.drawString(110.68, 555, nameOfInstitution)

        # URL of the image
        url = passportUrl

        # Send a GET request to the URL to download the image
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the image from the response content
            image = Image.open(BytesIO(response.content))

            # Now you can work with the image as needed
            resized_image = image.resize((117, 105))

            resized_image.save("images/member_resized_image.jpg")

        else:
            print("Failed to download the image")
            return "Unable to download or read image from remote url", 400

        c.drawInlineImage('images/member_resized_image.jpg', 24.48, 365)

        c.setFont("Montserrat-Regular", 14)
        c.setFillColor("black") 

        c.drawString(179.28, 315.6, memberSince)
        c.drawString(180, 290.68, moreInfo)

        c.setFont("Montserrat-Bold", 14)
        c.drawString(24.48, 180.8, nameOfInstitution)
        c.drawString(24.48, 159.92, nameOfAdmin)

        c.setFont("Montserrat-Italic", 14)
        c.drawString(24.48, 141.2, adminDesignation)
        c.drawString(24.48, 80, currentDateTime)

        c.setFont("Montserrat-Bold", 14)

        c.setFillColor("white")
        c.drawString(462.24, 640.04, badgeID)

        # Define the URL template with a placeholder for the badge ID
        url_template = 'http://individual.veridaq.com/auth/credential?id={}'

        # Replace the placeholder in the URL template with the actual badge ID
        url = url_template.format(badgeID)

        # Generate QR code and embed it into the PDF
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
        qr.add_data(url)  # Replace 'http://your-link.com' with your actual link
        qr.make(fit=True)
        img = qr.make_image(fill_color="black")
        img.save('qrcode/member_qrcode.png')
        c.drawInlineImage('qrcode/member_qrcode.png', 412.88, 85.76)


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