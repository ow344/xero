import json
from datetime import datetime, timezone, date, timedelta

class Analysis:
    def __init__(self, path_to_file):
        self.data = self.load_json(path_to_file)

    def load_json(self, path_to_file):
        with open(path_to_file, 'r') as f:
            return json.load(f)


def convert_date(date_str):
        timestamp_str = date_str.split('(')[1].split('+')[0]
        timestamp = int(timestamp_str) / 1000  # Convert milliseconds to seconds
        dt_object_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        dt_object = dt_object_utc.date()
        return dt_object

class InvoiceAnalysis(Analysis):
    def __init__(self, path_to_file):
        super().__init__(path_to_file)
        self.invoices = self.data["Invoices"]

    def filter_by_status(self, invoices, status, filter_out=False):
        if filter_out:
            return [invoice for invoice in invoices if invoice["Status"] not in status]
        else:
            return [invoice for invoice in invoices if invoice["Status"] in status]
        
    def filter_by_reference(self, invoices, references, filter_out=False):
        new_invoices = []
        for invoice in invoices:
            try:
                if filter_out:
                    if invoice["Reference"] not in references:
                        new_invoices.append(invoice)
                else:
                    if invoice["Reference"] in references:
                        new_invoices.append(invoice)
            except KeyError:
                pass
        return new_invoices
    
    def filter_by_type(self, invoices, types, filter_out=False):
        if filter_out:
            return [invoice for invoice in invoices if invoice["Type"] not in types]
        else:
            return [invoice for invoice in invoices if invoice["Type"] in types]

    def filter_by_dates(self, invoices, start_date, end_date):
        new_invoices = []
        for invoice in invoices:
            try:
                if convert_date(invoice["DueDate"]) >= start_date and convert_date(invoice["DueDate"]) <= end_date:
                    new_invoices.append(invoice)
            except KeyError:
                pass
        return new_invoices
        # Below is old method that could not handle invoices without a due date (return key error)
        # return [invoice for invoice in invoices if convert_date(invoice["DueDate"]) >= start_date and convert_date(invoice["DueDate"]) <= end_date]
    




   
    def totals(self, invoices):
        total = sum([invoice["Total"] for invoice in invoices])
        paid = sum([invoice["AmountPaid"] for invoice in invoices])
        due = sum([invoice["AmountDue"] for invoice in invoices])
        credited = sum([invoice["AmountCredited"] for invoice in invoices])
        return total, paid, due, credited





class PaymentAnalysis(Analysis):
    def __init__(self, path_to_file):
        super().__init__(path_to_file)
        self.payments = self.data["Payments"]

    def filter_by_status(self, payments, status, filter_out=False):
        if filter_out:
            return [payment for payment in payments if payment["Status"] not in status]
        else:
            return [payment for payment in payments if payment["Status"] in status]
        
    def filter_by_reconciliation(self, payments, reconciled=True):
        return [payment for payment in payments if payment["IsReconciled"] == reconciled]













def begin_invoice_analysis(school):
    print(f"Beginning analysis for {school}")
    analysis = InvoiceAnalysis(f"C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\xerooutput\\{school}\\Invoices.json")
    invoices = analysis.filter_by_status(analysis.invoices,["DELETED", "VOIDED"], filter_out=True)
    invoices = analysis.filter_by_type(invoices, ["ACCREC"])
    invoices = analysis.filter_by_dates(invoices, date(2023,10,1), date(2023,12,31))
    # invoices = analysis.filter_by_dates(invoices, date(2022,3,1), date(2024,12,31))

    total, paid, due, credited = analysis.totals(invoices)

    print(total , paid, due, credited)
    print(round(total,2) == round(sum([paid, due, credited]),2))
    print(len(invoices))
    return [school, total, paid, due, credited]

    




# if __name__ == "__main__":
#     x = begin_payment_analysis("Beechwood School")
#     print(x)



