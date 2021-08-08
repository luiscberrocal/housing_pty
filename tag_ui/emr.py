import json
import rpa as r


def get_credential_data(environment, **kwargs):
    credentials_file = kwargs.get('credentials_file', '../.creds/emr_cred.json')
    with open(credentials_file, 'r') as json_file:
        creds = json.load(json_file)
    return creds.get(environment)


def login_to_admin(admin_url, username, password):
    r.url(admin_url)

    element = '//input[@id="id_username"]'
    if r.exist(element):
        print('Login')
        r.click(element)
        r.type(element, username)

        element = '//input[@id="id_password"]'
        r.click(element)
        r.type(element, password)
        #print(element, password)

        element = '//input[@type="submit"]'
        r.click(element)
    else:
        print('Already logged in')

def change_password(username, new_password):
    #//*[@id="content-main"]/div[9]/table/tbody/tr/th/a
    element = '//tr[@class="model-user"]/th/a'
    r.click(element)
    #//Element[@attribute1="abc" and @attribute2="xyz" and text()="Data"]
    #user_elem = f'//td[@class="field-name" and text()="{username}"]' #/preceding-sibling::th[@class="field-id"]/a'
    user_elem = f'//td[text()="{username}"]/preceding-sibling::th[@class="field-id"]/a'
    r.click(user_elem)
    pwd_form_elem = '//a[@href="../password/"]'
    r.click(pwd_form_elem)

    pwd1_elem = '//input[@id="id_password1"]'
    r.click(pwd1_elem)
    r.type(pwd1_elem, new_password)
    pwd2_elem = '//input[@id="id_password2"]'
    r.click(pwd2_elem)
    r.type(pwd2_elem, new_password)

    submit_elem = '//input[@type="submit"]'
    r.click(submit_elem)
    print('CLICK')



if __name__ == '__main__':
    env = 'staging'
    user = 'drchepe'
    pwd = '_N0SePuede0909'

    cred = get_credential_data(env)
    #print(cred)
    r.init()

    ## LOGIN
    admin_url = cred['base_url'] + cred['roles']['admin']['url']
    username = cred['roles']['admin']['username']
    password = cred['roles']['admin']['password']
    login_to_admin(admin_url, username, password)
    ## CHANGE PASSWORD
    r.wait(2)

    change_password(user, pwd)

    r.wait(30)
    r.close()
