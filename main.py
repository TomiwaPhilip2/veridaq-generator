from flask import Flask, send_file
from reportlab.pdfgen import canvas
import qrcode

app = Flask(__name__)

@app.route('/generate_pdf')
def generate_pdf():
    # Create a PDF document
    pdf_file = 'generated_pdf.pdf'
    c = canvas.Canvas(pdf_file)
    
    # Add content to the PDF
    c.drawString(100, 750, "Hello, World!")
    
    # Generate QR code and embed it into the PDF
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data('http://your-link.com')  # Replace 'http://your-link.com' with your actual link
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qrcode.png')
    c.drawInlineImage('qrcode.png', 100, 700)  # Adjust position as needed

    # Save the PDF
    c.save()

    # Send the PDF as a response
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
