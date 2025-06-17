# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class ViewVerification(http.Controller):

    @http.route(['/ain/view_verification'], type='http', auth="public", website=True, sitemap=True, methods=["GET", "POST"])
    def view_verification(self):
        return request.render("Ain.view_verification_popup_template", {
        })