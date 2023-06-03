# -*- coding: utf-8 -*-
##############################################################################
#
# Part of lucidbrainz. (Website: www.lucidbrainz.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.variant import VariantController


class VariantControllerInh(VariantController):
    @http.route(['/sale/get_combination_info'], type='json', auth="user", methods=['POST'])
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        res = super().get_combination_info(product_template_id, product_id, combination, add_qty, pricelist_id, **kw)
        if res.get('product_id'):
            product_rec = request.env['product.product'].sudo().browse(res['product_id'])
            rel_product = product_rec.x_aa_ol_link_product_id
            if rel_product:
                res.update({
                    'product_id': rel_product.id,
                    'virtual_available': rel_product.x_aa_ol_free_on_hand,
                    'virtual_available_formatted': rel_product.x_aa_ol_free_on_hand,
                    'list_price' : rel_product.lst_price,
                    'price' : rel_product.lst_price,
                    'inventory_availability': rel_product.inventory_availability,
                    'custom_message': rel_product.custom_message,
                })
            else:
                res.update({
                    'virtual_available': product_rec.x_aa_ol_free_on_hand,
                    'virtual_available_formatted': product_rec.x_aa_ol_free_on_hand,
                })
        return res
