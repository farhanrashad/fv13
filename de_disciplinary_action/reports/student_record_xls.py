from odoo import models


class Studentxlsx(models.AbstractModel):
    _name = 'report.de_disciplinary_action.report_case'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font-size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font-size':10, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Student record')
        sheet.write(2, 2, 'name', format1)
        sheet.write(2, 3, lines.name_seq, format2)

        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)
