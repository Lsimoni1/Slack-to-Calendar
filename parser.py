import pdfplumber
import config

def pdf_to_schedule(file):
    pdf = pdfplumber.open(file)
    data = pdf.pages[0].extract_table()

    for row in data:
        if row[0] == config.MY_NAME:
            return row
    return None

def pdf_to_dates(file):
    pdf = pdfplumber.open(file)
    data = pdf.pages[0].extract_table()

    for row in data:
        if row[0] in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
            return row
    return None