import webbrowser
import base64
import json
import requests
from os import environ, path
from dotenv import load_dotenv
from settings import basedir
load_dotenv(path.join(basedir, '.env'))

from xerointeract.tokenmanage import MySQLaccess

client_id = environ.get('client_id')
client_secret = environ.get('client_secret')

redirect_url = 'http://localhost:5000/'
scope = 'offline_access accounting.transactions accounting.reports.read'
b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')

def XeroFirstAuth():
    # 1. Send a user to authorize your app
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')
    webbrowser.open_new(auth_url)
    # 2. Users are redirected back to you with a code
    auth_res_url = input('What is the response URL? ')
    start_number = auth_res_url.find('code=') + len('code=')
    end_number = auth_res_url.find('&scope')
    auth_code = auth_res_url[start_number:end_number]
    print(auth_code)
    # 3. Exchange the code
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(exchange_code_url,
                            headers={'Authorization': 'Basic ' + b64_id_secret},
                            data = {'grant_type': 'authorization_code','code': auth_code,'redirect_uri': redirect_url})
    json_response = response.json()
    print(json_response)
    with MySQLaccess() as mysql_access:
        mysql_access.post_token(json_response['refresh_token'])
    return [json_response['access_token'], json_response['refresh_token']]


def XeroTenants(access_token, tenant_name = None):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url, headers = {'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'})
    json_response = response.json()
    # print(list(tenants['tenantName'] for tenants in json_response))
    for tenants in json_response:
        if tenant_name:
            if tenants['tenantName'] == tenant_name:
                json_dict = tenants
                break
        else:
            json_dict = tenants
    return json_dict['tenantId']

def XeroRefreshToken():
    with MySQLaccess() as mysql_access:
        refresh_token = mysql_access.get_token()
        print(refresh_token)
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                            headers = {'Authorization' : 'Basic ' + b64_id_secret,'Content-Type': 'application/x-www-form-urlencoded'},
                            data = {'grant_type' : 'refresh_token','refresh_token' : refresh_token})
    json_response = response.json()
    new_refresh_token = json_response['refresh_token']

    with MySQLaccess() as mysql_access:
        mysql_access.post_token(new_refresh_token)

    return [json_response['access_token'], json_response['refresh_token']]

def XeroRequests(request_title, tenant_name = None):
    print(f"Requesting for {tenant_name}")
    new_tokens = XeroRefreshToken()
    xero_tenant_id = XeroTenants(new_tokens[0], tenant_name)
    get_url = f'https://api.xero.com/api.xro/2.0/{request_title}'
    response = requests.get(get_url, headers ={'Authorization': 'Bearer ' + new_tokens[0],'Xero-tenant-id': xero_tenant_id,'Accept': 'application/json'})
    json_response = response.json()
    file_title = request_title.replace("/", "-")
    if tenant_name:
        file_path = f'xerooutput\\{tenant_name}\\{file_title}.json'
    else:
        file_path = f'xerooutput\\{file_title}.json'
    with open(file_path, 'w') as file:
        json.dump(json_response, file)



if __name__ == "__main__":
    # XeroFirstAuth()

    request_title = input("Title of request: ")
    XeroRequests(request_title)
