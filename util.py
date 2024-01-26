all_orgs = ['Alpha Schools (Holdings)','Abbotsford Preparatory School','Ashley Manor Prep School','Beechwood School',
'Chadderton Preparatory Grammar School','Clevelands Prep School','Lady Lane Park School',
'Lucton School','Moor Allerton Prep School','Prebendal School','Sackville School',
'Sherrardswood School','St Edwards Senior School','St James School','St Martins Prep School',
'The Chalfonts','Trinity School','Wellesley Haddon Dene School','Wellow House','Wycombe Preparatory School']

import os

path = "C:\\Users\\Olli\\Documents\\Projects\\Xero-2\\xerooutput"

for org in all_orgs:
    if os.path.exists(os.path.join(path, org)):
        print(org)
    else:
        print(f"{org} not found")
        os.mkdir(os.path.join(path, org))
        print("Folder %s created!" % os.path.join(path, org))

