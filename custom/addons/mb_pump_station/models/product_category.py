from odoo import api, fields, models, tools, _

class ProductCategory(models.Model):
    _inherit = "product.category"
    
    is_fule = fields.Boolean(string="Is A Fule Category")
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    is_fule = fields.Boolean(related="categ_id.is_fule", string="Fule", store=True)

