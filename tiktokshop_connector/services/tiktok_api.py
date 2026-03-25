import time
import hashlib
import hmac
import requests
import logging

_logger = logging.getLogger(__name__)


class TikTokAPI:
    def __init__(self, app_key, app_secret, access_token):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token
        self.base_url = "https://open-api.tiktokglobalshop.com"

    def _sign(self, path, params):
        sorted_params = sorted(params.items())
        param_str = ''.join(f"{k}{v}" for k, v in sorted_params)

        sign_str = f"{path}{param_str}"

        return hmac.new(
            str(self.app_secret).encode(),   
            sign_str.encode(),
            hashlib.sha256
        ).hexdigest()

    def call_api(self, path, params=None):
        if not params:
            params = {}

        params.update({
            'app_key': self.app_key,
            'timestamp': int(time.time()),
            'access_token': self.access_token
        })

        params['sign'] = self._sign(path, params)

        url = f"{self.base_url}{path}"

        try:
            res = requests.get(url, params=params, timeout=15)


            _logger.info("TikTok URL: %s", res.url)
            _logger.info("Status: %s", res.status_code)
            _logger.info("Response: %s", res.text)


            if res.status_code != 200:
                return {
                    'error': 'HTTP Error',
                    'status': res.status_code,
                    'text': res.text
                }


            try:
                return res.json()
            except Exception:
                return {
                    'error': 'Not JSON response',
                    'status': res.status_code,
                    'text': res.text
                }

        except Exception as e:
            _logger.error("TikTok API Error: %s", str(e))
            return {
                'error': str(e)
            }
