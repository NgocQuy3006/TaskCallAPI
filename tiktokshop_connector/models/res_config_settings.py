from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tiktok_app_key = fields.Char("App Key")
    tiktok_app_secret = fields.Char("App Secret")
    tiktok_access_token = fields.Char("Access Token")

    def set_values(self):
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()

        config.set_param('tiktok.app_key', self.tiktok_app_key)
        config.set_param('tiktok.app_secret', self.tiktok_app_secret)
        config.set_param('tiktok.access_token', self.tiktok_access_token)

    def get_values(self):
        res = super().get_values()
        config = self.env['ir.config_parameter'].sudo()

        res.update(
            tiktok_app_key=config.get_param('tiktok.app_key'),
            tiktok_app_secret=config.get_param('tiktok.app_secret'),
            tiktok_access_token=config.get_param('tiktok.access_token'),
        )
        return res