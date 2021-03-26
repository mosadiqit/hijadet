# -*- coding: utf-8 -*-
#################################################################################
# Author      : CodersFort (<https://codersfort.com/>)
# Copyright(c): 2017-Present CodersFort.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://codersfort.com/>
#################################################################################

{
    "name": "Product Barcode Generator",
    "summary": " This application is generating product EAN13 barcode automatically (on product creation) or manually.",
    "version": "14.0.1",
    "description": """
    This application is generating product EAN13 barcode automatically (on product creation) or manually.

    You can create barcode in bulk for already created products, you have the option to select multiple products and create barcode or
    select multiple product categories and create the barcode for all products of the selected product category.

    - This module helps you to Auto Generate EAN13 Barcode with Following Benifits and Features

    - Benefits
        - Easy to generate new barcodes.
        - Barcode Images also generated.
        - Easy to select barcode type from general settings.
        - Easy to auto-generate barcode on product creation.
        - Easy to generate mass product barcode.
        - No special configuration required, install it, use it.
        - This module saves your important time.
        - It reduces human efforts.
    -Features
        - Auto generate EAN13 barcode using random number
        - Auto generate EAN13 barcode using today's date.
        - Auto generate EAN13 barcode in using some prefix.
        - Auto generate EAN13 barcode in different size.
        - Auto generate EAN13 barcode in different colors.
        - Manage EAN13 barcode font size, Space before and after, text below barcode, distance between them
        - Auto generate EAN13 bulk barcode by selecting multiple products.
        - Auto generate EAN13 bulk barcode by selecting multiple products categories.
        - Company wise barcode generation setting.
        - Product can be search by ean13 barcode.

    barcode product barcode auto generate product barcode ean13 auto generate product barcode auto generate product ean13 auto generate barcode product auto generate barcode ean13 auto product generate barcode auto generate ean13 product auto generate ean13 barcode auto product generate ean13 auto product barcode generate auto product barcode ean13 auto barcode generate product auto barcode generate ean13 auto barcode product generate auto product ean13 barcode auto product ean13 generate auto barcode product ean13 generate auto product barcode auto ean13 generate product auto barcode ean13 generate auto barcode ean13 product auto ean13 generate barcode auto ean13 product generate auto ean13 product barcode generate auto ean13 generate auto ean13 barcode generate auto ean13 barcode product generate auto barcode ean13 generate product auto ean13 product generate barcode generate product auto ean13 generate product barcode auto ean13 barcode generate product ean13 auto product generate ean13 barcode generate ean13 auto product generate product generate barcode ean13 auto barcode ean13 generate barcode product auto ean13 generate ean13 auto barcode generate ean13 product auto ean13 product barcode ean13 barcode product auto barcode ean13 barcode auto ean13 barcode product ean13 barcode auto generate barcode product ean13 product barcode generate barcode product auto product generate barcode ean13 generate barcode auto barcode product ean13 product auto generate auto barcode product barcode generate barcode auto generate product barcode generate barcode ean13 barcode auto product barcode generate ean13 generate auto product generate auto barcode auto barcode auto ean13 barcode ean13 generate ean13 product generate ean13 generate product ean13 barcode product ean13 auto generate ean13 generate barcode ean13 product ean13 barcode auto ean13 generate ean13 barcode generate auto product auto product ean13 generate product barcode ean13 barcode ean13 auto generate auto barcode ean13 auto ean13 product auto product ean13 auto barcode ean13 product barcode ean13 auto product ean13 auto generate product generate barcode product auto
    """,    
    "author": "CodersFort",
    "maintainer": "Ananthu Krishna",
    "license" :  "Other proprietary",
    "website": "http://www.codersfort.com",
    "images": ["images/auto_generate_barcode.png"],
    "category": "Tools",
    "depends": ["base", "product"],
    "data": [
        "security/auto_generate_barcode_security.xml",
        'security/ir.model.access.csv',
        "wizard/generate_product_barcode_view.xml",
        "wizard/generate_product_category_barcode_view.xml",
        "views/res_company_view.xml",
        "views/product_view.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": True,
    "price"                :  7,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",   
}
