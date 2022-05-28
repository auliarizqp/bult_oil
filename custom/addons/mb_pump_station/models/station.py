from odoo import api, fields, models, tools, _

class Station(models.Model):
    _name = "station.station"
    _description = "Station"
    
    name = fields.Char(string="Station")
    pump_line_ids = fields.One2many("station.pump", "station_id", string="Pump Line")
    
