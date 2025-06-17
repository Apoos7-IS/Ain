# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class Success(http.Controller):
   
    @http.route(['/ain/success'], type='http', auth="public", website=True, sitemap=True)
    def success(self):
        return request.render("Ain.success_popup_template")