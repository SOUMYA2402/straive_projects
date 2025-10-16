from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create a canvas object to write a PDF
c = canvas.Canvas("one_line_pdf.pdf", pagesize=letter)

# Set the font and size for the text
c.setFont("Helvetica", 12)

# Add a line of text (x, y are the coordinates)
c.drawString(100, 750, "This is a one-line PDF that I have created.")

# Save the PDF
c.save()
