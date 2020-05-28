# © 2020 Vanmoof BV (<https://www.vanmoof.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common, tagged
from odoo.tests.common import TransactionCase


@tagged('standard')
class TestClaimsButton(TransactionCase):
    def test_picking_to_clim_button(self):
        picking = self.env.ref('stock.outgoing_shipment_main_warehouse6')
        picking2 = self.env.ref('stock.outgoing_shipment_main_warehouse5')
        self.env['crm.claim'].create({
            'name': 'Test Claim',
            'model_ref_id': '%s,%s' % ('stock.picking', picking.id),
        })
        self.env['crm.claim'].create({
            'name': 'Test Claim',
            'model_ref_id': '%s,%s' % ('stock.picking', picking.id),
        })
        self.assertEqual(picking.claim_count_out, 2)
        self.assertFalse(picking2.claim_count_out)
