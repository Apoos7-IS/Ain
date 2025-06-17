# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class MyCompliants(http.Controller):
   
# controller for open بلاغاتي button
    @http.route("/ain/my_compliants", type='http', auth="public", website=True, sitemap=True)
    def my_compliants(self, **kw):
        if request.httprequest.method == "POST":
            values = {}
            phone_number = request.session.get('phone_number')
            p = request.env["property"].sudo().search([('phone_number', '=' , phone_number)], order='create_date DESC')
            values.update(
                {
                    "compliants": p,
                }
            )
            code = "7652"
            user_code = kw.get('verification_code')
            if user_code == code:
                return request.render("Ain.my_compliant_template", values)
            else:
                # نمرر رسالة الخطأ للقالب
                return request.render("Ain.view_verification_popup_template", {
                    "error": "الرمز المُدخل غير صحيح"
                })

        # عند GET فقط نعرض صفحة الإدخال بدون تحقق
        return request.render("Ain.view_verification_popup_template")
