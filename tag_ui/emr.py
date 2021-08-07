import json
import rpa as r


def get_credential_data(environment, **kwargs):
    credentials_file = kwargs.get('credentials_file', '../.creds/emr_cred.json')
    with open(credentials_file, 'r') as json_file:
        creds = json.load(json_file)
    return creds.get(environment)


def login_to_admin(admin_url, username, password):
    r.url(admin_url)
    #//Employee/[@id='4']

    element = '//input[@id="id_username"]'
    r.click(element)
    r.type(element, username)

    element = '//input[@id="id_password"]'
    r.click(element)
    r.type(element, password)
    r.click('Log in.png')

if __name__ == '__main__':
    env = 'staging'
    cred = get_credential_data(env)
    #print(cred)
    r.init()

    ## LOGIN
    admin_url = cred['base_url'] + cred['roles']['admin']['url']
    username = cred['roles']['admin']['username']
    password = cred['roles']['admin']['password']
    login_to_admin(admin_url, username, password)

    r.wait(30)
    r.close()
