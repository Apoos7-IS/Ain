# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class Home(http.Controller):
   
    @http.route(['/ain/home'], type='http', auth="public", website=True, sitemap=True)
    def home(self):
        return request.render("Ain.homepage")