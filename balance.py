from xerointeract.tokenmanage import MySQLaccess
from xerointeract.selectorg import select_org2
from xerointeract.xerodata import XeroRequests
import pandas as pd
import json
from settings import available_orgs
from datetime import date



def my_merge(df1, df2):
    if df1 is None:
        df1 = df2
    else:
        df1 = pd.concat([df1, df2], axis=1)
    return df1


def shift_rows_to_top(df, rows_to_shift):
    """Shift row, given by index_to_shift, to top of df."""
    idx = df.index.tolist()
    for i in rows_to_shift:
        idx.remove(i)

    df = df.reindex(rows_to_shift + idx)

    return df

def XeroBalanceSheets(**kwargs):
    filtered_request = ''
    if kwargs:
        filtered_request = '?'
        for key, value in kwargs.items():
            filtered_request += f'{key}={value}&'
        filtered_request = filtered_request[:-1]
    request_title = 'Reports/BalanceSheet'
    request_title += filtered_request
    for org in select_org2(available_orgs):
        XeroRequests(request_title, org)

class Analysis:
    def __init__(self, school):
        self.school = school

    def load_json(self, path_to_file):
        with open(path_to_file, 'r') as f:
            return json.load(f)
        
class BSAnalysis(Analysis):
    def __init__(self, school):
        super().__init__(school)
        path_to_file = f'C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\xerooutput\\{school}\\Reports-BalanceSheet.json'
        self.data = self.load_json(path_to_file)
        self.bs = self.data["Reports"][0]

    def get_bank_df(self):
        target = "Bank"
        for sections in self.bs["Rows"]:
            if sections["RowType"] == "Section" and sections["Title"] == target:
                mydict = {}
                for rows in sections["Rows"]:
                    mydict[rows["Cells"][0]["Value"]] = rows["Cells"][1]["Value"]
        return pd.DataFrame.from_dict({"Total Bank": mydict.get("Total Bank", 0)}, orient='index', columns=[f'{self.school}'])
        
    
    
    def get_current_assets_df(self):
        target = "Current Assets"
        for sections in self.bs["Rows"]:
            if sections["RowType"] == "Section" and sections["Title"] == target:
                mydict = {}
                for rows in sections["Rows"]:
                    if rows["Cells"][0]["Value"] != "Total Current Assets":
                        mydict[rows["Cells"][0]["Value"]] = rows["Cells"][1]["Value"]   
        return pd.DataFrame.from_dict(mydict, orient='index', columns=[f'{self.school}'])
    
    def get_current_liabilities_df(self):
        target = "Current Liabilities"
        for sections in self.bs["Rows"]:
            if sections["RowType"] == "Section" and sections["Title"] == target:
                mydict = {}
                for rows in sections["Rows"]:
                    if rows["Cells"][0]["Value"] != "Total Current Liabilities":
                        mydict[rows["Cells"][0]["Value"]] = rows["Cells"][1]["Value"]   
        return pd.DataFrame.from_dict(mydict, orient='index', columns=[f'{self.school}'])
    
    def get_fixed_assets_df(self):
        target = "Fixed Assets"
        for sections in self.bs["Rows"]:
            if sections["RowType"] == "Section" and sections["Title"] == target:
                mydict = {}
                for rows in sections["Rows"]:
                    if rows["Cells"][0]["Value"] != "Total Fixed Assets":
                        mydict[rows["Cells"][0]["Value"]] = rows["Cells"][1]["Value"]
        try:  
            return pd.DataFrame.from_dict(mydict, orient='index', columns=[f'{self.school}'])
        except UnboundLocalError:
            return pd.DataFrame.from_dict({}, orient='index', columns=[f'{self.school}'])
        
    def get_equity_df(self):
        target = "Equity"
        for sections in self.bs["Rows"]:
            if sections["RowType"] == "Section" and sections["Title"] == target:
                mydict = {}
                for rows in sections["Rows"]:
                    if rows["Cells"][0]["Value"] != "Total Equity":
                        mydict[rows["Cells"][0]["Value"]] = rows["Cells"][1]["Value"]
        return pd.DataFrame.from_dict(mydict, orient='index', columns=[f'{self.school}'])
    
    def get_non_current_liabilities_df(self):
        target = "Non-Current Liabilities"
        for sections in self.bs["Rows"]:
            if sections["RowType"] == "Section" and sections["Title"] == target:
                mydict = {}
                for rows in sections["Rows"]:
                    if rows["Cells"][0]["Value"] != "Total Non-Current Liabilities":
                        mydict[rows["Cells"][0]["Value"]] = rows["Cells"][1]["Value"]
        try:
            return pd.DataFrame.from_dict(mydict, orient='index', columns=[f'{self.school}'])
        except UnboundLocalError:
            return pd.DataFrame.from_dict({}, orient='index', columns=[f'{self.school}'])
        



