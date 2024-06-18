from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
class ProductPublicCategoryAttributes(models.Model):
    _inherit = 'product.public.category'

    attribute_ids = fields.Many2many('product.attribute', string='Attributes')

    html_code = fields.Char('Sindication Code')
    csv_file = fields.Binary(string="CSV File", filename="csv_filename")

    def write(self, vals):
        res = super(ProductPublicCategoryAttributes, self).write(vals)
        if 'attribute_ids' in vals:
            products = self.env['product.template'].search([('public_categ_ids', 'in', self.ids)])
            for product in products:
                product._update_attribute_lines()
        return res