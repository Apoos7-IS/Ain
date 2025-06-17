# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class Error(http.Controller):
   
    @http.route(['/ain/error'], type='http', auth="public", website=True, sitemap=True)
    def error(self):
        return request.render("Ain.error_popup_template")