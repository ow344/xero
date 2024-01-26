# available_orgs = {
#     1: 'Demo Company (UK)',
#     2: 'Beechwood School'}

def select_org(available_orgs):
    print('Available Organisations:')
    idx = 0
    for i in available_orgs:
        print(f'{idx}. {i}')
        idx += 1
    org = int(input('Please select organisation by number: '))
    print(f'You have selected {available_orgs[org]}')
    return available_orgs[org]

def select_org2(available_orgs):
    all_orgs = input("All Orgs or only some? (A): ") in ['a','A']
    if all_orgs:
        return available_orgs
    else:
        orgs = []
        while True:
            print('Available Organisations:')
            idx = 0
            for i in available_orgs:
                print(f'{idx}. {i}')
                idx += 1
            org = int(input('Please select organisation by number: '))
            orgs.append(available_orgs[org])
            print(f'You have selected {orgs}')
            if input("Continue? (y/n): ") != 'y':     
                return orgs   
            else:
                continue
        
