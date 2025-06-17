# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class CompliantView(http.Controller):
   
    @http.route(['/ain/compliant_view'], type='http', auth="public", website=True, sitemap=True)
    def compliant_view(self, **kw):
        values = {}
        p = request.env["property"].sudo().search([('number', '=' , kw.get('compliant_id'))])
        values.update(
            {
                "compliants": p,
            }
        )
        return request.render("Ain.compliant_view_template", values)