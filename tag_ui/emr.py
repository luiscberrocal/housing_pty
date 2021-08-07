import json

def get_credential_data(environment, **kwargs):
    credentials_file = kwargs.get('credentials_file', '../.creds/emr_cred.json')
    with open(credentials_file, 'r') as json_file:
        creds = json.load(json_file)
    return creds.get(environment)

def login_to_admin(admin_url, username, password, robot):
    pass


if __name__ == '__main__':
    env = 'staging'
    cred = get_credential_data(env)
    print(cred)