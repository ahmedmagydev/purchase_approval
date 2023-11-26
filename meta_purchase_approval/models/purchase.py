# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import json


select=[
        ('draft', 'Quotation'),
        ('sent', 'RFQ Sent'),
        ('first_approval', 'Approval 1'),
        ('second_approval', 'Approval 2'),
        ('third_approval', 'Approval 3'),
        ('fourth_approval', 'Approval 4'),
        
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ]

class PurchaseOrder(models.Model):
    
    _inherit = 'purchase.order'


    state = fields.Selection(select, string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    state2=fields.Selection(select, string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    
    approval=fields.Boolean(string="Approval Status",compute="approval_computed")
    total_min_amount=fields.Monetary(compute="computed_amont",readonly=True)
    
  
            
    @api.depends("total_min_amount") 
    def computed_amont(self):
         
            config_settings =  self.company_id.po_double_validation_amount

            
            self.total_min_amount = config_settings
            
    def operation_send_approve(self):
        
       

        
        return self.write({'state': 'first_approval'}),self.write({'state2': 'first_approval'})
        
        
    # def operation_send_approve(self):
    #     return self.write({'state': 'first_approval'})
    

    def first_approval_button(self):
         
      
      
      
     return self.write({'state': 'second_approval'}),self.write({'state2': 'second_approval'})
      
            

    def first_approval_reject(self):
       

        return self.write({'state': 'cancel'})
    # @api.depends('approval')
    def approval_computed(self):
        if self.amount_total >= self.total_min_amount:
            self.approval = True
        else:
            self.approval = False    
    
    def second_approval_button(self):
        
        if self.approval == True:
            

            return  self.write({'state': 'third_approval'}),self.write({'state2': 'third_approval'})
        else:
          
          return  self.write({'state': 'purchase'}),self.write({'state2':'purchase'})
    
    def second_approval_reject(self):
       

        return self.write({'state': 'cancel'}),self.write({'state2': 'cancel'})
    
    def third_approval_button(self):
        

        return self.write({'state': 'fourth_approval'}),self.write({'state2': 'fourth_approval'})
   
    
    def third_approval_reject(self):
        

        return self.write({'state': 'cancel'}),self.write({'state2': 'cancel'})
    
    def fourth_approval_button(self):
        
        return self.write({'state': 'purchase'}),self.write({'state2': 'purchase'})
    
    
    def fourth_approval_reject(self):
        

        return self.write({'state': 'cancel'}),self.write({'state2': 'cancel'})
    def button_confirm(self):

        for order in self:
            if order.state not in ['draft', 'sent','purchase' ]:
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