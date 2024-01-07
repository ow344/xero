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
