



from odoo import models, fields, api

class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    
    # Cranes Information
    serial_no=fields.Char(string="Serial NO")
    manufacturer=fields.Many2one("fleet.vehicle.model.brand")
    class_code=fields.Char(string="FA Class Code :")
    supclass_code=fields.Char(string="FA Subclass Code :")
    
    @api.model
    def create(self, vals):
        # Create the asset first
        asset = super(AccountAsset, self).create(vals)

        # Create a product with the same name
        product_vals = {
            'name':asset.name,
            'asset_id': asset.id,
            'type': 'product',
           
        }
        self.env['product.template'].create(product_vals)

        return asset

import logging

_logger = logging.getLogger(__name__)


class RentalOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _onchange_product_id(self):
    #    _logger.error("============= order_line ============.%s",self.order_line)

        
       for rec in self:
    #        _logger.error("============= order_line ============.%s",self.order_line)
    #        _logger.error("============= analytic_distribution ============.%s",self.order_line.analytic_distribution)
    #        _logger.error("============= order_line.product_template_id.asset_id.analytic_distribution  ============.%s",self.order_line.product_template_id.asset_id.analytic_distribution )
    #        _logger.error("============= order_line.product_template_id.asset_id.analytic_distribution  ============.%s",self.order_line.product_template_id.asset_id )

           rec.order_line.analytic_distribution = rec.order_line.product_template_id.asset_id.analytic_distribution     

class Product_relate(models.Model):
    _inherit='product.template'
    
    
    asset_id = fields.Many2one('account.asset')
    
    #Carnes Information
    product_group_code = fields.Char(string="Product Group Code")
    capacity_code = fields.Char(string="Capacity Code")
    manufacturer_code = fields.Char(string="Manufacturer Code")
    manufacturer = fields.Many2one("fleet.vehicle.model.brand", string="Manufacturer", related='asset_id.manufacturer')
    serial_no = fields.Char(string="Serial NO", related='asset_id.serial_no')
    
    
    #cost
    cost=fields.Monetary(string="Cost" , related='asset_id.original_value')
    
    # python3 odoo-bin -c conf/odoo.conf -d kaizenac