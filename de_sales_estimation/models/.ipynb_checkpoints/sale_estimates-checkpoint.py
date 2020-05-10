from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp

class SalesEstimate(models.Model):
    _name = 'sales.estimate'
    _rec_name = 'name_seq'
    _description = 'Sale Estimates to Customer'
    
    def action_sale_quotations(self):
        sale_id = self.env['sale.order'].create({
            'partner_id':self.partner_id.id,
            'date_order': fields.Datetime.now(),
            'payment_term_id': self.payment_terms_id.id,
            'opportunity_id': self.opportunity_id.id,
            'estimate_id': self.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'origin': self.name_seq,
        })
        for line in self.est_order_line:
            vals = {
                'order_id': sale_id.id,
                'product_id':line.product_id.id,
                'name': line.est_name,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
            }         
            self.env['sale.order.line'].create(vals)
            
        self.write({
            'state': 'create',
            'sale_id': sale_id.id,
        })
        

    # def action_sale_quotations(self):
    #     if not self.partner_id:
    #         return self.env.ref("de_sales_estimation.crm_quotation_partner_action").read()[0]
    #     else:
    #         return self.action_new_quotation_new()
    #
    # def action_new_quotation_new(self):
    #     action = self.env.ref("de_sales_estimation.sale_action_quotations_new").read()[0]
    #     action['context'] = {
    #         # 'search_default_opportunity_id': self.id,
    #         # 'default_opportunity_id': self.id,
    #         'search_default_partner_id': self.partner_id.id,
    #         'default_partner_id': self.partner_id.id,
    #         'default_payment_terms_id': self.payment_terms_id,
    #         'default_team_id': self.est_team.id,
    #         'default_order_line': self.est_order_line.id,
    #         # 'default_campaign_id': self.campaign_id.id,
    #         # 'default_medium_id': self.medium_id.id,
    #         # 'default_origin': self.name,
    #         # 'default_source_id': self.source_id.id,
    #         # 'default_company_id': self.company_id.id or self.env.company.id,
    #     }
    #     return action

    def ban_open_sale_estimates(self):
        self.write({'state': 'create'})
        return True
        if not self.partner_id:
            return self.env.ref("de_sales_estimation.crm_quotation_partner_action").read()[0]
        else:
            return self.action_new_quote()

    def action_new_quote(self):
        action = self.env.ref("de_sales_estimation.quote_action_quotations_new").read()[0]
        action['context'] = {
            # 'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.est_team.id,
            'default_client_ref': self.est_src,
            # 'default_est_user_id': self.est_user_id,
            'default_origin': self.origin.id,
            # 'default_source_id': self.source_id.id,
            # 'default_company_id': self.company_id.id or self.env.company.id,
        }
        return action

    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    def action_cancel(self):
        return self.write({'state': 'draft'})

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def reset(self):
        self.write({'state': 'draft'})

    def action_quotation_form(self):
        for rec in self:
            rec.state = 'create'

    def action_approved(self):
        for rec in self:
            rec.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('sale.estimates.sequence') or _('New')

        result = super(SalesEstimate, self).create(vals)
        return result

    @api.depends('state')
    def _compute_type_name(self):
        for record in self:
            record.type_name = _('Estimate') if record.state in ('draft', 'sent', 'cancel') else _('Sale Estimate')

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        if force_confirmation_template or (self.state == 'draft' and not self.env.context.get('proforma', False)):
            template_id = int(
                self.env['ir.config_parameter'].sudo().get_param('de_sales_estimation.email_tamplate_estimates'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('de_sales_estimation.email_tamplate_estimates',
                                                                        raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('de_sales_estimation.email_tamplate_estimates',
                                                                    raise_if_not_found=False)
        return template_id

    def action_quotation_estimate(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_template(template.lang, 'sales.estimate', self.ids[0])
        ctx = {
            'default_model': 'sales.estimate',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            # 'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang),
            'mark_so_as_sent': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def open_qute_estimates(self):
        self.ensure_one()
        return {
            'name': 'Qutation',
            'view_id': False,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sales.estimate',
            'type': 'ir.actions.act_window',
            'domain': [],
            'context': "{'create': True}"
        }

    def qute_count(self):
        count = self.env['sales.estimate'].search_count([('name_seq', '=', self.id)])
        self.qute_count_id = count

    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'account.use_invoice_terms') and self.env.company.invoice_terms or ''

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    
    type_name = fields.Char('Type Name', compute='_compute_type_name')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )
    payment_terms_id = fields.Many2one('account.payment.term', string='Payment Terms')
    client_ref = fields.Char(string="Customer Reference")
    est_date = fields.Datetime(string='Date', required=True, readonly=True, index=True,
                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                               default=fields.Datetime.now,
                               help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    est_src = fields.Char(string="Source Document")
    est_user_id = fields.Many2one(comodel_name="res.users", string="Sales Person", required=True, )
    est_team = fields.Many2one(comodel_name="crm.team", string="Sales Team", required=True, )
    est_order_line = fields.One2many(comodel_name="sales.estimate.line", inverse_name="order_id", required=True, )
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    sale_id = fields.Many2one(comodel_name="sale.order", string="Sales Qutation", required=False, )
    note = fields.Text('Terms and conditions', default=_default_note)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Estimate Sent'),
        ('confirm', 'Confirmed'),
        ('done', 'Approved'),
        ('create', 'Qutation Created'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    amount_total = fields.Monetary(string='Total Estimate', store=True, readonly=True, compute='_amount_all',
                                   tracking=4)
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Opportunity", required=False, )

    currency_id = fields.Many2one('res.currency', string='Currency')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    
    @api.depends('est_order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.est_order_line:
                amount_untaxed += line.price_subtotal
                # amount_tax += line.price_tax
            order.update({
                'amount_total': amount_untaxed,
            })


class SalesEstimateLine(models.Model):
    _name = 'sales.estimate.line'

    @api.onchange('product_id')
    def set_products_auto(self):
        for rec in self:
            rec.price_unit = rec.product_id.lst_price
            rec.est_name = rec.product_id.name
            rec.product_uom = rec.product_id.uom_id

    product_id = fields.Many2one('product.product', string='Product')
    order_id = fields.Many2one('sales.estimate', string='Reference')
    est_name = fields.Text(string='Description')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    # currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    # price_subtotal = fields.Monetary(string='Subtotal', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0, required=True, )
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price_unit_id = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])
    price_total = fields.Monetary(compute='_compute_amount', string='Total Estimate', readonly=True, store=True)
    product_custom_attribute_value_ids = fields.One2many('product.attribute.custom.value', 'sale_order_line_id',
                                                         string="Custom Values")
    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Extra Values",
                                                              ondelete='restrict')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id)
            line.update({
                # 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                # 'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