example = {
    "Type": "ACCPAY",
    "InvoiceID": "7b7fd50e-b9c9-4f3f-b60d-02d56836310c", 
    "InvoiceNumber": "OB-SR1", 
    "Reference": "", 
    "Payments": [
        {"PaymentID": "d98fffc6-2d83-477e-b936-066aca3a954b",
         "BatchPaymentID": "8e386f25-d739-4a98-b3a3-b912f369b25c", 
         "Date": "/Date(1678838400000+0000)/", 
         "Amount": 995.0, 
         "Reference": "", 
         "CurrencyRate": 1.0, 
         "HasAccount": False, 
         "HasValidationErrors": False}],
    "CreditNotes": [],
    "Prepayments": [],
    "Overpayments": [],
    "AmountDue": 0.0,
    "AmountPaid": 995.0,
    "AmountCredited": 0.0, 
    "CurrencyRate": 1.0, 
    "IsDiscounted": False, 
    "HasAttachments": False, 
    "InvoiceAddresses": [], 
    "HasErrors": False, 
    "InvoicePaymentServices": [],
    "Contact": {
        "ContactID": "d0ad37ca-4b2c-4b57-9451-c9da084ba50d", 
        "Name": "Rambler Coaches Ltd", 
        "Addresses": [], 
        "Phones": [], 
        "ContactGroups": [], 
        "ContactPersons": [], 
        "HasValidationErrors": False}, 
    "DateString": "2023-02-28T00:00:00", 
    "Date": "/Date(1677542400000+0000)/", 
    "DueDateString": "2023-02-28T00:00:00", 
    "DueDate": "/Date(1677542400000+0000)/", 
    "Status": "PAID", 
    "LineAmountTypes": "NoTax", 
    "LineItems": [], 
    "SubTotal": 995.0, 
    "TotalTax": 0.0, 
    "Total": 995.0, 
    "UpdatedDateUTC": "/Date(1680271260047+0000)/", 
    "CurrencyCode": "GBP",
    "FullyPaidOnDate": "/Date(1678838400000+0000)/"}


def get_dates_between(start_date, end_date):
    dates_and_value = {}
    while start_date <= end_date:
        dates_and_value[start_date] = 0
        start_date += timedelta(days=1)
    return dates_and_value


def create_payment_dict(invoices, start_date, end_date):
    dates_and_value = get_dates_between(start_date, end_date)
    for invoice in invoices:
        try:
            for payment in invoice["Payments"]:
                date = convert_date(payment["Date"])
                dates_and_value[date] += payment["Amount"]
        except KeyError:
            dates_and_value[convert_date(invoice["Date"])] = invoice["Total"]
    # Get smallest and largest dates
    start_date = min(dates_and_value.keys())
    end_date = max(dates_and_value.keys())
    # Fill in missing dates
    while start_date <= end_date:
        if start_date not in dates_and_value.keys():
            dates_and_value[start_date] = 0
        start_date += timedelta(days=1)

    # Sort the dictionary by date
    dates_and_value = dict(sorted(dates_and_value.items()))
    
    
    return dates_and_value







def begin_payment_analysis(school):
    print(f"Beginning analysis for {school}")
    analysis = InvoiceAnalysis(f"C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\xerooutput\\{school}\\Invoices.json")
    invoices = analysis.filter_by_status(analysis.invoices,["DELETED", "VOIDED"], filter_out=True)
    invoices = analysis.filter_by_type(invoices, ["ACCREC"])
    invoices = analysis.filter_by_dates(invoices, date(2023,10,1), date(2024,1,31))
    payments = create_payment_dict(invoices, date(2023,10,1), date(2024,1,18))
    return payments


import pandas as pd

available_orgs = ['Abbotsford Preparatory School','Ashley Manor Prep School','Beechwood School',
'Chadderton Preparatory Grammar School','Clevelands Prep School','Lady Lane Park School',
'Lucton School','Moor Allerton Prep School','Prebendal School','Sackville School',
'Sherrardswood School','St Edwards Senior School','St James School','St Martins Prep School',
'The Chalfonts','Trinity School','Wellesley Haddon Dene School','Wellow House','Wycombe Preparatory School']


if __name__ == "__main__":
    # Merge all the dataframes together
    for school in available_orgs:
        x = begin_payment_analysis(school)
        df = pd.DataFrame(x.items(), columns=['Date', school])
        try:
            df_all = pd.merge(df_all, df, on='Date', how='outer')
        except NameError:
            df_all = df

    with pd.ExcelWriter(f'finaloutput\\all.xlsx') as writer:
        df_all.to_excel(writer, sheet_name='Sheet1')

