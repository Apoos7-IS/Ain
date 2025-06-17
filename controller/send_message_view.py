# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
import json, requests
import logging
import werkzeug.utils

_logger = logging.getLogger(__name__)
class SendMessage(http.Controller):

    @http.route('/ain/send_message_view', type='http', auth='public', methods=['POST'])
    def send_message_view(self, **kw):
        phone_number = "967" + kw.get("phone_number")
        _logger.info("Sending message...")
        url = "https://business.enjazatik.com/api/v1/send-message"
        payload = {
            "message": "رمز التحقق لنظام عين هو: *7652*",
            "number": phone_number
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJudW1iZXIiOiJnb2xkYm95Iiwic2VyaWFsIjoiNWRjZjczMGViZGEwNDgyIiwiaWF0IjoxNzQ4Njk5NzAzLCJleHAiOjE4MzUwOTk3MDN9.E99dBh0ylLhGaxtPCLvvmI0IB6VsgaK3n3nJweKkJQ0"
        }

        _logger.info("Message sent!")
        
        response = requests.post(url, json=payload, headers=headers)
        _logger.info('AAA - response: ', response)
        

        request.session['phone_number'] = kw.get('phone_number')
        return werkzeug.utils.redirect ('/ain/view_verification')
        
