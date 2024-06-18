from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

class Website(models.Model):
    _inherit = 'website'
    def get_visible_parent(self):
        parent_ids = []
        visible_categories_ids = self.env['product.public.category'].sudo().search([('visible_on_web', '=', True)])
        for category in visible_categories_ids:
            if not len(category.parent_id) > 0:
                parent_ids.append(category.id)
        visible_categories_ids = self.env['product.public.category'].sudo().search([('id', 'in', parent_ids)])
        return visible_categories_ids
    def get_visible_childs(self, parent_id):
        childs = self.env['product.public.category'].sudo().search([('parent_id', '=', parent_id),('visible_on_web', '=', True)])
        return childs
    def get_visible_grandchild(self, childs_id):
        grand_child = self.env['product.public.category'].sudo().search([('parent_id', '=', childs_id),('visible_on_web', '=', True)])
        return grand_child