# © 2020 Vanmoof BV (<https://www.vanmoof.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import _, api, fields, models


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    @api.model
    def _selection_model(self):
        """
        Extend claim's Reference filed selection with Stock Picking
        :return: list of tuples (model_name, model_description)
        """
        res = super(CrmClaim, self)._selection_model()
        res.append(('stock.picking', _(self.env['stock.picking']._description)))
        return res
