import base64
import io
import xlrd
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

class Add_Attributes(models.Model):
    _name = 'add.attributes'

    excel_file = fields.Binary(string="Excel File", filename="excel_filename")

    def import_attribute_lines_from_excel(self):
        if self.excel_file:
            decoded_data = base64.b64decode(self.excel_file)
            io_data = io.BytesIO(decoded_data)

            workbook = xlrd.open_workbook(file_contents=io_data.getvalue())
            sheet = workbook.sheet_by_index(0)

            for row_num in range(1, sheet.nrows):
                try:
                    row = sheet.row_values(row_num)
                    if len(row) < 3:
                        raise UserError("Incomplete Excel Row")

                    product_id = str(row[0]).strip()
                    attribute_name = str(row[1]).strip()
                    value_names = [str(value).strip() for value in
                                   str(row[2]).split('|')]

                    product = self.env['product.template'].browse(int(product_id))
                    if not product.exists():
                        raise UserError(f"A product with ID '{product_id}' was not found.")

                    attribute = self.env['product.attribute'].search([('name', '=', attribute_name)], limit=1)
                    if not attribute:
                        raise UserError(f"An attribute with the name '{attribute_name}' was not found.")

                    if attribute_name == 'SKU':
                        if hasattr(product,
                                   'sku') and product.sku:
                            value_names = [product.sku]
                        else:
                            pass

                    value_objs = []
                    for value_name in value_names:
                        value_obj = self.env['product.attribute.value'].search(
                            [('name', '=', value_name), ('attribute_id', '=', attribute.id)], limit=1)
                        if not value_obj:
                            if attribute.char_editable:
                                value_obj = self.env['product.attribute.value'].create({
                                    'name': value_name,
                                    'attribute_id': attribute.id,
                                })
                            else:
                                raise UserError(
                                    f"Value '{value_name}' not found in the database for attribute '{attribute_name}' on product '{product.name}'.")
                        value_objs.append(value_obj)

                    value_ids = [(6, 0, [value.id for value in value_objs])]

                    existing_attribute_lines = product.attribute_line_ids.filtered(
                        lambda line: line.attribute_id == attribute)

                    if existing_attribute_lines:
                        existing_attribute_lines.write({'value_ids': value_ids})
                    else:
                        product.attribute_line_ids.create({
                            'attribute_id': attribute.id,
                            'value_ids': value_ids,
                        })
                except Exception as e:
                    raise UserError(f"Error during import: {e}")
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        self.excel_file = False
        return True