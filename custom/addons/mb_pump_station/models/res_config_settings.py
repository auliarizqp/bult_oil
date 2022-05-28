from odoo import models,fields,api,_
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'

    disc_debit_account_id = fields.Many2one('account.account',string = "Discount Debit Account")
    disc_credit_account_id = fields.Many2one('account.account',string = "Discount Credit Account")


# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     disc_debit_account_id = fields.Many2one('account.account',string = "Discount Debit Account",related = "company_id.disc_debit_account_id",readonly = False)
#     disc_credit_account_id = fields.Many2one('account.account',string = "Discount Credit Account",related = "company_id.disc_credit_account_id",readonly = False)