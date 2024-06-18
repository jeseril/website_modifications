# -- coding: utf-8 --

{
    'name': 'Website Modifications',
    'summary': 'Website Modifications',
    'version': '1.0.0',
    'category': 'Customizations',
    'website': 'https://www.linkedin.com/in/jesussebastian/',
    'author': 'Jesus Rincon <jeseril2213@gmail.com>',
    'depends': ['web','website_sale','product','stock'],
    'description': 'Sindication Content + Bulk attributes in ecommerce categories + Add TRM API Superfinanciera',
    'data': [
        "security/ir.model.access.csv",
        "security/website_modifications_security.xml",
        "views/product_template.xml",
        "views/website_sale_product.xml",
        "views/add_field_attribute.xml",
        "views/add_attributes.xml",
        "views/update_dolar.xml",
        #"views/add_menu_categories.xml",
        "views/add_field_visible_on_website.xml",
    ],
    'assets': {
        'web.assets_frontend': {
                'website_modifications/static/src/js/add_dolar_web.js',
                'website_modifications/static/src/css/styles.css',
        }
    },
    'application': False,
    'installable': True
}