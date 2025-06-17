# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class NewVerification(http.Controller):

    @http.route(['/ain/new_verification'], type='http', auth="public", website=True, sitemap=True, methods=["GET", "POST"])
    def new_verification(self):
        return request.render("Ain.new_verification_popup_template")