import requests
from .auth import auth
import json

class oath():
    def __init__(self):
        access = auth()
        self.access_token = access.token()
        self.endpoint = 'https://api.kroger.com/v1/locations'

    def get_loct(self, zipCode: str="97124", limit: int=13):
        params = {
            'filter.limit': limit,
            'filter.radiusInMiles': 13,
            'filter.zipCode.near': zipCode,
        }

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        result = requests.get(self.endpoint, params=params, headers=headers)

        if result.status_code == 200:
           self.result = result.json()
           return result.json()

    def structure_ts(self, zipCode: str="97124", limit: int=13):
        result = []
        response = self.get_loct(zipCode=zipCode, limit=limit)
        for location in response.get('data', []):
            loc = {
               "name": location.get('name'),
               "phone_number": self.format_phone_number(location.get('phone')),
               "location_id": location.get('locationId'),
               "store_number": location.get('storeNumber'),
               "addressLine1": location.get('address', {})['addressLine1'],
               "city": location.get('address', {})['city'],
               "state": location.get('address', {})['state'],
               "zipCode": location.get('address', {})['zipCode'],
               "lat": location.get("geolocation", {}).get("latitude"),
               "lng": location.get("geolocation", {}).get("longitude"),
            }
            loc["address"] = f"{loc['addressLine1']},{loc['city']},{loc['state']} {loc['zipCode']}"
            result.append(loc)

        return result

    def products_endpoint(self, locationId:int=None, q:str=None):
        endpoint = 'https://api.kroger.com/v1/products'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        # Define the parameters for the product search
        params = {
            'filter.locationId': locationId,
            'filter.term': q,
            'filter.limit': 44,
        }
        print('access_token: ', self.access_token)
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()

        return response.text

    def structure_pos(self, locationId: int=70100661, search: str="milk"):
        result = []
        response = self.products_endpoint(locationId=locationId, q=search)

        for item in response.get('data', []):
            pos = {
                "name": item.get("description"),
                "productId": item.get("productId"),
                "brand": item.get("brand"),
                "price": item.get("items", [])[0].get("price", {}).get("regular"),
                "size": item.get("items", [])[0].get("size", {}),
            }
            # Extracting the small front image
            images = item.get("images", [])
            for image in images:
                if image.get("perspective") == "front":
                    for size in image.get("sizes", []):
                        if size.get("size") == "small":
                            pos["smlImage"] = size.get("url")
                    break
            result.append(pos)

        return result

    def format_phone_number(self, phone_number):
        phone_number = str(phone_number)  # Ensure it's a string
        return f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
