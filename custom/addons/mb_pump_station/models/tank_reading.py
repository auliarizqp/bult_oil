from odoo import api, fields, models, tools, _

class TankReading(models.Model):
    _name = "tank.reading"
    _description = "Tank Reading"
    _order = "id desc"
    name = fields.Char(string="Tank Reading Number",index=1, readonly=True, required=True, copy=False,default=lambda self: _('New'))
    tank_id = fields.Many2one("pump.tank", string="Tank")
    date = fields.Date(string="Date", required="1")
    t_opening_reading = fields.Float(string="Opening Reading")
    t_closing_reading = fields.Float(string="Closing Reading")
    user_id = fields.Many2one("res.users", string="User")
    shift_id = fields.Many2one("pump.shift", string="Shift")
    purchase = fields.Float(string="Purchase")
    t_expected_sales = fields.Float(string="Expected Sales")
    t_is_readonly = fields.Boolean(compute="_compute_tank_field_readonly")
    t_is_compute = fields.Boolean(string="Compute",
                                compute="tank_compute_all_in_one")
    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('tank.reading') or _('New')
        res = super(TankReading,self).create(vals)
        latest_record = self.search([('tank_id','=',res.tank_id.id),('id','!=',res.id)],order = "id desc",limit = 1)
        res.t_opening_reading = latest_record.t_closing_reading
        return res
     
    @api.depends("t_closing_reading")   
    def tank_compute_all_in_one(self):
        for record in self:
            record.t_is_compute = False
            record.t_expected_sales = 0.0
            total_sale = 0.0
            if record.t_closing_reading:
                total_sale = record.t_closing_reading - record.t_opening_reading
                record.t_expected_sales = total_sale
                
    def _compute_tank_field_readonly(self):
        for rec in self:
            rec.t_is_readonly = False
            abc = rec.env.user.has_group("mb_pump_station.group_edit_reading_manager")
            date = fields.Date.today()
            if not rec.env.user.has_group("mb_pump_station.group_edit_reading_manager") and rec.date < date:
                rec.t_is_readonly = True
