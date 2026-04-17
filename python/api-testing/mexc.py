"""
MEXC API Client
Handles authentication and retrieval of spot account balances.
Used as a data source for the Portfolio Dashboard ETL pipeline.
"""

import os
import json
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()


class MexcClient:
    def __init__(self):
        self.api_key = os.getenv('MEXC_API_KEY')
        self.api_secret = os.getenv('MEXC_API_SECRET')
        self.base_url = 'https://api.mexc.com'
        self.save_dir = os.path.join(os.getcwd(), "Responses")

    def _create_signature(self, query_string):
        """Internal helper to sign requests."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

    def get_server_time(self):
        url = f'{self.base_url}/api/v3/time'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['serverTime']

    def get_account_info(self):
        endpoint = '/api/v3/account'
        params = {'timestamp': self.get_server_time()}

        query_string = urlencode(params)
        signature = self._create_signature(query_string)

        headers = {'X-MEXC-APIKEY': self.api_key}
        url = f'{self.base_url}{endpoint}?{query_string}&signature={signature}'

        response = requests.get(url, headers=headers)
        return response.json()

    def save_to_file(self, data, filename):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        file_path = os.path.join(self.save_dir, f"{filename}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")


if __name__ == "__main__":
    client = MexcClient()

    info = client.get_account_info()
    client.save_to_file(info, "mexc_balance")
    print(json.dumps(info, indent=4))
