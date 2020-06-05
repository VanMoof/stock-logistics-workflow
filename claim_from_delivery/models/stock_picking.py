# © 2020 Vanmoof BV (<https://www.vanmoof.com>)
# © 2004-2009 Tiny SPRL (<http://tiny.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _compute_claim_count_out(self):
        """
        Count number of claims related to stock pickings
        """
        claim_cls = self.env['crm.claim']
        for pick in self:
            pick.claim_count_out = claim_cls.search_count(
                [('model_ref_id', '=', 'stock.picking,{}'.format(pick.id))])

    claim_count_out = fields.Integer(
        compute="_compute_claim_count_out", string="Claims")
