# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from lxml import etree

from openerp import models, fields, api
from openerp.osv.orm import setup_modifiers


# class /users/moylop260/odoo/dynamic_view(models.Model):
#     _name = '/users/moylop260/odoo/dynamic_view./users/moylop260/odoo/dynamic_view'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class DynamicView(models.TransientModel):
    _name = 'dynamic.view'
    # _auto = False

    employee_id = fields.Many2one('hr.employee', store=False)
    dummy = fields.Char(store=False)
    # dummy2 = fields.Text(store=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(DynamicView, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            node = doc.xpath("//field[@name='dummy']")[0]
            parent_node = node.getparent()
            date_work = datetime.now()
            def get_states_field():
                return fields.Selection([
                        ('present_for_duty', 'Present for Duty'),
                        ('recreational', 'Recreational'),
                    ], store=False, default='present_for_duty')
            for i in range(10):
                date_work += timedelta(days=1)
                date_name = date_work.strftime('%b %d')
                t_date_name = date_name.lower().replace(' ', '_')
                self._add_field(t_date_name, get_states_field())
                date_node = etree.fromstring('<field name="%s" widget="selection" string="%s"/>' % (t_date_name, date_name))
                parent_node.insert(1, date_node)
            result['arch'], result['fields'] = self.env['ir.ui.view'].postprocess_and_fields(self._name, doc, None)

        return result

    @api.model
    def create(self, values):
        print values
        res = super(DynamicView, self).create(values)
        return res
