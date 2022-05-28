from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    discount_per_liter = fields.Float(string='Discount Per Liter',)