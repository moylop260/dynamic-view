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

    employee_id = fields.Many2one('hr.employee', store=False, readonly=True)

    field_view_definition = '<field name="%s"/>'
    default_state = None

    def get_field_states(self, label):
        states = self.env['hr.attendance']._fields['action'].selection
        return fields.Selection(states, string=label)

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
                self._add_field(t_date_name, self.get_field_states(date_name))
                date_node = etree.fromstring(
                    self.field_view_definition % t_date_name)
                parent_node.insert(parent_node.index(node) + 1, date_node)
                date_work += timedelta(days=1)
                node_work = date_node
            result['arch'], result['fields'] = (
                self.env['ir.ui.view'].postprocess_and_fields(
                    self._name, doc, None))
            self = self.create({'employee_id': 1})
        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # res = super(DynamicView, self).search_read(
        #     domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        # TODO: Process the domain based on employee data
        attendance_brw = self.env['hr.attendance']
        employees = self.env['hr.employee'].search(
            [], limit=limit, offset=offset)
        res = []
        data_initial = dict((field, self.default_state)
                            for field in fields if field[0].isdigit())  # Just dates fields
        attendances = attendance_brw.search([('employee_id', 'in', employees.ids),
                                             # TODO: Date fields.values() but currently we have datetime :(
                                             ])
        print "*"*10,len(attendances), len(employees)
        attendances_dict = {}
        for attendance in attendances:
            attendances_dict.setdefault(attendance.employee_id.id, {}).update({
                attendance.name[:-9]: attendance.action,
            })
        for employee in employees:
            data = data_initial.copy()
            data.update(dict(
                id=employee.id,
                employee_id=employee.id,
                **(attendances_dict.get(employee.id) or {})
            ))
            res.append(data)
        print res
        return res

    @api.multi
    def write(self, vals):
        self.ensure_one()
        attendance_brw = self.env['hr.attendance']
        employee_id = self.id
        domain = [('employee_id', '=', employee_id),
                  # ('name', 'in', vals.keys())])  # TODO: Enable this line for the model where is used date. (and not datetime)
                 ]
        attendances_dict = dict((attendance.name[:-9], attendance) for attendance in attendance_brw.search(domain))
        for attendance_date in vals:
            attendance = attendances_dict.get(attendance_date)
            data = dict(
                employee_id=employee_id,
                action=vals[attendance_date],
                name=attendance_date + ' 00:00:00'
            )
            if not attendance:
                attendance_brw.create(data)
            else:
                attendance.write(data)
        for record in self:
            record._cache.update(record._convert_to_cache(vals, update=True))
        # mark the fields as being computed, to avoid their invalidation
        for key in vals:
            self.env.computed[self._fields[key]].update(self._ids)
        # inverse the fields
        # for key in vals:
        #     self._fields[key].determine_inverse(self)  # get error
        for key in vals:
            self.env.computed[self._fields[key]].difference_update(self._ids)
        return True
