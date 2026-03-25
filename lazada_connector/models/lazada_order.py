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