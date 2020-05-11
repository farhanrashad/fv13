from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp


class SaleEstimate(models.Model):
    _name = 'sale.estimate'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _rec_name = 'name'
    _description = 'Sale Estimates to Customer'

    def action_sale_quotations(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productions'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [],
            'context': dict(self._context, create=True, default_partner_id=self.partner_id.id,
                            ),
        }

    def action_sale_quotations(self):
        sale_id = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'date_order': fields.Datetime.now(),
            'payment_term_id': self.payment_term_id.id,
            'opportunity_id': self.opportunity_id.id,
            'estimate_id': self.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'origin_id': self.name,
        })
        for line in self.est_order_line:
            vals = {
                'order_id': sale_id.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
            }
            self.env['sale.order.line'].create(vals)

        self.write({
            'state': 'create',
            # 'sale_id': sale_id.id,
        })


        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': _('Productions'),
        #     'res_model': 'sale.order',
        #     'view_mode': 'form',
            # 'domain': [],
            # 'context': dict(self._context, create=True, default_partner_id=self.partner_id.id,
            #                 ),
        # }


    def action_cancel(self):
        return self.write({'state': 'cancel'})

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

    name = fields.Char(string='Number', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.estimates.sequence') or _('New')
        result = super(SaleEstimate, self).create(vals)
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
        self.write({
            'state': 'sent',
        })
        if template.lang:
            lang = template._render_template(template.lang, 'sale.estimate', self.ids[0])
        ctx = {
            'default_model': 'sale.estimate',
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
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Quotation',
            'target': 'current',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [],
            'context': dict(self._context, create=True, default_estimate_id=self.id),
        }


    def qute_count(self):
        count = self.env['sale.order'].search_count([('estimate_id', '=', self.id)])
        self.qute_count_id = count
    qute_count_id = fields.Integer(string="Quotation", compute="qute_count")

    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'account.use_invoice_terms') and self.env.company.invoice_terms or ''

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    sale_create_qute = fields.Char(string="create button", required=False, )
    type_name = fields.Char('Type Name', compute='_compute_type_name')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, readonly=True, states={'draft': [('readonly', False)]})
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', readonly=True, states={'draft': [('readonly', False)]})
    client_ref = fields.Char(string="Customer Reference" )
    date_estimate = fields.Datetime(string='Date', required=True, readonly=True, index=True,
                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                               default=fields.Datetime.now,
                               help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    origin = fields.Char(string="Source Document" )
    user_id = fields.Many2one(comodel_name="res.users", string="Sales Person", required=True, readonly=True, states={'draft': [('readonly', False)]} )
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team", required=True, readonly=True, states={'draft': [('readonly', False)]})
    est_order_line = fields.One2many(comodel_name="sale.estimate.line", inverse_name="order_id", required=True, readonly=True, states={'draft': [('readonly', False)]})
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    sale_id = fields.Char(string="Sales Quotation", required=False, readonly=True, states={'draft': [('readonly', False)]})
    note = fields.Text('Terms and conditions', default=_default_note)


    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Estimate Sent'),
        ('confirm', 'Confirmed'),
        ('done', 'Approved'),
        ('create', 'Qutation Created'),
        ('cancel', 'Cancelled')], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')



    amount_total = fields.Monetary(string='Total Estimate', store=True, readonly=True, compute='_amount_all',
                                   tracking=4)
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Opportunity", required=False, )
    quote_id = fields.Many2one(comodel_name="sale.order", string="", required=False, )
    currency_id = fields.Many2one('res.currency', string='Currency')


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
