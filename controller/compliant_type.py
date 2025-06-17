# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


class CompliantType(http.Controller):
   
    @http.route(['/ain/property'], type='http', auth="public", website=True, sitemap=True, methods=["GET", "POST"])
    def compliant_type(self, **kw):

        code = "1165"  # لاحظ أنه يجب أن يكون str لأن input text يرجع نص

        if request.httprequest.method == "POST":
            user_code = kw.get('verification_code')
            if user_code == code:
                return request.render("Ain.compliant_type_template")
            else:
                # نمرر رسالة الخطأ للقالب
                return request.render("Ain.new_verification_popup_template", {
                    "error": "الرمز المُدخل غير صحيح"
                })

        # عند GET فقط نعرض صفحة الإدخال بدون تحقق
        return request.render("Ain.new_verification_popup_template")