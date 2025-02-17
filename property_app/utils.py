from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_rent_agreement(booking):
    filename = f"rent_agreement_{booking.id}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    content = [
        Paragraph("RENTAL AGREEMENT", styles['Heading1']),
        Paragraph(f"This agreement is made between {booking.user.get_full_name()} (Tenant) and {booking.property.owner.get_full_name()} (Landlord)...", styles['BodyText'])
    ]
    
    doc.build(content)
    return filename