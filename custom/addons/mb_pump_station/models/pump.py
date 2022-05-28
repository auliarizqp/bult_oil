from odoo import api, fields, models, tools, _

class StationPump(models.Model):
    _name = "station.pump"
    _description = "Station Pump"
    
    name = fields.Char(string="Pump")
    station_id = fields.Many2one("station.station",
                                 string="Station")
    tank_id = fields.Many2one("pump.tank", string="Tank")
    
