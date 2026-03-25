from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lazada_app_key = fields.Char(
        string="App Key",
        config_parameter='lazada.app_key'
    )

    lazada_app_secret = fields.Char(
        string="App Secret",
        config_parameter='lazada.app_secret'
    )

    lazada_access_token = fields.Char(
        string="Access Token",
        config_parameter='lazada.access_token'
    )