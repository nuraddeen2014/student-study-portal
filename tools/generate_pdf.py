from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import textwrap

input_md = 'documentation.md'
output_pdf = 'documentation.pdf'

# Read markdown file (we'll render headings simply)
with open(input_md, 'r', encoding='utf-8') as f:
    content = f.read()

styles = getSampleStyleSheet()
if 'Heading1' not in styles:
    styles.add(ParagraphStyle(name='Heading1', fontSize=16, leading=20, spaceAfter=10, spaceBefore=12))
if 'Heading2' not in styles:
    styles.add(ParagraphStyle(name='Heading2', fontSize=14, leading=18, spaceAfter=8, spaceBefore=10))
if 'Body' not in styles:
    styles.add(ParagraphStyle(name='Body', fontSize=11, leading=16))

story = []
for line in content.splitlines():
    if line.startswith('# '):
        story.append(Paragraph(line[2:].strip(), styles['Heading1']))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:].strip(), styles['Heading2']))
    elif line.startswith('---'):
        story.append(Spacer(1, 12))
    elif line.strip() == '':
        story.append(Spacer(1, 6))
    else:
        # wrap long lines
        wrapped = '\n'.join(textwrap.wrap(line, width=110))
        story.append(Paragraph(wrapped.replace('&', '&amp;'), styles['Body']))

    # small spacer after each element
    story.append(Spacer(1, 6))

# Build PDF
SimpleDocTemplate(output_pdf, pagesize=A4).build(story)
print('PDF generated:', output_pdf)
