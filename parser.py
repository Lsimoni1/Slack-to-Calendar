import pdfplumber
import config
from datetime import datetime

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
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    for row in data:
        for month in months:
                if month in row[0]:
                    row[0] = month
                    return row
    return None

def sort_dates(dates):
    month = dates[0]
    try:
        if dates.index("1") > 1:
            month_value = datetime.strptime(month, "%B").month + 1
            if month_value > 12:
                month_value = 1
            dates.append(datetime.strptime(str(month_value), "%m").strftime("%B"))
    except:
        return