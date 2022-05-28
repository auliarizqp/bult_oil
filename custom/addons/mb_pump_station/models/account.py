from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # fixed_discount = fields.Float(string="Fixed Disc.", digits="Product Price", default=0.000)

    discount_per_liter = fields.Float(string='Discount Per Liter',)
    total_discount = fields.Float(string = "Total Discount",)
    price_after_discount = fields.Float(string = "Price After Disocunt",)
    pump_id = fields.Many2one('station.pump',string = "Pump")
    is_discount_line = fields.Boolean()

    @api.onchange('quantity', 'discount_per_liter', 'price_unit', 'tax_ids')
    def tm_onchange_price_subtotal(self):
        for line in self:
            if not line.move_id.is_invoice(include_receipts=True):
                continue

            res = {}

            # Compute 'price_subtotal'.
            line_discount_price_unit = line.price_unit
            if line.discount_per_liter == 0:
                line.discount_per_liter = line.partner_id.discount_per_liter

            if line.discount_per_liter != 0:
                line.total_discount = line.discount_per_liter * line.quantity
                line_discount_price_unit = line.price_after_discount =line.price_unit - line.discount_per_liter

            # subtotal = line.quantity * line_discount_price_unit

            # # Compute 'price_total'.
            # if line.tax_ids:
            #     taxes_res = line.tax_ids._origin.with_context(force_sign=1).compute_all(line_discount_price_unit,
            #         quantity=line.quantity, currency=line.currency_id, product=line.product_id, partner=line.partner_id, is_refund=line.move_id.move_type in ('out_refund', 'in_refund'))
            #     res['price_subtotal'] = taxes_res['total_excluded']
            #     res['price_total'] = taxes_res['total_included']
            # else:
            #     res['price_total'] = res['price_subtotal'] = subtotal
            # #In case of multi currency, round before it's use for computing debit credit
            # if line.currency_id:
            #     res = {k: line.currency_id.round(v) for k, v in res.items()}
            
            # line.update(res)

            # if line.move_id.move_type in line.move_id.get_outbound_types():
            #     sign = 1
            # elif line.move_id.move_type in line.move_id.get_inbound_types():
            #     sign = -1
            # else:
            #     sign = 1

            # amount_currency = line.price_subtotal * sign
            # balance = line.currency_id._convert(amount_currency, line.move_id.company_id.currency_id, line.move_id.company_id, line.move_id.date or fields.Date.context_today(self))
            # line.update(
            #      {
            #     'amount_currency': amount_currency,
            #     'currency_id': line.currency_id.id,
            #     'debit': balance > 0.0 and balance or 0.0,
            #     'credit': balance < 0.0 and -balance or 0.0,
            # }
            # )
            
    
class AccountMove(models.Model):
    _inherit = 'account.move'

    vehicle_no = fields.Char(string = "Vehicle")
    is_discount_entry = fields.Boolean(string = "Is Discount Entry")

    def _recompute_dynamic_lines(self, recompute_all_taxes=False, recompute_tax_base_amount=False):

        res = super(AccountMove,self)._recompute_dynamic_lines(recompute_all_taxes, recompute_tax_base_amount)

        for invoice in self:

            
            if self.env.company.disc_debit_account_id and self.env.company.disc_credit_account_id and self.move_type == 'out_invoice':
            
                discount_lines = invoice.line_ids.filtered('is_discount_line')
                
                invoice.line_ids -= discount_lines
                total_discount = sum(invoice.invoice_line_ids.mapped('total_discount'))


                create_method = self.env['account.move.line'].new or self.env['account.move.line'].create
                te_rounding_line = create_method({
                    'account_id' :  self.env.company.disc_debit_account_id.id,
                    'debit': total_discount,
                    'credit':0.0,
                    'name': ' ',
                    'partner_id': invoice.partner_id.id,
                    'exclude_from_invoice_tab':True,
                    'is_rounding_line':False,
                    'is_discount_line' : True
                    })

                invoice.line_ids += te_rounding_line

                te_rounding_line = create_method({
                    'account_id' :  self.env.company.disc_credit_account_id.id,
                    'debit': 0.0,
                    'credit':total_discount,
                    'name': ' ',
                    'partner_id': invoice.partner_id.id,
                    'exclude_from_invoice_tab':True,
                    'is_rounding_line':False,
                    'is_discount_line' : True
                    })

                invoice.line_ids += te_rounding_line

                unnecessary_line = invoice.line_ids.filtered(lambda x:x.debit == 0 and x.credit == 0)
                invoice.line_ids -= unnecessary_line
            
                        

        return res

    

    