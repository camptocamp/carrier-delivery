# Copyright 2015 Swisslux
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    company_group_id = fields.Many2one(
        related='partner_id.company_group_id',
        model='res.partner',
        store=True,
        readonly=True,
        string='Company Group',
    )

    # The partner that will be invoiced
    income_partner_id = fields.Many2one(
        related='partner_invoice_id.commercial_partner_id',
        model='res.partner',
        store=True,
        readonly=True,
        string='Income Commercial Partner',
    )

    # The partner where the order will be sent
    commercial_partner_id = fields.Many2one(
        related='partner_id.commercial_partner_id',
        model='res.partner',
        store=True,
        readonly=True,
        string='Commercial Entity',
    )

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        vals = super()._prepare_invoice()
        company_partner = self.partner_id.get_company_partner()
        vals['income_partner_id'] = company_partner.id
        return vals


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        self.ensure_one()
        invoice_return = super()._create_invoice(order, so_line, amount)
        company_partner = order.partner_id.get_company_partner()
        invoice_return.income_partner_id = company_partner.id
        return invoice_return
