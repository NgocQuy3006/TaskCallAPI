import hashlib
import hmac
import time
import requests
import logging

_logger = logging.getLogger(__name__)


class LazadaAPIService:
    def __init__(self, env):
        self.env = env


    def _get_config(self):
        config = self.env['ir.config_parameter'].sudo()
        return {
            'app_key': config.get_param('lazada.app_key'),
            'app_secret': config.get_param('lazada.app_secret'),
            'access_token': config.get_param('lazada.access_token'),
            'base_url': config.get_param('lazada.base_url', 'https://api.lazada.vn/rest'),
        }


    def _sign(self, params, app_secret):
        sorted_params = sorted(params.items())
        sign_str = ''.join(f"{k}{v}" for k, v in sorted_params)

        return hmac.new(
            app_secret.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()


    def call_api(self, action, params=None, method="GET"):
        config = self._get_config()

        if not params:
            params = {}

        params.update({
            'app_key': config['app_key'],
            'timestamp': str(int(time.time() * 1000)),
            'access_token': config['access_token'],
            'sign_method': 'sha256',
        })

        params['sign'] = self._sign(params, config['app_secret'])

        url = f"{config['base_url']}?action={action}"

        try:
            if method == "GET":
                res = requests.get(url, params=params)
            else:
                res = requests.post(url, data=params)

            res.raise_for_status()
            return res.json()

        except Exception as e:
            _logger.error("Lazada API error: %s", str(e))
            return False