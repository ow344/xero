from xerointeract.tokenmanage import MySQLaccess
from xerointeract.xerodata import XeroRequests, XeroFirstAuth
from xerointeract.selectorg import select_org
from analyse import begin_analysis
import pandas as pd

available_orgs = ['Abbotsford Preparatory School','Ashley Manor Prep School','Beechwood School',
'Chadderton Preparatory Grammar School','Clevelands Prep School','Lady Lane Park School',
'Lucton School','Moor Allerton Prep School','Prebendal School','Sackville School',
'Sherrardswood School','St Edwards Senior School','St James School','St Martins Prep School',
'The Chalfonts','Trinity School','Wellesley Haddon Dene School','Wellow House','Wycombe Preparatory School']


# available_orgs = ['Abbotsford Preparatory School', 'Chadderton Preparatory Grammar School', 'Beechwood School', 'Trinity School']

def launch_request():   
    request_title = input("Title of request: ")
    single = input("Single or multiple requests? (s/m): ")
    if single == 's':
        org = select_org(available_orgs)
        if input("Continue? (y/n): ") != 'y':
            exit()
        XeroRequests(request_title, org)
    else:
        for org in available_orgs:
            XeroRequests(request_title, org)

def analyse():
    single = input("Single or multiple requests? (s/m): ")
    if single == 's':
        org = select_org(available_orgs)
        if input("Continue? (y/n): ") != 'y':
            exit()
        begin_analysis(org)
    else:
        rez = []
        for org in available_orgs:
            rez.append(begin_analysis(org))
        print(rez)
        # Convert to pandas dataframe
        df = pd.DataFrame(rez, columns=['School', 'Total', 'Paid', 'Due', 'Credited'])
        print(df)
        # Write the dataframe to the sheet
        with pd.ExcelWriter('finaloutput\\output.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        # Save the excel file




if __name__ == '__main__':
    # pass
    # XeroFirstAuth()
    # launch_request()
    analyse()




    # mysqlaccess = MySQLaccess()
    # with mysqlaccess as db:
    #     print(db.get_token())
