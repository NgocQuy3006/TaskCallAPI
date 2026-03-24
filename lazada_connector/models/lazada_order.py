from odoo import models, fields
from odoo.exceptions import UserError
import requests

class LazadaOrder(models.Model):
    _name = 'lazada.order'
    _description = 'Lazada Order'

    name = fields.Char(string='Order ID', required=True)
    customer_name = fields.Char(string='Customer')
    total_amount = fields.Float(string='Total Amount')

    def action_test_lazada_api(self):

        api_key = self.env['ir.config_parameter'].sudo().get_param('lazada_connector.api_key')

        if not api_key:
            raise UserError("Chưa nhập API Key trong Settings")

        try:

            url = "https://httpbin.org/get"
            response = requests.get(url, params={"api_key": api_key}, timeout=10)

            if response.status_code == 200:

                raise UserError(" API OK\n\n" + response.text[:300])
            else:
                raise UserError(" API FAIL: %s" % response.status_code)

        except Exception as e:
            raise UserError("Lỗi kết nối: %s" % str(e))
