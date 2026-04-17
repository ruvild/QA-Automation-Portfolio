"""
Pionex API Client
Handles authentication and retrieval of spot account balances.
Used as a data source for the Portfolio Dashboard ETL pipeline.
"""

import os
import time
import hmac
import hashlib
import requests
import json
from dotenv import load_dotenv

load_dotenv()


class PionexClient:
    def __init__(self):
        self.api_key = os.getenv('PIONEX_KEY')
        self.api_secret = os.getenv('PIONEX_API_SECRET')
        self.base_url = 'https://api.pionex.com'
        self.save_dir = os.path.join(os.getcwd(), "Responses")

    def _generate_signature(self, method, path_url):
        """Pionex specific: Concatenates METHOD and PATH_URL for signing."""
        full_request_string = f"{method.upper()}{path_url}"
        return hmac.new(
            self.api_secret.encode(), full_request_string.encode(), hashlib.sha256
        ).hexdigest()

    def get_balances(self):
        endpoint = "/api/v1/account/balances"
        timestamp = int(time.time() * 1000)

        # Pionex requires params sorted and joined with ? for the signature
        path_url = f"{endpoint}?timestamp={timestamp}"

        signature = self._generate_signature("GET", path_url)

        headers = {'PIONEX-KEY': self.api_key, 'PIONEX-SIGNATURE': signature}

        url = f"{self.base_url}{path_url}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def save_to_file(self, data, filename):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        file_path = os.path.join(self.save_dir, f"{filename}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")


if __name__ == "__main__":
    client = PionexClient()

    try:
        balances = client.get_balances()
        client.save_to_file(balances, "pionex_balances")
        print("Balances retrieved successfully.\n")
        print(json.dumps(balances, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")
