from odoo import models, fields, api, exceptions, _
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError

class DiscountReport(models.AbstractModel):
    _name = 'report.mb_pump_station.report_discount'
    _description = ''    
    
    @api.model
    def _get_report_values(self, docids, data=None):
        return data

class DisocuntReportWizard(models.TransientModel):
    _name='te.discount.report.wizard'
    
    from_date = fields.Date(string="From Date",required= True)
    to_date = fields.Date(string = "To Date",required=True)
    partner_ids = fields.Many2many('res.partner',string = "Customers")

    def print_report(self):
        datas = self.read()[0]
        sdate = self.from_date
        edate = self.to_date

        if str(sdate) > str(edate):
            raise UserError("From Date must be less than To date")

        date_list = [str(sdate+timedelta(days=x)) for x in range((edate-sdate).days  + 1)]

        partners = self.partner_ids
        if not partners:
            partners = self.env['res.partner'].search([])
         
        list_of_dict = []
        for partner in partners:
            total_discount = 0
            total_paid_discount = 0
            total_balance = 0
            partner_wise_data_list = []
            invoices = self.env['account.move'].search(['|',('invoice_date','>',sdate),('invoice_date','=',sdate),'|',('invoice_date','<',edate),('invoice_date','=',edate),('partner_id','=',partner.id)])
            for date in date_list:
                related_invoices = invoices.filtered(lambda x:str(x.invoice_date) == date)
                if related_invoices:
                    related_invoices = related_invoices[0]
                
                move_lines = self.env['account.move'].search([('is_discount_entry','=',True)]).filtered(lambda x:str(x.date) == date).mapped('line_ids').filtered(lambda x:x.partner_id.id == partner.id and x.debit > 0)
                if move_lines:
                    move_lines = move_lines[0]
                    
                for line in related_invoices.invoice_line_ids:
                    partner_wise_data_list.append({
                        'vehicle_no' : related_invoices.vehicle_no,
                        'invoice_no' : related_invoices.name,
                        'invoice_date' : related_invoices.invoice_date,
                        'item' : line.product_id.name,
                        'quantity' :line.quantity,
                        'discount': line.discount_per_liter,
                        'total_discount' : line.total_discount,
                        'paid_discount' : move_lines.debit,
                        'balance' : move_lines.debit -  line.total_discount
                    })
                

                    total_discount = total_discount + line.total_discount
                    # total_paid_discount = total_paid_discount + move_lines.debit
                    # total_balance = total_balance + (move_lines.debit -  line.total_discount)
                if move_lines and not related_invoices:
                    partner_wise_data_list.append({
                        'vehicle_no' : '',
                        'invoice_no' : move_lines.move_id.ref,
                        'invoice_date' : move_lines.move_id.date,
                        'item' : '',
                        'quantity' :'',
                        'discount': 0,
                        'total_discount' : 0,
                        'paid_discount' : move_lines.debit,
                        'balance' : move_lines.debit -  0
                    })

                    total_paid_discount = total_paid_discount + move_lines.debit
                total_balance =  (total_paid_discount -  total_discount)
                

            
            list_of_dict.append({
                'partner_name' : partner.name,
                'partner_wise_data_list' :partner_wise_data_list,
                'total_discount' :total_discount,
                'total_paid_discount' :total_paid_discount,
                'total_balance' :total_balance
            })

        datas.update({
            'from_date':str(sdate),
            'to_date' : str(edate),
            'list_of_dict':list_of_dict,
            
        })
       
        return self.env.ref('mb_pump_station.action_report_discount').report_action([], data=datas)      