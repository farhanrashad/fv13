from odoo import models, fields, api


class ProductMail(models.Model):
    _inherit = 'product.template'

    user_id = fields.Many2one('res.users', string="User", required=True)
    is_mail = fields.Boolean('Is Mailed?', default=False)
    is_notified = fields.Boolean('Is Notified?', default=False)
    is_scheduler_running = fields.Boolean('Is scheduler running?', default=False)
    admin = ''

    def run_scheduler(self):
        global admin
        admin = self.env.user.email
        self.is_scheduler_running = True
        print('Scheduler Called!!!')
        scheduler = self.env['ir.cron'].search([('name', '=', 'Mail Scheduler')])
        if not scheduler:
            scheduler = self.env['ir.cron'].search(
                [('name', '=', 'Mail Scheduler'), ('active', '=', False)])
        scheduler.active = False
        scheduler.interval_number = 1
        scheduler.interval_type = 'days'

    def get_ordering_rules_qty(self):
        print("--------Checking Products--------")
        records = self.env['product.template'].search([])
        products = {}
        for rec in records:
            product_name = rec.name
            order_rule = rec.nbr_reordering_rules
            min_val = rec.reordering_min_qty
            qty = rec.qty_available
            sub_list = []
            sub_dic = {}
            if rec.user_id.id:
                if order_rule > 0:
                    email_to = rec.user_id.email
                    if qty < min_val and rec.is_notified == False:
                        print("Email Sent!!!!!")
                        rec.is_notified = True
                        # sub_list.extend((product_name, qty, min_val, order_rule, rec.user_id.email))
                        sub_dic = {
                            rec.id: {
                                'product_name': rec.name,
                                'minimum_value': rec.reordering_min_qty,
                                'inhand': rec.qty_available,
                                'email': rec.user_id.email
                            }
                        }
                    elif qty >= min_val and rec.is_notified == True:
                        print("State changed!!!!! Restocked")
                        rec.is_notified = False
                else:
                    print("Reordering Rule is Empty!!!!")
                    if qty > 0 and rec.is_notified == True:
                        print("Notified is Turned False!!!")
                        rec.is_notified = False
                    elif qty == 0 and rec.is_notified == False:
                        rec.is_notified = True
                        print("Email Sent")
                        sub_dic = {
                            rec.id: {
                                'product_name': rec.name,
                                'minimum_value': rec.reordering_min_qty,
                                'inhand': rec.qty_available,
                                'email': rec.user_id.email
                            }
                        }

          
            if sub_dic:
                products.update(sub_dic)

        self.action_email(products, email_to)

    def action_email(self, products, email_to):
        body_html = """<table class="table table-condensed"><thead><tr><th>SNO</th><th>Product 
                        Name</th><th>OnHand Quantity</th><th>Minimum Ordering Qty</th></tr></thead><tbody> """
        i = 0
        for sub_dictionary in products.values():
            if type(sub_dictionary) is dict:
                print(sub_dictionary.get('product_name'))
                i = i + 1
                body_html += "<tr><td>" + str(
                    i) + "</td><td>" + sub_dictionary.get('product_name') + "</td><td>" + str(sub_dictionary.get('inhand')) + "</td><td>" + str(sub_dictionary.get('minimum_value')) + "</td></td></tr>"

        body_html += """  </tbody></table>"""
        email_values = {
                        'body_html': body_html,
                        'subject': " Products Out of Stock Notification",
                        'email_from': admin,
                        'email_to': email_to
                        }
        self.env['mail.mail'].create(email_values).send()