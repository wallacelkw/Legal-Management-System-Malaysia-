
import os
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from fpdf import FPDF

# def send_email_to_client():

def send_email_with_attachment(subject, message, recipient_list, file_path):
    mail = EmailMessage(subject=subject,body = message, from_email=settings.EMAIL_HOST_USER,
                        to=recipient_list)
    
    mail.attach_file(file_path)
    mail.send()


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
        self.ln(1)  # Move down a little

    def chapter_content(self, data):
        # Set font for the content
        self.set_font("Arial", size=10)
        print(data)
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
        self.ln(1)  # Move down a little

def create_pdf_n_save_it(case,obj,clients,proservices,reimburservice, file_name):
    pdf = PDF('P', 'mm', 'A4')
    
    # Add a page
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('helvetica', '', 10)
    pdf.ln(3)
    # Add the "Our Ref" and "Date" lines
    our_ref_text = f'Our Ref: {case.ref_no}'
    date_text = f'Date: {obj.invoice_date_time}'
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
    pdf.multi_cell(0, 5, clients.full_name, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.address1, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.address2, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, f'{clients.city}, {clients.postcode}, {clients.state}', align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.country, align='L')

    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)

    # pdf.cell(0, 5, 'PROFESSIONAL CHARGES IN THE MATTER OF:-', ln=2, align='C')
    pdf.chapter_title('PROFESSIONAL CHARGES IN THE MATTER OF:-')
    pdf.chapter_body(obj.short_descriptions)

    # Add a chapter title for "PROFESSIONAL CHARGES"
    chapter_title = "PROFESSIONAL CHARGES"
    pdf.chapter_title_detail(chapter_title)

    proservices_data =[]
    for record in proservices:
        proservices_data.append((record.prof_service, f"RM {record.prof_service_price:.2f}"))

    # Add a total row
    total_price = obj.total_prof_service_price
    proservices_data.append( f"RM {total_price:.2f}")
    print("PROSERVUICES: ", proservices_data)
    # Add the professional charges content
    pdf.chapter_content(proservices_data)

    # Add a chapter title for "REIMBURSEMENTS"
    chapter_title = "REIMBURSEMENTS"
    pdf.chapter_title_detail(chapter_title)

    articles_data =[]
    for record in reimburservice:
        articles_data.append((record.reimbur_service, f"RM {record.reimbur_service_price:.2f}"))

    # Add a total row
    total_price = obj.total_reimbur_service_price
    articles_data.append(f"RM {total_price:.2f}")


    # Add the reimbursements content
    pdf.chapter_content(articles_data)

    # Add the "Total" section
    total = ["Total","", f"RM {obj.final_total}"]
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(100, 5, total[0], border=1)
    pdf.cell(45, 5,total[1], border=1)
    pdf.cell(45, 5, total[2], align="R", border=1)







    pdf.ln(50)
    # signature
    pdf.set_font('helvetica', '', 10)
    # Add the signature image at a fixed location (x, y)
    signature_x = 10  # Adjust as needed
    signature_y = 0  # Adjust as needed
    signature_width = 25  # Adjust as needed
    signature_height = 20  # Adjust as needed
    signature_image_path = f"{settings.BASE_DIR}/myadmin/static/images/signature.png"
    
    pdf.set_x(10)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, 'Alice Lee', align='L')
    x = pdf.get_x()
    y = pdf.get_y()
    pdf.set_x(10)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, 'LEE CHEW & CO', align='L')
    pdf.set_x(10)
    pdf.image(signature_image_path, x=signature_x, y=y-25, w=signature_width, h=signature_height)


    pdf.output(f'{file_name}_invoice.pdf')