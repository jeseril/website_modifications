from odoo import models,exceptions


class SaleOrder(models.Model):
    _inherit = 'account.move'

    def post(self):
        # Asegúrate de que existe un producto vinculado y que tiene el campo is_dropshipping
        for order in self:
            if order.line_ids.sale_line_ids.order_id.order_line.purchase_line_ids.order_id.api_supplier_order:
                raise exceptions.UserError("Ya existe una orden de compra de dropshipping para este pedido.")
            if not order.line_ids.sale_line_ids.order_id.order_line.purchase_line_ids.order_id.api_supplier_order:
                if any(line.product_id.product_tmpl_id.is_dropshipping for line in order.invoice_line_ids):
                    # Obtener el proveedor en el account_move
                    supplier = self.invoice_line_ids.product_id.product_tmpl_id.variant_seller_ids.partner_id

                    api_credentials = self.env['api.credentials'].search([('partner_id', '=', supplier.id)])

                    if supplier == api_credentials.partner_id:

                        configuration_id = self.env['api.configuration'].search(
                            [('name', '=', 'RealizarPedido')])

                        configuration_id.mps_methods_ids.authenticate_api(account_move=self)





