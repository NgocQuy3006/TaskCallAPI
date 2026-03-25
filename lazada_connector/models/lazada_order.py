from odoo import models, fields
from ..services.lazada_api import LazadaAPIService
import logging

_logger = logging.getLogger(__name__)


class LazadaOrder(models.Model):
    _name = 'lazada.order'
    _description = 'Lazada Order'

    name = fields.Char("Order ID")
    customer_name = fields.Char("Customer Name")
    total_amount = fields.Float("Total Amount")

    def action_test_lazada_api(self):
        service = LazadaAPIService(self.env)

        res = service.call_api(
            action='orders/get',
            params={'limit': 5}
        )

        _logger.info("TEST API: %s", res)


        if not res:
            return


        orders = res.get('data', {}).get('orders', [])


        for o in orders:
            order_id = o.get('order_id')


            if self.search([('name', '=', order_id)]):
                continue

            self.create({
                'name': order_id,
                'customer_name': o.get('customer_first_name'),
                'total_amount': float(o.get('price', 0)),
            })


        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Đã sync đơn hàng!',
                'type': 'success',
            }
        }