# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class PumpReading(models.TransientModel):
    _name = "tank.reading.wizard"
    _description = 'Generate Tank Reading Reports'

    from_date = fields.Date('From Date',required=True)
    to_date = fields.Date('To Date',required=True)

    tank_ids = fields.Many2many('pump.tank', string='Tanks')
    station_ids = fields.Many2many('station.station', string='Stations')
    shit_ids = fields.Many2many('pump.shift', string='Shifts')


    def action_generate_tank_report(self):
        tank_record_list = []
        station_wise_tank_list = []
        if self.from_date > self.to_date:
            raise UserError(
                _('From date must be less than To date.')
            )
            
        else:        
            # PREPARE LIST OF TANKS RELATED TO STATION FOR FITLER STATION WISE
            if self.station_ids:
                for station in self.station_ids:
                    if station.pump_line_ids:
                        for line in station.pump_line_ids:
                            station_wise_tank_list.append(line.tank_id.id)
                        # station_wise_tank_list.append(station.pump_line_ids.mapped('tank_id').id)
            # PREPARE LIST OF TANKS RELATED TO STATION
            if self.tank_ids and self.station_ids:
                for tank_id in self.tank_ids:
                    if tank_id.id in station_wise_tank_list:
                        tank_record_list.append(tank_id.id)
            else:
                # GET ALL TANKS RECORDS
                if self.tank_ids:
                    for tank in self.tank_ids:
                        tank_record_list.append(tank.id)
                else:
                    all_tank_records = self.env['pump.tank'].search([])
                    for tank in all_tank_records:
                        tank_record_list.append(tank.id)

            
            # GET ALL SHITS
            get_all_shits = self.env['pump.shift'].search([])

            data = {'tank_records':tank_record_list,'shits':self.shit_ids.ids if self.shit_ids.ids else get_all_shits.ids,'from_date':self.from_date,'to_date':self.to_date}                        
            return self.env.ref('mb_pump_station.action_report_tank_report').report_action(self, data=data)