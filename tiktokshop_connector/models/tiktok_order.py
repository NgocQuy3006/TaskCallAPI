from odoo import models, fields
from odoo.exceptions import UserError
from ..services.tiktok_api import TikTokAPI


class TikTokOrder(models.Model):
    _name = 'tiktok.order'
    _description = 'TikTok Order'

    name = fields.Char("Order ID")
    customer_name = fields.Char("Customer")
    total_amount = fields.Float("Amount")

    def action_sync_tiktok_orders(self):
        config = self.env['ir.config_parameter'].sudo()

        app_key = config.get_param('tiktok.app_key')
        app_secret = config.get_param('tiktok.app_secret')
        access_token = config.get_param('tiktok.access_token')

        if not all([app_key, app_secret, access_token]):
            raise UserError("Chưa cấu hình TikTok API")

        api = TikTokAPI(app_key, app_secret, access_token)

        data = api.call_api(
            path="/orders/search",
            params={"page_size": 5}
        )

        orders = data.get('data', {}).get('orders', [])


        for o in orders:
            if self.search([('name', '=', o.get('order_id'))]):
                continue

            self.create({
                'name': o.get('order_id'),
                'customer_name': o.get('buyer_name'),
                'total_amount': float(o.get('total_amount', 0)),
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'TikTok',
                'message': 'Đã sync đơn TikTok!',
                'type': 'success',
            }
        }