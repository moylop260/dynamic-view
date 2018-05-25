# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from lxml import etree

from openerp import models, fields, api
from openerp.osv.orm import setup_modifiers
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


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
    field_view_definition = '<field name="%s"/>'

    @staticmethod
    def get_field_states(label):
        return fields.Selection([
            ('present_for_duty', 'Present for Duty'),
            ('recreational', 'Recreational'),
        ], default='present_for_duty', string=label)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(DynamicView, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            node = doc.xpath("//field[@name='employee_id']")[0]
            parent_node = node.getparent()
            date_work = datetime.now()
            node_work = node
            for i in range(10):
                date_name = date_work.strftime('%b %d')
                t_date_name = date_work.strftime(DEFAULT_SERVER_DATE_FORMAT)
                self._add_field(t_date_name, DynamicView.get_field_states(date_name))
                date_node = etree.fromstring(
                    DynamicView.field_view_definition % t_date_name)
                parent_node.insert(parent_node.index(node) + 1, date_node)
                date_work += timedelta(days=1)
                node_work = date_node
            result['arch'], result['fields'] = (
                self.env['ir.ui.view'].postprocess_and_fields(
                    self._name, doc, None))
        return result

    @api.model
    def create(self, values):
        print values
        res = super(DynamicView, self).create(values)
        return res
