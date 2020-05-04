from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def open_sale_estimates(self):
        self.ensure_one()

        return {
            'name': 'Estimate',
            'view_id': False,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sales.estimate',
            'type': 'ir.actions.act_window',
            'domain': [],
            'context': "{'create': True}"
        }

    def estimate_count(self):
        count = self.env['sales.estimate'].search_count([('partner_id', '=', self.id)])
        self.estimate_count_id = count

    estimate_count_id = fields.Integer(string="Estimate", compute="estimate_count")


class SaleOrderInhert(models.Model):
    _inherit = 'sale.order'

    @api.onchange('est_src')
    def onchange_method(self):
        for rec in self:
            line = []
            for line in self.order_line.est_order_line:
                vals = {
                    'est_src': line.id
                }
            line.append(0, 0, vals)
        print("lines", line)
        # rec.order_line = line


class SalesEstimate(models.Model):
    _name = 'sales.estimate'
    _rec_name = 'name_seq'
    _description = 'Sale Estimates to Customer'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_confirm(self):
        for rec in self:
            rec.state = 'done'

    def reset(self):
        self.write({'state': 'draft'})

    def create_qute(self):
        for rec in self:
            rec.state = 'create'

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

    qute_count_id = fields.Integer(string="Qutations", compute="qute_count")
    sale_create_qute = fields.Char(string="create button", required=False, )
    type_name = fields.Char('Type Name', compute='_compute_type_name')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )
    payment_terms_id = fields.Many2one('account.payment.term', string='Payment Terms')
    client_ref = fields.Char(string="Customer Reference", required=True, )
    est_date = fields.Datetime(string="Date", required=True, )
    est_src = fields.Char(string="Source Document", required=True, )
    est_user_id = fields.Many2one(comodel_name="res.users", string="Sales Person", required=True, )
    est_team = fields.Many2one(comodel_name="crm.team", string="Sales Team", required=True, )
    est_order_line = fields.One2many(comodel_name="sales.estimate.line", inverse_name="order_id", required=True, )
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    sale_qute = fields.Many2one(comodel_name="sale.order", string="Sales Qutation", required=False, )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Estimate Sent'),
        ('confirm', 'Confirmed'),
        ('done', 'Approved'),
        ('create', 'Qutation Created'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    amount_total = fields.Monetary(string='Total Estimate', store=True, readonly=True, compute='_amount_all', tracking=4)

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


class SalesEstimateLine(models.Model):
    _name = 'sales.estimate.line'

    product_id = fields.Many2one('product.product', string='Product')
    order_id = fields.Many2one('sales.estimate', string='Reference')
    est_name = fields.Text(string='Description')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    # currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    # price_subtotal = fields.Monetary(string='Subtotal', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0, required=True, )
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price_unit_id = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])
    price_total = fields.Monetary(compute='_compute_amount', string='Total Estimate', readonly=True, store=True)

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
