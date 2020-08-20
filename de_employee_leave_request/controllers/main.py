from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


def leave_page_content():
    leave_type = request.env['hr.leave.type'].search([])
    employees = request.env['hr.employee'].search([])
    return {
        'leave_type': leave_type,
        'employees': employees,
    }


class MyLeaves(http.Controller):

    @http.route('/leave_page', type="http", auth="public", website=True)
    def leave_template(self, **kw):
        print("Execution Here.........................")
        return http.request.render('de_employee_leave_request.leave_template', leave_page_content())

    @http.route('/my_leave_page', type="http", auth="public", website=True)
    def leave_page_template(self, **kw):
        print("leave Execution Here.........................")
        leave_details = request.env['hr.leave'].sudo().search([])
        return request.render('de_employee_leave_request.leave_page_template', {'my_details': leave_details})

    @http.route('/create/leave', type="http", auth="public", website=True)
    def create_leave(self, **kw):
        print("Data Received.....", kw)
        doctor_val = {
            'holiday_status_id': int(kw.get('holiday_status_id')),
            'employee_id': int(kw.get('employee_id')),
            'request_date_from': kw.get('request_date_from'),
            'request_date_to': kw.get('request_date_to'),
            'number_of_days': kw.get('number_of_days'),
            'name': kw.get('name'),
        }
        request.env['hr.leave'].sudo().create(doctor_val)
        return request.render("de_employee_leave_request.patient_thanks", {})
