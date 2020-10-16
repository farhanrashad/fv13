import xlwt

from odoo import models
import datetime

class PartnerXlsx(models.AbstractModel):
    _name = 'report.de_helpdesk_ticket_detail_report.report_emp_att_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
            format1 = workbook.add_format(({'font_size': 10, 'align': 'vcenter', 'bold':True}))
            format2 = workbook.add_format(({'font_size': 10, 'align': 'vcenter', 'bold':True}))
            sheet1 = workbook.add_worksheet('Comp Feedback Report')
            sheet2 = workbook.add_worksheet('Material Consumption')
#             sheet1.set_column(0,0,5)
#             sheet1.set_column(0,2,5)
            sheet1.write(0,0,'Sr No', format1)
            sheet1.write(0,1,'Order Number', format1)
            sheet1.write(0,2,'CRMID', format1)
            sheet1.write(0,3,'Equipment', format1)
            sheet1.write(0,4,'Customer Name', format1)
            sheet1.write(0,5,'Contact Person', format1)
            sheet1.write(0,6,'Telephone1', format1)
            sheet1.write(0,7,'Street', format1)
            sheet1.write(0,8,'Description', format1)
            sheet1.write(0,9,'Return Equipment', format1)
            sheet1.write(0,10,'Distributer', format1)
            sheet1.write(0,11,'Long Text', format1)
            sheet1.write(0,12,'City Name', format1)
            sheet1.write(0,13,'Notification', format1)
            sheet1.write(0,14,'(3p) Received', format1)
            sheet1.write(0,15,'Town', format1)
            sheet1.write(0,16,'Tech Name', format1)
            sheet1.write(0,17,'BAR CODE', format1)
            sheet1.write(0,18,'AssetCode', format1)
            sheet1.write(0,19,'Asset Model', format1)
            sheet1.write(0,20,'Fault & Diagnosing', format1)
            sheet1.write(0,21,'Remedy/Technician Remarks', format1)
            sheet1.write(0,22,'Main Category', format1)
            sheet1.write(0,23,'Sub Category', format1)
            sheet1.write(0,24,'Status', format1)
            sheet1.write(0,25,'Date', format1)
            sheet1.write(0,26,'Contact Person', format1)
            sheet1.write(0,27,'Contact Number', format1)
            sheet1.write(0,28,'Additional Remarks', format1)
            sheet1.write(0,29,'Compressor Number', format1)
            sheet1.write(0,29,'Final BarCode', format1)
            sheet1.write(0,29,'Level', format1)
            sheet1.write(0,29,'Report Date & Time', format1)
#============================sheet 2==============================            
            sheet2.write(0,0,'Order Number', format2)
            sheet2.write(0,1,'City', format2)
            sheet2.write(0,2,'Model', format2)
            sheet2.write(0,3,'Status', format2)
            sheet2.write(0,4,'Fault', format2)
            sheet2.write(0,5,'Equipment', format2)
            sheet2.write(0,6,'Service', format2)
            sheet2.write(0,7,'Material Code', format2)
            sheet2.write(0,8,'Material Description', format2)
            sheet2.write(0,9,'QTY', format2)
            sheet2.write(0,10,'Warranty', format2)
            sheet2.write(0,11,'Date', format2)
            
            
            
            






