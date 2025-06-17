# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
import json, requests

class NewPhonePopup(http.Controller):
    
# controller for open phone_popup
    @http.route("/ain/new_phone_popup", type='http', auth="public", website=True, sitemap=True)
    
    def new_phone_popup(self):
        return request.render("Ain.new_phone_popup_template")
