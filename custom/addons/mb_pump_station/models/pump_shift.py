from odoo import api, fields, models, tools, _

class PumpShift(models.Model):
    _name = "pump.shift"
    _description = "Pump Shift"
    
    name = fields.Char(string="Shift")
