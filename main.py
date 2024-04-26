import io
from flask import Flask, send_file
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PyPDF2
import qrcode

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
        c.setFont("Montserrat", 20)

        # Set text color to white
        c.setFillColor("white")  # White color

        # Draw "Hello" on the page
        c.drawString(23.04, 762.08, "COVENANT UNIVERSITY")
        c.drawString(23.04, 690.64, "TOMIWA PHILIP")

        montserrat_font_path = 'static/Montserrat-Regular.ttf'  # Path to Montserrat font file
        pdfmetrics.registerFont(TTFont("Montserrat2", montserrat_font_path))
        c.setFont("Montserrat2", 14)
        c.setFillColor("black") 

        c.drawString(199.4, 547, "CERTIFICATE")
        c.drawString(199.4, 519, "CERTIFICATE OF DEGREE COMPLETION")
        c.drawString(199.4, 491, "4637CU")
        c.drawString(199.4, 465, "TRUE")
        c.drawString(199.4, 438, "This certificate is from Covenant University itself!")
        c.drawString(24.48, 234, "Covenant University")
        c.drawString(24.48, 212, "Bushiri Gamma")
        c.drawString(24.48, 192, "Registrar")
        c.drawString(24.48, 138, "12-04-6 12:30PM")

        montserrat_font_path = 'static/Montserrat-Bold.ttf'  # Path to Montserrat font file
        pdfmetrics.registerFont(TTFont("Montserrat3", montserrat_font_path))
        c.setFont("Montserrat", 14)

        c.setFillColor("white")
        c.drawString(462.24, 816, "Veridaq-1345")

        # Generate QR code and embed it into the PDF
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=4)
        qr.add_data('http://veridaq.com')  # Replace 'http://your-link.com' with your actual link
        qr.make(fit=True)
        img = qr.make_image(fill_color="black")
        img.save('qrcode.png')
        c.drawInlineImage('qrcode.png', 410, 123)


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
