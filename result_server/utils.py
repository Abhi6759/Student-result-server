import os
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
pdf = FPDF()


def make_pdf(studentdata):
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Results 2021", ln=1)
    pdf.cell(200, 10, txt=f"Name :- {studentdata.Name}", ln=2)
    pdf.cell(200, 10, txt=f"Seat No :- {studentdata.seat_no}", ln=3)
    pdf.cell(200, 10, txt=f"English :- {studentdata.english}", ln=4)
    pdf.cell(200, 10, txt=f"Science :- {studentdata.science}", ln=5)
    pdf.cell(200, 10, txt=f"Maths :- {studentdata.maths}", ln=6)
    pdf.cell(200, 10, txt=f"History :- {studentdata.history}", ln=7)
    pdf.cell(200, 10, txt=f"IT :- {studentdata.IT}", ln=8)
    pdf.output(f"{studentdata.seat_no}_open.pdf")
    out = PdfFileWriter()
    file = PdfFileReader(f"{studentdata.seat_no}_open.pdf")
    num = file.numPages
    for idx in range(num):
        page = file.getPage(idx)
        out.addPage(page)
    password = f"{studentdata.phone_no}"
    out.encrypt(password)
    with open(f"{studentdata.seat_no}.pdf", "wb") as f:
        out.write(f)
    os.remove((f"{studentdata.seat_no}_open.pdf"))





def getresult(studentdata):
    if studentdata.english < 35 or studentdata.science < 35 or studentdata.maths < 35 or studentdata.history < 35 or studentdata.IT < 35:
        return "Sorry You have failed the examination"
    else:
        return "Congratulations You have Passed the examination"