def get_all_current_assets():
    df1 = None
    for school in available_orgs:
        df1 = my_merge(df1, BSAnalysis(school).get_current_assets_df())
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    to_top = ['Parent Debtors', 'Other Debtors', 'Prepayment', 'Provision for Bad Debts', 'Stock', 'Uniform Stock']
    df1 = shift_rows_to_top(df1, to_top)
    return df1
    
def get_all_bank():
    df1 = None
    for school in available_orgs:
        df1 = my_merge(df1, BSAnalysis(school).get_bank_df())
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    return df1

def get_all_current_liabilities():
    df1 = None
    for school in available_orgs:
        df1 = my_merge(df1, BSAnalysis(school).get_current_liabilities_df())
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    to_top = ['Suppliers Owed', 'School Trips', 'Long Term Deposits', 'Short Term Deposits', 'PTFA', 'Scholarship Fund Reserves (Tanner Trust)', 'Multi Years Deferred Income', 'Annual Deferred Income', 'Termly Deferred Income', 'Spring Term Deferred Income', 'Summer Term Deferred Income', 'Autumn Term Deferred Income']
    df1 = shift_rows_to_top(df1, to_top)
    df1.loc['Total Current Liabilities'] = df1.sum()
    return df1

def get_all_fixed_assets():
    df1 = None
    for school in available_orgs:
        df1 = my_merge(df1, BSAnalysis(school).get_fixed_assets_df())
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    df1.loc['Total Fixed Assets'] = df1.sum()
    return df1

def get_all_non_current_liabilities():
    df1 = None
    for school in available_orgs:
        df1 = my_merge(df1, BSAnalysis(school).get_non_current_liabilities_df())
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    df1.loc['Total Non Current Liabilities'] = df1.sum()
    return df1

def get_all_equity():
    df1 = None
    for school in available_orgs:
        df1 = my_merge(df1, BSAnalysis(school).get_equity_df())
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    df1.loc['Total Equity'] = df1.sum()
    return df1

def get_all_bac():
    df1 = get_all_bank()
    df2 = get_all_current_assets()
    df3 = pd.concat([df1, df2], axis=0)
    df3.loc['Total Current Assets'] = df3.sum()
    return df3

def date_selector():
    if input('Do you want to use todays date? (y/n): ').lower() == 'y':
        t_date = date.today()
    else:
        str_date = input('Enter date in format YYYY-MM-DD: ')
        t_date = date.fromisoformat(str_date)
    return t_date


bs_date = date_selector()
XeroBalanceSheets(date=str(bs_date))

with pd.ExcelWriter(f"C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\{bs_date.strftime("%Y%m%d")} Consol Balance Sheet.xlsx") as writer:  
    get_all_fixed_assets().to_excel(writer, sheet_name='Fixed Assets')
    get_all_bac().to_excel(writer, sheet_name='Current Assets')
    get_all_current_liabilities().to_excel(writer, sheet_name='Current Liabilities')
    get_all_non_current_liabilities().to_excel(writer, sheet_name='Non Current Liabilities')
    get_all_equity().to_excel(writer, sheet_name='Equity')
