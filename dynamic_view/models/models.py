# -*- coding: utf-8 -*-

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

    dummy = fields.Text(store=False)
    dummy2 = fields.Text(store=False)
    # custom = fields.Text(store=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(DynamicView, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            node = doc.xpath("//field[@name='dummy']")[0]
            node.set('string', 'Dummy 2?')
            parent_node = node.getparent()
            setup_modifiers(node, result['fields']['dummy'])
            node2 = etree.fromstring('<field name="dummy2"/>')
            result['fields']['dummy2'] = result['fields']['dummy']
            result['fields']['dummy2']['string'] = 'Dummy2'
            print result['fields']
            setup_modifiers(node, result['fields']['dummy2'])
            parent_node.insert(1, node2)

            import pdb;pdb.set_trace()
            custom2 = fields.Text(store=False)
            # self._fields.update({'custom2': custom2})
            self._add_field('custom2', custom2)
            node_custom = etree.fromstring('<field name="custom2"/>')
            result['fields']['custom2'] = result['fields']['dummy']
            result['fields']['custom2']['string'] = 'Custom 2'
            setup_modifiers(node_custom, result['fields']['custom2'])
            parent_node.insert(1, node_custom)


        # asset_id = self.env.context.get('active_id')
        # active_model = self.env.context.get('active_model')
        # if active_model == 'account.asset.asset' and asset_id:
        #     asset = self.env['account.asset.asset'].browse(asset_id)
        #     doc = etree.XML(result['arch'])
        #     if asset.method_time == 'number' and doc.xpath("//field[@name='method_end']"):
        #         node = doc.xpath("//field[@name='method_end']")[0]
        #         node.set('invisible', '1')
        #         setup_modifiers(node, result['fields']['method_end'])
        #     elif asset.method_time == 'end' and doc.xpath("//field[@name='method_number']"):
        #         node = doc.xpath("//field[@name='method_number']")[0]
        #         node.set('invisible', '1')
        #         setup_modifiers(node, result['fields']['method_number'])
        #     result['arch'] = etree.tostring(doc)
            result['arch'] = etree.tostring(doc)
        return result

    @api.model
    def create(self, values):
        print values
        res = super(DynamicView, self).create(values)
        return res
