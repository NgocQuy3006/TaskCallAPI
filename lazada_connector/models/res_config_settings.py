from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lazada_api_key = fields.Char(
        string="Lazada API Key",
        config_parameter='lazada_connector.api_key'
    )
