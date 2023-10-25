from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus.flowables import PageBreak

# Create a custom paragraph style with full justification
styles = getSampleStyleSheet()
justified_style = ParagraphStyle(name="JustifiedStyle", parent=styles["Normal"])
justified_style.alignment = TA_JUSTIFY

# Sample text with line breaks for demonstration
text = """
This is a sample paragraph. It will be justified and fully use the width of the page.
You can add more text here and it will automatically wrap to the next line.
Just make sure to replace this sample text with your content.
"""

# Create a PDF document
doc = SimpleDocTemplate("output.pdf", pagesize=letter)

# Create a list of flowables (content elements)
story = []

# Split the text into paragraphs and create Paragraph elements
paragraphs = text.split('\n')
for paragraph in paragraphs:
    if paragraph.strip():
        story.append(Paragraph(paragraph, justified_style))

# Add a page break to start a new page if needed
story.append(PageBreak())

# Build the document
doc.build(story)