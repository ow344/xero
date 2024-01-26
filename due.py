from xerointeract.xerodata import XeroRequests
from main import available_orgs, launch_request
from analyse import InvoiceAnalysis, begin_invoice_analysis
from datetime import date

# Update Invoice Data



launch_request()

for org in available_orgs:
    stats = begin_invoice_analysis(org)
    print(stats)
