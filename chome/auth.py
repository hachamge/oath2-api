import requests

class auth():
    def __init__(self):
        pass

    def token(self):
        self.client_secret = 'Tac-2DoqjuIkVr4EM_hUA-ON7eTSn31hUPQMMpIJ'
        self.client_id = 'stripe-8a98c86b49d93794705dd64bcdbbe3ab2888467165813679391'

        access = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'product.compact'
        }
        endpoint:str = 'https://api.kroger.com/v1/connect/oauth2/token'
        response = requests.post(endpoint, data=access)

        if response.status_code == 200:
            return response.json()['access_token']

        return response
