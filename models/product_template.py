import base64
import io
import csv
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError


class ProductContentTemplate(models.Model):
    _inherit = "product.template"

    html_code = fields.Char('Sindication Code')
    attribute_line_ids = fields.One2many('product.template.attribute.line', 'product_tmpl_id', string='Attributes')
    product_variant_id = fields.Many2one('product.product', 'Product', compute='_compute_product_variant_id', store=True)

    @api.onchange('public_categ_ids')
    def _onchange_public_categ_ids(self):
        self._update_attribute_lines()
    @api.model
    def create(self, vals):
        template = super(ProductContentTemplate, self).create(vals)
        template._update_attribute_lines()
        return template

    def write(self, vals):
        res = super(ProductContentTemplate, self).write(vals)
        if 'public_categ_ids' in vals:
            self._update_attribute_lines()
        return res

    def _update_attribute_lines(self):
        for product_template in self:
            existing_attribute_lines = product_template.attribute_line_ids.filtered(lambda line: line.attribute_id in product_template.public_categ_ids.mapped('attribute_ids'))
            existing_attributes = existing_attribute_lines.mapped('attribute_id')
            for category in product_template.public_categ_ids:
                for attribute in category.attribute_ids:
                    if attribute not in existing_attributes:
                        values = {'attribute_id': attribute.id}
                        if attribute.value_ids:
                            default_value = attribute.value_ids.filtered(lambda x: x.name == '_')
                            if default_value:
                                values['value_ids'] = [(6, 0, [default_value.id])]
                        existing_attribute_lines += self.env['product.template.attribute.line'].new(values)
            product_template.attribute_line_ids = existing_attribute_lines

    def _create_variant_ids(self):
        for tmpl_id in self:
            if len(tmpl_id.product_variant_ids) > 1:
                products_with_valid_variant = self.env['product.product'].search([
                    ('product_tmpl_id', '=', tmpl_id.id),
                    ('valid_variant', '=', True)
                ])
                tmpl_id.write({
                    'product_variant_ids': [(6, 0, products_with_valid_variant.ids)]
                })
        return super(ProductContentTemplate, self)._create_variant_ids()

    def clear_variant_attributes(self):
        for product in self.product_variant_ids:
            product.write({'attribute_value_ids': [(5, 0, 0)]})


class ProductUnlinkModification(models.Model):
    _inherit = "product.product"

    product_content_template_id = fields.Many2one('product.template', 'Product Template')
    valid_variant = fields.Boolean(string='Valid variant')

    def _unlink_or_archive(self, check_access=True):
        for product in self:
            product_content_template = product.product_content_template_id
            if len(product_content_template.product_variant_id) > 1:
                for variant in product_content_template.product_variant_id:
                    if not variant.valid_variant:
                        res = super(ProductUnlinkModification, variant)._unlink_or_archive()
            elif product.id != product_content_template.product_variant_id.id and not product.valid_variant:
                res = super(ProductUnlinkModification, product)._unlink_or_archive()

