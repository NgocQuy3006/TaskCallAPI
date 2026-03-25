from odoo import models, fields
from odoo.exceptions import UserError
from ..services.shopee_api import ShopeeAPI
import logging

_logger = logging.getLogger(__name__)


class ShopeeOrder(models.Model):
    _name = 'shopee.order'
    _description = 'Shopee Order'

    name = fields.Char("Order ID")
    customer_name = fields.Char("Customer Name")
    total_amount = fields.Float("Total Amount")

    def action_sync_shopee_orders(self):
        config = self.env['ir.config_parameter'].sudo()

        partner_id = config.get_param('shopee.partner_id')
        partner_key = config.get_param('shopee.partner_key')
        shop_id = config.get_param('shopee.shop_id')
        access_token = config.get_param('shopee.access_token')

        if not all([partner_id, partner_key, shop_id, access_token]):
            raise UserError("Vui lòng cấu hình Shopee trong Settings trước!")

        api = ShopeeAPI(
            partner_id=int(partner_id),
            partner_key=partner_key,
            shop_id=int(shop_id),
            access_token=access_token
        )

        data = api.get_orders()

        _logger.info("Shopee API response: %s", data)

        if not data:
            return


        orders = data.get('response', {}).get('order_list', [])

        for o in orders:
            order_id = o.get('order_sn')


            if self.search([('name', '=', order_id)]):
                continue

            self.create({
                'name': order_id,
                'customer_name': o.get('buyer_username'),
                'total_amount': float(o.get('total_amount', 0)),
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Shopee',
                'message': 'Đã sync đơn Shopee!',
                'type': 'success',
            }
        }