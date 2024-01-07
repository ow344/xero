import json
from datetime import datetime, timezone, date

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




def begin_analysis(school):
    print(f"Beginning analysis for {school}")
    analysis = InvoiceAnalysis(f"C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\xerooutput\\{school}\\Invoices.json")
    invoices = analysis.filter_by_status(analysis.invoices,["DELETED", "VOIDED"], filter_out=True)
    invoices = analysis.filter_by_type(invoices, ["ACCREC"])
    # invoices = analysis.filter_by_dates(invoices, date(2023,7,1), date(2023,9,30))
    invoices = analysis.filter_by_dates(invoices, date(2022,3,1), date(2024,12,31))

    total, paid, due, credited = analysis.totals(invoices)

    print(total , paid, due, credited)
    print(round(total,2) == round(sum([paid, due, credited]),2))
    print(len(invoices))
    return [school, total, paid, due, credited]



# invoices = analysis.filter_by_reference(invoices,["Spring term", "Spring Term 2024", "Spring term 2024", "Spring Term 24","Spring term 24", "SPRING TERM 24", "Lent Term 2024"])
# ["Spring term", "Spring Term 2024", "Spring term 2024", "Spring Term 24", "SPRING TERM 24", "Lent Term 2024"]
# ["Autumn term", "Autumn Term 2023", "Autumn term 2023", "Autumn Term 23", "AUTUMN TERM 23"]