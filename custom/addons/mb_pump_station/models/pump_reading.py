from pkg_resources import require
from odoo import api, fields, models, tools, _
from datetime import date,datetime

class PumpReading(models.Model):
    _name = "pump.reading"
    _description = "Pump Reading"
    _order = "id desc"
    
    name = fields.Char(string="Pump Reading Number",index=1, readonly=True, required=True, copy=False,default=lambda self: _('New'))
    pump_id = fields.Many2one("station.pump", string="Pump")
    tank_id = fields.Many2one(related=  "pump_id.tank_id",store = True)
    date = fields.Date(string="Date",required="1")
    p_opening_reading = fields.Float(string="Opening Reading")
    p_closing_reading = fields.Float(string="Closing Reading")
    user_id = fields.Many2one("res.users", string="User")
    shift_id = fields.Many2one("pump.shift", string="Shift")
    p_expected_sales = fields.Float(string="Expected Sales")
    is_readonly = fields.Boolean(compute="_compute_pump_field_readonly")
    sale_price = fields.Float(string="Price")
    total_sales = fields.Float(string="Total Sales")
    is_compute = fields.Boolean(string="Compute",
                                compute="pump_compute_all_in_one")
    

    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pump.reading') or _('New')
        res = super(PumpReading,self).create(vals)
        latest_record = self.search([('pump_id','=',res.pump_id.id),('id','!=',res.id)],order = "id desc",limit = 1)
        res.p_opening_reading = latest_record.p_closing_reading 
        return res
     
    @api.depends("p_closing_reading")    
    def pump_compute_all_in_one(self):
        for record in self:
            record.is_compute = False
            record.p_expected_sales = 0.0
            record.total_sales = 0.0
            total_sale = 0.0
            if record.p_closing_reading:
                total_sale = record.p_closing_reading - record.p_opening_reading
                record.p_expected_sales = total_sale
                record.total_sales = record.p_expected_sales*record.sale_price
                
    def _compute_pump_field_readonly(self):
        for rec in self:
            rec.is_readonly = False
            abc = rec.env.user.has_group("mb_pump_station.group_edit_reading_manager")
            date = fields.Date.today()
            if not rec.env.user.has_group("mb_pump_station.group_edit_reading_manager") and rec.date < date:
                rec.is_readonly = True
                
    @api.onchange("pump_id")
    def onchange_price(self):
        for record in self:
           if record.pump_id:
              record.sale_price = record.pump_id.tank_id.product_id.list_price
              
    
