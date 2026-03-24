from odoo import models, fields
from odoo.exceptions import UserError
from ..services.shopee_api import ShopeeAPI
import logging

_logger = logging.getLogger(__name__)


class ShopeeOrder(models.Model):
    _name = 'shopee.order'
    _description = 'Shopee Order'

    name = fields.Char("Test")

    def action_test_api(self):
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

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Shopee API',
                'message': str(data),
                'type': 'success',
                'sticky': False,
            }
        }