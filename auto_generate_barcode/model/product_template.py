import barcode
import base64
import functools
import os
from datetime import datetime
from random import randrange
from barcode.writer import ImageWriter
from odoo import fields, models, api
import io

def ean_checksum(ean):
    code = list(ean)
    oddsum = evensum = total = 0
    for i in range(len(code)):
        if i % 2 == 0:
            evensum += int(code[i])
        else:
            oddsum += int(code[i])
    total = oddsum * 3 + evensum
    return int((10 - total % 10) % 10)

def sanitize_ean(random=True, prefix=None):
    if prefix:
        if random:
            numbers = [randrange(10) for x in range(8)]
        else:
            numbers = [int(a) for a in datetime.today().strftime('%d%H%M%S')]
        numbers = prefix + numbers

    else:
        if random:
            numbers = [randrange(10) for x in range(12)]
        else:
            numbers = [int(a) for a in datetime.today().strftime('%y%m%d%H%M%S')]

    numbers.append(ean_checksum(numbers))
    return ''.join(map(str, numbers))

def generate_ean(company, random=True, prefix=None, ean13=None):
        if not ean13:
            ean13 = sanitize_ean(random=random, prefix=prefix)
        return ean13

class Products(models.Model):
    _inherit = 'product.product'

    ean13_image = fields.Binary("Barcode Image", compute='_compute_ean13_image', store=True)

    @api.depends('barcode')
    def _compute_ean13_image(self):
        company = self.env.company
        for record  in self:
            if record.barcode:                
                options = {
                    'module_width': company.module_width or 0.2,
                    'module_height': company.module_height or 8.0,
                    'quiet_zone': company.quiet_zone or 0.0,            
                    
                    'background': company.background or '#FFFFFF',
                    'foreground': company.foreground or '#000000',

                    'write_text': company.write_text or False,
                    'font_size': company.font_size or 10,
                    'text_distance': company.text_distance or 0.3,
                }                
                ean = barcode.get('EAN13', record.barcode, writer=ImageWriter())
                img = ean.save('/tmp/' +  record.barcode, options)                
                r = base64.b64encode(open(img, 'rb').read())
                os.remove(img)
                record.ean13_image = r
            else:
                record.ean13_image = False
                record.barcode = False 

    def generate_ean_barcode(self, barcode=None):        
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company        
        if company.use_prefix and company.prefix:
            prefix = [int(a) for a in company.prefix]
            if company.generate_method == 'current_date':                
                ean13 = generate_ean(company, random=False, prefix=prefix, ean13=barcode)
            else:                
                ean13 = generate_ean(company, random=True, prefix=prefix, ean13=barcode)

        else:
            if company.generate_method == 'current_date':                
                ean13 = generate_ean(company, random=False, prefix=None, ean13=barcode)
            else:                
                ean13 = generate_ean(company, random=True, prefix=None, ean13=barcode)
                
        if not barcode:
            if not self.search([('barcode', '=', ean13)]):                
                return ean13
            else:                
                return False
        else:
            return ean13
    
    @api.model
    def create(self, vals):
        if self._context.get('company_id'):
            company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        else:
            company = self.env.company

        if company.on_product_creation:
            ean13 = self.generate_ean_barcode(vals.get('barcode'))
            if ean13:
                vals.update({
                    'barcode': ean13, 
                })
        return super(Products, self).create(vals)
    
    def generate_barcode(self):
        ctx = dict(self._context)
        for product in self:
            ean13 = None
            
            if product.company_id:
                ctx.update({
                    'company_id': product.company_id.id
                })
            else:
                company = self.env.company
                ctx.update({
                    'company_id': company.id
                })   

            if self._context.get('override_barcode'):                
                ean13 = product.with_context(ctx).generate_ean_barcode()
                while self.search([('barcode', '=', ean13)]):                    
                    ean13 = product.with_context(ctx).generate_ean_barcode()
            
            elif product.barcode:
                if not product.ean13_image:
                    ean13 = product.with_context(ctx).generate_ean_barcode(product.barcode)
                    
            else:                
                ean13 = product.with_context(ctx).generate_ean_barcode(product.barcode)
                while self.search([('barcode', '=', ean13)]):                    
                    ean13 = product.with_context(ctx).generate_ean_barcode(product.barcode)
            
            if ean13:
                product.write({
                    'barcode': ean13,                     
                })                
        return True
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    ean13_image = fields.Binary("Barcode Image", compute='_compute_ean13_image', store=True)

    @api.depends('barcode')
    def _compute_ean13_image(self):
        company = self.env.company
        for record  in self:
            if record.barcode:                
                options = {
                    'module_width': company.module_width or 0.2,
                    'module_height': company.module_height or 8.0,
                    'quiet_zone': company.quiet_zone or 0.0,            
                    
                    'background': company.background or '#FFFFFF',
                    'foreground': company.foreground or '#000000',

                    'write_text': company.write_text or False,
                    'font_size': company.font_size or 10,
                    'text_distance': company.text_distance or 0.3,
                }                
                ean = barcode.get('EAN13', record.barcode, writer=ImageWriter())
                img = ean.save('/tmp/' +  record.barcode, options)                
                r = base64.b64encode(open(img, 'rb').read())
                os.remove(img)
                record.ean13_image = r
            else:
                record.ean13_image = False
                record.barcode = False            
            
    def generate_ean_barcode(self, barcode=None):        
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company        
        if company.use_prefix and company.prefix:
            prefix = [int(a) for a in company.prefix]
            if company.generate_method == 'current_date':                
                ean13 = generate_ean(company, random=False, prefix=prefix, ean13=barcode)
            else:                
                ean13 = generate_ean(company, random=True, prefix=prefix, ean13=barcode)

        else:
            if company.generate_method == 'current_date':                
                ean13 = generate_ean(company, random=False, prefix=None, ean13=barcode)
            else:                
                ean13 = generate_ean(company, random=True, prefix=None, ean13=barcode)
                
        if not barcode:
            if not self.search([('barcode', '=', ean13)]):
                return ean13
            else:                
                return False
        else:
            return ean13

    @api.model
    def create(self, vals):
        if self._context.get('company_id'):
            company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        else:
            company = self.env.company

        if company.on_product_creation:
            ean13 = self.generate_ean_barcode(vals.get('barcode'))
            if ean13:
                vals.update({
                    'barcode': ean13, 
                })
        return super(ProductTemplate, self).create(vals)

    def generate_barcode(self):
        ctx = dict(self._context)
        for product in self:
            ean13 = None
            
            if product.company_id:
                ctx.update({
                    'company_id': product.company_id.id
                })
            else:
                company = self.env.company
                ctx.update({
                    'company_id': company.id
                })   

            if self._context.get('override_barcode'):                
                ean13 = product.with_context(ctx).generate_ean_barcode()
                while self.search([('barcode', '=', ean13)]):                    
                    ean13 = product.with_context(ctx).generate_ean_barcode()
            
            elif product.barcode:
                if not product.ean13_image:
                    ean13 = product.with_context(ctx).generate_ean_barcode(product.barcode)
                    
            else:                
                ean13 = product.with_context(ctx).generate_ean_barcode(product.barcode)
                while self.search([('barcode', '=', ean13)]):                    
                    ean13 = product.with_context(ctx).generate_ean_barcode(product.barcode)
            
            if ean13:
                product.write({
                    'barcode': ean13,                     
                })                
        return True