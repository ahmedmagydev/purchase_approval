# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import json
class PurchaseOrder(models.Model):
    
    _inherit = 'purchase.order'


    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'RFQ Sent'),
        ('first_approval', 'Approval 1'),
        ('second_approval', 'Approval 2'),
        ('third_approval', 'Approval 3'),
        ('fourth_approval', 'Approval 4'),
        
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

  
    total_min_amount=fields.Monetary(compute="computed_amont",readonly=True)
    @api.depends("total_min_amount") 
    def computed_amont(self):
         
            config_settings =  self.company_id.po_double_validation_amount

            
            self.total_min_amount = config_settings
            
    def operation_send_approve(self):
        
       

        return self.write({'state': 'first_approval'})
    # def operation_send_approve(self):
    #     return self.write({'state': 'first_approval'})
    

    def first_approval(self):
         
      
      
      
      self.write({'state': 'second_approval'})
      
            
    # def first_approval(self):
    #     return self.write({'state': 'second_approval'})
    
    def first_approval_reject(self):
       

        return self.write({'state': 'cancel'})
    
    def second_approval(self):
        if self.amount_total >= self.total_min_amount:

          self.write({'state': 'third_approval'})
        else:
          self.write({'state': 'purchase'})
    
    def second_approval_reject(self):
       

        return self.write({'state': 'cancel'})
    
    def third_approval(self):
        

        return self.write({'state': 'fourth_approval'})
   
    
    def third_approval_reject(self):
        

        return self.write({'state': 'cancel'})
    
    def fourth_approval(self):
        
        return self.write({'state': 'purchase'})
    
    
    def fourth_approval_reject(self):
        

        return self.write({'state': 'cancel'})
    def button_confirm(self):

        for order in self:
            if order.state not in ['draft', 'sent', 'purchase',]:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.company.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'purchase'})
        return True


    #Sree Joaynto Chandro Barmon

