from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shopee_partner_id = fields.Char(
        string="Shopee Partner ID",
        config_parameter='shopee.partner_id'
    )
    shopee_partner_key = fields.Char(
        string="Shopee Partner Key",
        config_parameter='shopee.partner_key'
    )
    shopee_shop_id = fields.Char(
        string="Shopee Shop ID",
        config_parameter='shopee.shop_id'
    )
    shopee_access_token = fields.Char(
        string="Shopee Access Token",
        config_parameter='shopee.access_token'
    )