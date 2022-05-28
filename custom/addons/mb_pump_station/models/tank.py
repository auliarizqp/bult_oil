from odoo import api, fields, models, tools, _

class PumpTank(models.Model):
    _name = "pump.tank"
    _description = "Pump Tank"
    
    name = fields.Char(string="Tank")
    product_id = fields.Many2one("product.template", string="Product")
