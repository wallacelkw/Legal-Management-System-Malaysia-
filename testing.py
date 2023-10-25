from fpdf import FPDF



class PDF(FPDF):
    def header(self) -> None:
        self.set_font('helvetica' ,'B', 20)
        self.cell(0, 10, 'LEE CHO & CO', border=False, ln=1, align='C')
        self.set_font('helvetica' ,'B', 10)
        self.cell(0,5 , 'Advocates & Solicitors', ln=1, align='C')
        self.set_font('helvetica' ,'', 10)
        self.cell(0,5 , 'No.13-1, Jalan Cetak 16/3, Seksyen 16,', ln=1,align='C')
        self.cell(0,5 , '40200 Shah Alam, Selangor Darul Ehsan.', ln=1, align='C')
        
        self.ln(1)
       # Tel and Fax
        tel_text = 'Tel: +603-5523 3513'
        fax_text = 'Fax: +603-5523 8513'
        total_width = self.w  # Total width of the page

        # Calculate the combined width of both cells
        tel_width = self.get_string_width(tel_text)
        fax_width = self.get_string_width(fax_text)
        total_text_width = tel_width + fax_width + 20  # 10 units of space

        # Calculate the starting x-coordinate to center the combined text
        x_start = (total_width - total_text_width) / 2

        # Set x position for Tel
        self.set_x(x_start)
        self.cell(tel_width, 5, tel_text, align='L')

        # Set x position for Fax
        self.set_x(x_start + tel_width + 20)
        self.cell(fax_width, 5, fax_text, align='L')

        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(3)
    

    def chapter_body(self, body):
        # Set font for chapter body
        self.set_font("helvetica",'' ,10)
        # MultiCell allows for text to flow and automatically wrap to the next line
        self.multi_cell(0, 5, body)
        self.ln()  # Move down after the paragraph

    def chapter_table(self, table_data):
        # Set font for the table
        self.set_font("Arial", size=10)
        
        # Define column widths
        col_widths = [80, 40, 40]  # Adjust as needed
        
        for row in table_data:
            for i, data in enumerate(row):
                self.cell(col_widths[i], 10, data, border=1)
            self.ln()

    def chapter_title_detail(self, title):
        # Set font for chapter title
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)  # Move down a little

    def chapter_content(self, data):
        # Set font for the content
        self.set_font("Arial", size=10)
        for item in data:
            if isinstance(item, tuple):
                # If it's a tuple, it's a line item
                self.cell(100, 5, item[0], border=1)
                self.cell(45, 5, item[1], align="R", border=1)
                self.cell(45, 5, "", align="R", border=1)
                self.ln()
            else:
                # If it's not a tuple, it's a total
                self.cell(100, 5, "", border=1)
                self.cell(45, 5, "", border=1)
                self.cell(45, 5, item, align="R", border=1)
                self.ln()
        self.ln(5)  # Move down a little

def check_pdf():
    ref = 'REF/902/312/234'
    date = 'Oct.2, 2023'
    add1 = '145A-Kampung Tiong Gemas'
    add2 = 'Jalan Kingdom'
    city = 'Sungai Petani'
    poscode = '8000'
    state = 'Kedah'
    country = 'Malaysia'

    description = '''Attending to and preparing the Discharge of Charge and other relevant documents, attending to execution, stamping and registration of the same, liaising with all parties concerned for relevant information, all other attendances and correspondences not specifically mentioned for for a vacant land held under Individual Title Geran 70519, Lot 37, Bandar Gemas, Derah Tampin, Negeri Sembilan'''


    pdf = PDF('P', 'mm', 'A4')



    # Add a page
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('helvetica', '', 10)
    pdf.ln(3)
    # Add the "Our Ref" and "Date" lines
    our_ref_text = f'Our Ref: {ref}'
    date_text = f'Date: {date}'
    our_ref_width = pdf.get_string_width(our_ref_text)
    date_width = pdf.get_string_width(date_text)
    max_width = min(our_ref_width, date_width)

    pdf.cell(max_width, 5, our_ref_text, align='L')
    pdf.cell(0, 5, date_text, align='R', ln=1)

    # Set the position for the "To" section
    to_x = max_width  # X-coordinate, with additional spacing
    to_y = pdf.get_y()  # Y-coordinate
    print("X: ", to_x)

    # Add the "To" section aligned with "Our Ref"
    # pdf.set_xy(to_x, to_y)
    pdf.cell(0, 5, 'To: ')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, 'CurryLim Muhamad', align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, add1, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, add2, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, f'{city}, {poscode}, {state}', align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, country, align='L')

    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)

    # pdf.cell(0, 5, 'PROFESSIONAL CHARGES IN THE MATTER OF:-', ln=2, align='C')
    pdf.chapter_title('PROFESSIONAL CHARGES IN THE MATTER OF:-')
    pdf.chapter_body(description)



    # Add a chapter title for "PROFESSIONAL CHARGES"
    chapter_title = "PROFESSIONAL CHARGES"
    pdf.chapter_title_detail(chapter_title)

    # Data for professional charges
    proservices = [
        ("Customer Service", "RM 100.00"),
        ("Customer Service", "RM 100.00"),
        ("RM 200.00"),
    ]

    # Add the professional charges content
    pdf.chapter_content(proservices)

    # Add a chapter title for "REIMBURSEMENTS"
    chapter_title = "REIMBURSEMENTS"
    pdf.chapter_title_detail(chapter_title)

    # Data for reimbursements
    articles = [
        ("Printing Service", "RM 122.00"),
        ("Printing Service3", "RM 32.00"),
        ("RM 154.00"),
    ]

    # Add the reimbursements content
    pdf.chapter_content(articles)

    # Add the "Total" section
    total = ["Total", "RM 354.00"]
    pdf.chapter_content(total)


    pdf.output('pdf_1.pdf')

