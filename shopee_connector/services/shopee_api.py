import time
import hmac
import hashlib
import requests


class ShopeeAPI:
    def __init__(self, partner_id, partner_key, shop_id=None, access_token=None):
        self.partner_id = partner_id
        self.partner_key = partner_key
        self.shop_id = shop_id
        self.access_token = access_token
        self.base_url = "https://partner.shopeemobile.com"

    def _generate_sign(self, path, timestamp):
        base_string = f"{self.partner_id}{path}{timestamp}"
        return hmac.new(
            self.partner_key.encode(),
            base_string.encode(),
            hashlib.sha256
        ).hexdigest()

    def get_orders(self):
        path = "/api/v2/order/get_order_list"
        timestamp = int(time.time())

        sign = self._generate_sign(path, timestamp)

        url = f"{self.base_url}{path}"

        params = {
            "partner_id": self.partner_id,
            "timestamp": timestamp,
            "sign": sign,
            "shop_id": self.shop_id,
            "access_token": self.access_token,
        }

        response = requests.get(url, params=params)
        return response.json()