# Copyright 2021 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import functools
from odoo import _, exceptions, models, tools


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_auto_unreserve_pickings(self):
        """ Unreserve other pickings in order to reserve pickings in self """
        to_unreserve = self._auto_unreserve_find_moves()
        to_unreserve._do_unreserve()
        self.message_post(_(
            'Unreserved picking(s) %s in order to assign this one'
        ) % ', '.join(to_unreserve.mapped('picking_id.name')))
        return self.action_assign()

    def _auto_unreserve_find_moves(self):
        """ Return moves to unreserve in order to reserve pickings in self """
        location = self.mapped('location_id')
        result = self.env['stock.move']
        assert len(location) == 1, 'Pickings need to be from the same location'
        float_compare = functools.partial(
            tools.float_compare,
            precision_digits=result._fields['product_qty'].digits,
        )

        for move_line in self.mapped('move_lines'):
            demand = (
                move_line.product_qty - move_line.reserved_availability -
                move_line.availability
            )
            if float_compare(demand, 0) <= 0:
                continue
            candidates = self.env['stock.move'].search([
                ('id', 'not in', result.ids),
                ('picking_id', 'not in', self.ids),
                ('location_id', '=', location.id),
                ('product_id', '=', move_line.product_id.id),
                ('state', 'in', ('partially_available', 'assigned')),
            ], order='write_date asc')

            for candidate in candidates:
                if float_compare(demand, 0) > 0:
                    result += candidate
                    demand -= candidate.reserved_availability
                else:
                    break
            
            if float_compare(demand, 0) > 0:
                raise exceptions.UserError(
                    _('Cannot unreserve enough %s, missing quantity is %d') % (
                        move_line.product_id.name, demand
                    )
                )
        return result
