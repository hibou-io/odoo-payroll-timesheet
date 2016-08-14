# -*- coding: utf-8 -*-
from openerp import models, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        self.ensure_one()

        attendances = {
            'name': 'Timesheet Attendance',
            'sequence': 10,
            'code': 'ATTN',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': self.contract_id.id,
        }

        valid_days = [
            ('sheet_id.employee_id', '=', self.employee_id.id),
            ('sheet_id.state', '=', 'done'),
            ('sheet_id.date_from', '>=', date_from),
            ('sheet_id.date_to', '<=', date_to),
        ]

        for day in self.env['hr_timesheet_sheet.sheet.day'].search(valid_days):
            if day.total_attendance >= 0.0:
                attendances['number_of_days'] += 1
                attendances['number_of_hours'] += day.total_attendance

        # needed so that the shown hours matches any calculations you use them for
        attendances['number_of_hours'] = round(attendances['number_of_hours'], 2)

        return super(HrPayslip, self).get_worked_day_lines(contract_ids, date_from, date_to) + [attendances]
