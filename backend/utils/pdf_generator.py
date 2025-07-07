from flask import current_app
from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        # Logo
        logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'school_logo.png')
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 33)
        
        # School name
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'SCHOOL NAME', 0, 0, 'C')
        self.ln(20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def generate_pdf_report_card(student, results, attendance):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Student information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'REPORT CARD - TERM {results[0].term if results else "N/A"}', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, 'Student Name:', 0, 0)
    pdf.cell(0, 6, f"{student.first_name} {student.last_name}", 0, 1)
    pdf.cell(40, 6, 'Admission Number:', 0, 0)
    pdf.cell(0, 6, student.admission_number, 0, 1)
    pdf.cell(40, 6, 'Class:', 0, 0)
    pdf.cell(0, 6, student.class_.name if student.class_ else 'N/A', 0, 1)
    pdf.ln(10)
    
    # Results table
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(80, 6, 'Subject', 1, 0)
    pdf.cell(30, 6, 'Marks', 1, 0, 'C')
    pdf.cell(30, 6, 'Grade', 1, 0, 'C')
    pdf.cell(0, 6, 'Remarks', 1, 1)
    
    pdf.set_font('Arial', '', 10)
    for result in results:
        pdf.cell(80, 6, result.subject.name, 1, 0)
        pdf.cell(30, 6, str(result.marks), 1, 0, 'C')
        pdf.cell(30, 6, result.grade, 1, 0, 'C')
        pdf.cell(0, 6, result.remarks or '', 1, 1)
    
    pdf.ln(10)
    
    # Attendance summary
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 6, 'Attendance Summary', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(60, 6, 'Total School Days:', 0, 0)
    pdf.cell(0, 6, str(attendance.get('total_days', 0)), 0, 1)
    pdf.cell(60, 6, 'Days Present:', 0, 0)
    pdf.cell(0, 6, str(attendance.get('present_days', 0)), 0, 1)
    pdf.cell(60, 6, 'Days Absent:', 0, 0)
    pdf.cell(0, 6, str(attendance.get('absent_days', 0)), 0, 1)
    pdf.cell(60, 6, 'Attendance Rate:', 0, 0)
    pdf.cell(0, 6, f"{attendance.get('attendance_rate', 0)}%", 0, 1)
    pdf.ln(10)
    
    # Comments
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Class Teacher Comments:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris.', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Principal Comments:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, 'Vivamus suscipit tortor eget felis porttitor volutpat. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus.', 0, 1)
    
    # Date and signature
    pdf.ln(15)
    pdf.cell(0, 6, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.ln(10)
    pdf.cell(0, 6, '_________________________', 0, 1, 'C')
    pdf.cell(0, 6, 'Principal Signature', 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin1')