from xerointeract.tokenmanage import MySQLaccess
from xerointeract.selectorg import select_org2
from xerointeract.xerodata import XeroRequests
import pandas as pd
import json
from settings import available_orgs

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
        print(school)
        bsanalysis = BSAnalysis(school)
        df2 = bsanalysis.get_current_assets_df()
        if df1 is None:
            df1 = df2
        else:
            df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    print(df1)
    df1.to_excel("C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\currentassets.xlsx")
    


def get_all_bank():
    df1 = None
    for school in available_orgs:
        print(school)
        bsanalysis = BSAnalysis(school)
        df2 = bsanalysis.get_bank_df()
        if df1 is None:
            df1 = df2
        else:
            df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    print(df1)
    df1.to_excel("C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\bank.xlsx")

def get_all_current_liabilities():
    df1 = None
    for school in available_orgs:
        print(school)
        bsanalysis = BSAnalysis(school)
        df2 = bsanalysis.get_current_liabilities_df()
        if df1 is None:
            df1 = df2
        else:
            df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    print(df1)
    df1.to_excel("C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\currentliabilities.xlsx")

def get_all_fixed_assets():
    df1 = None
    for school in available_orgs:
        print(school)
        bsanalysis = BSAnalysis(school)
        df2 = bsanalysis.get_fixed_assets_df()
        if df1 is None:
            df1 = df2
        else:
            df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    print(df1)
    df1.to_excel("C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\fixedassets.xlsx")

def get_all_non_current_liabilities():
    df1 = None
    for school in available_orgs:
        print(school)
        bsanalysis = BSAnalysis(school)
        df2 = bsanalysis.get_non_current_liabilities_df()
        if df1 is None:
            df1 = df2
        else:
            df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    print(df1)
    df1.to_excel("C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\noncurrentliabilities.xlsx")

def get_all_equity():
    df1 = None
    for school in available_orgs:
        print(school)
        bsanalysis = BSAnalysis(school)
        df2 = bsanalysis.get_equity_df()
        if df1 is None:
            df1 = df2
        else:
            df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.apply(pd.to_numeric, errors='coerce')  # Convert values to numeric format
    df1.fillna(0, inplace=True)
    print(df1)
    df1.to_excel("C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\finaloutput\\equity.xlsx")


XeroBalanceSheets(date='2023-12-31')
get_all_current_assets()
get_all_bank()
get_all_current_liabilities()
get_all_fixed_assets()
get_all_non_current_liabilities()
get_all_equity()


