import pdfplumber
import config
from datetime import datetime

months = dict([
               ("Jan" , "January"), ("January", "January"), ("Feb", "February"), ("February", "February"),
               ("Mar", "March"), ("March", "March"), ("Apr", "April"), ("April", "April"),
               ("Jun", "June"), ("June", "June"), ("May", "May"),
               ("Jul", "July"), ("July", "July"), ("Aug", "August"), ("August", "August"), 
               ("Sept", "September"), ("September", "September"), ("Oct", "October"), ("October", "October"), 
               ("Nov", "November"), ("November", "November"), ("Dec", "December"), ("December", "December")
            ])

def pdf_to_schedule(file):
    pdf = pdfplumber.open(file)
    data = pdf.pages[0].extract_table()

    for row in data:
        if row[0] == config.MY_NAME:
            return row
    raise ValueError("No schedule row found for " + config.MY_NAME + " in the pdf file: " + file)

def pdf_to_dates(file):
    pdf = pdfplumber.open(file)
    data = pdf.pages[0].extract_table()

    for row in data:
        for k, v in months.items(): 
            if k in row[0]:
                row[0] = v
                row[1:] = [x.split()[0] for x in row[1:]]
                return row
    raise ValueError("No month row found in the pdf file: " + file)

def sort_dates(dates):
    month = dates[0]
    days = dates[2:]
    if "1" in days:
        month_value = datetime.strptime(month, "%B").month + 1
        if month_value > 12:
            month_value = 1
        dates.append(datetime.strptime(str(month_value), "%m").strftime("%B"))
