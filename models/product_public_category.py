from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    visible_on_web = fields.Boolean('Visible On Web')

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    char_editable = fields.Boolean('Create unregistered attributes')