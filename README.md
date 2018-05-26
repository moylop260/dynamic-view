# dynamic-view
Repository to create a POC for creation of a dynamic view with fields created on-the-fly

Use 9.0 version of odoo and apply the following patch:

```python
diff --git a/addons/hr_attendance/hr_attendance.py b/addons/hr_attendance/hr_attendance.py
index cd8bae0e1a1..305a9274339 100644
--- a/addons/hr_attendance/hr_attendance.py
+++ b/addons/hr_attendance/hr_attendance.py
@@ -57,15 +57,15 @@ class hr_attendance(osv.osv):
         return res
 
     _columns = {
-        'name': fields.datetime('Date', required=True, select=1),
+        'name': fields.date('Date', required=True, select=1),
         'action': fields.selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('action','Action')], 'Action', required=True),
         'action_desc': fields.many2one("hr.action.reason", "Action Reason", domain="[('action_type', '=', action)]", help='Specifies the reason for Signing In/Signing Out in case of extra hours.'),
         'employee_id': fields.many2one('hr.employee', "Employee", required=True, select=True),
         'department_id': fields.many2one('hr.department', "Department", related="employee_id.department_id"),
-        'worked_hours': fields.function(_worked_hours_compute, type='float', string='Worked Hours', store=True),
+        # 'worked_hours': fields.function(_worked_hours_compute, type='float', string='Worked Hours', store=True),
     }
     _defaults = {
-        'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'), #please don't remove the lambda, if you remove it then the current time will not change
+        'name': lambda *a: time.strftime('%Y-%m-%d'), #please don't remove the lambda, if you remove it then the current time will not change
         'employee_id': _employee_get,
     }
 
@@ -89,7 +89,7 @@ class hr_attendance(osv.osv):
                 return False
         return True
 
-    _constraints = [(_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])]
+    # _constraints = [(_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])]
     _order = 'name desc'
 
 
diff --git a/addons/hr_timesheet_sheet/hr_timesheet_sheet.py b/addons/hr_timesheet_sheet/hr_timesheet_sheet.py
index 02c15a63f46..c99df226a5f 100644
--- a/addons/hr_timesheet_sheet/hr_timesheet_sheet.py
+++ b/addons/hr_timesheet_sheet/hr_timesheet_sheet.py
@@ -403,6 +403,7 @@ class hr_attendance(osv.osv):
             employee = employee_obj.browse(cr, uid, employee_id, context=context)
             tz = employee.user_id.partner_id.tz
 
+        date = None
         if not date:
             date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
 
```
