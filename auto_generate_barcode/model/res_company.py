from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    on_product_creation = fields.Boolean(string='Generate On Product Creation')
    use_prefix = fields.Boolean(string='Use 4 Digit Prefix')
    prefix = fields.Char(string='Barcode Prefix', size=4)
    generate_method = fields.Selection([
        ('random_number', "Using Random Number"),
        ('current_date', "Using Today's Date"),
    ], string='Barcode Create Method', required=True, default='random_number')
    module_width = fields.Float(string='Barcode Width In mm', digits=(16, 2), default=0.2,help='The width of one barcode module in mm as Float. Defaults to 0.2')
    module_height = fields.Float(string='Barcode Height In mm', digits=(16, 2), default=5.0,help='The height of the barcode modules in mm as Float. Defaults to 5.0.')
    quiet_zone = fields.Float(string='Space Before And After Barcode', digits=(16, 2), default=0.0, help='Distance on the left and on the right from the border to the first (last) barcode module in mm as float.')    
    background = fields.Char(string="Barcode Background Color", default='#FFFFFF', help='The background color of the created barcode as string. Defaults to white.')
    foreground = fields.Char(string="Barcode Foreground Color", default='#000000', help='The foreground and text color of the created barcode as string. Defaults to black.')
    write_text = fields.Boolean(string='Write EAN13 Below Image', default=True)
    font_size = fields.Integer(string='Font Size Of Text Under Barcode', default=10,help='Font size of the text under the barcode in pt as integer. Defaults 10.')
    text_distance = fields.Float(string='Distance Between Barcode and Text Under It', digits=(16, 2), default=0.3, help='Distance between the barcode and the text under it in mm as float. Defaults to 0.3')

    @api.constrains('prefix')
    def _check_valid_prefix(self):
        for obj in self:            
            if len(obj.prefix) == 4:
                try:
                    prefix = [int(a) for a in obj.prefix]
                except:
                    raise ValidationError(_("Barcode Prefix Should Be Integer(Number) with Length of Four Only !"))
            else:
                raise ValidationError(_("Barcode Prefix Lenght Should Be Four Only !"))