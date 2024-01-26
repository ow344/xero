from xerointeract.tokenmanage import MySQLaccess
from xerointeract.xerodata import XeroRequests, XeroFirstAuth
from xerointeract.selectorg import select_org, select_org2
from analyse import begin_invoice_analysis
import pandas as pd

from settings import available_orgs


# available_orgs = ['Abbotsford Preparatory School', 'Chadderton Preparatory Grammar School', 'Beechwood School', 'Trinity School']

def launch_request():   
    request_title = input("Title of request: ")
    for org in select_org2(available_orgs):
        XeroRequests(request_title, org)


def analyse():
    single = input("Single or multiple requests? (s/m): ")
    if single == 's':
        org = select_org(available_orgs)
        if input("Continue? (y/n): ") != 'y':
            exit()
        begin_invoice_analysis(org)
    else:
        rez = []
        for org in available_orgs:
            rez.append(begin_invoice_analysis(org))
        print(rez)
        # Convert to pandas dataframe
        df = pd.DataFrame(rez, columns=['School', 'Total', 'Paid', 'Due', 'Credited'])
        print(df)
        # Write the dataframe to the sheet
        with pd.ExcelWriter('finaloutput\\output.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        # Save the excel file




if __name__ == '__main__':
    # XeroFirstAuth()
    launch_request()
    # analyse()
    pass




    # mysqlaccess = MySQLaccess()
    # with mysqlaccess as db:
    #     print(db.get_token())
