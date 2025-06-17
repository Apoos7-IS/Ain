import logging
import random
from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request, route
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.portal.controllers.portal import CustomerPortal


class Confirm(AuthSignupHome):
    """
    كلاس Confirm يرث من AuthSignupHome لمعالجة عملية تسجيل المستخدمين
    """
        
    @http.route(
        "/new/registration", 
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def web_auth_signup(self, **kw):
        """
        دالة لمعالجة عملية تسجيل مستخدم جديد عبر الموقع
        """
        values = {}
        # إذا كانت الطلبية من نوع GET نعرض صفحة التسجيل
        if request.httprequest.method == "GET":
            return request.render("them_canary.signup_template")
            
        # إذا كانت الطلبية من نوع POST نعالج بيانات التسجيل
        if request.httprequest.method == "POST":
            try:
                # إنشاء قاموس يحتوي على بيانات المستخدم الجديد
                new_compliant = {
                    "name": kw.get("name", False),
                    "email": kw.get("login", False),
                    "mobile": kw.get("mobile", False),
                    "phone": kw.get("mobile", False),
                    "identity_number": kw.get("identity_number", False),
                    "company_id": request.env.company.id,
                    "is_guardian": True,
                }
                try:
                    # البحث عن شريك موجود بنفس رقم الجوال وله صفة ولي أمر أو طفل
                    exist_partner = request.env["res.partner"].sudo().search([
                        ('mobile', '=', kw.get("mobile", False)),
                        '|', 
                        ('is_guardian', '=', True), 
                        ('is_child', '=', True)
                    ])
                    if exist_partner:
                        values.update(kw)
                        values["error"] = _("Identity number already exists.")
                        return request.render("them_canary.signup_template", values)
                    
                    # التحقق من وجود مستخدم بنفس رقم الجوال (كاسم مستخدم)
                    user = request.env["res.users"].sudo().search_count([('login', '=', kw.get("mobile", False))])
                    if user > 0:
                        values.update(kw)
                        values["error"] = _("Mobile number already exists.")
                        return request.render("them_canary.signup_template", values)
                        
                    # بدء عملية إنشاء مستخدم جديد داخل savepoint للتراجع عند الخطأ
                    with request.env.cr.savepoint():
                        # إنشاء شريك جديد
                        partner_new = request.env["res.partner"].sudo().create(new_compliant)
                        request.session['partner_id'] = partner_new.id
                        
                        # إنشاء رمز تحقق عشوائي وإرساله عبر SMS
                        verification = int(random.randint(1000, 9999))
                        request.env["verification.code"].sudo().create(
                            {
                                "verification_code": verification,
                                "partner_id": partner_new.id,
                            }
                        )
                        sms_message_otp = request.env.ref("canary_sms_message.send_otp_msg")
                        content = sms_message_otp.content.format(otp=verification)
                        sms = request.env["sms.send"].create({
                            "partner_id": partner_new.id,
                            "mobile": partner_new.mobile,
                            "message_id": sms_message_otp.id,
                            "company_id":  partner_new.company_id.id,
                            "content": content
                        })
                        sms.send_sms()
                        return request.redirect("/verification")
                except ValidationError as msg:
                    # معالجة أخطاء التحقق من الصحة
                    values.update(kw)
                    error = str(msg.args[0])
                    if error:
                        values["error"] = error
                        return request.render("them_canary.signup_template", values)
            except Exception as e:
                # معالجة الأخطاء العامة
                return request.render("them_canary.error_signup_template", {'exception': e})
            
    @route(
        ["/verification"],
        type="http",
        auth="public",
        website=True,
        csrf=False
        )
        
    def verification(self, *args, **kw):
        """
        دالة للتحقق من رمز OTP وإنشاء حساب المستخدم بعد التحقق
        """
        values = {}
        if request.session.get('partner_id'):
            partner = request.env["res.partner"].sudo().browse(request.session.get('partner_id'))
            request.session['partner_id'] = partner.id
            
            # إذا كانت الطلبية GET نعرض صفحة إدخال رمز التحقق
            if request.httprequest.method == "GET":
                if partner:
                    return request.render("them_canary.verification_code_template")
                    
            # إذا كانت الطلبية POST نتحقق من رمز OTP
            elif request.httprequest.method == "POST":
                if partner:
                    # البحث عن آخر رمز تحقق للمستخدم
                    verification = request.env["verification.code"].sudo().search([("partner_id", "=", partner.id),], limit=1, order="id desc")
                    # تجميع أجزاء رمز التحقق من الحقول المنفصلة
                    verification_code = kw.get("verification_code1") + kw.get("verification_code2") + kw.get("verification_code3") + kw.get("verification_code4")
                    
                    # التحقق من صحة رمز التحقق
                    if verification_code == "" or verification.verification_code != int(verification_code):
                        values["error"] = _("The entered verification code is incorrect.")
                        return request.render("them_canary.verification_code_template", values)
                    else:
                        # إنشاء مستخدم جديد بعد التحقق الناجح
                        beneficiary_user = request.env["res.users"].sudo().create(
                            {
                                "company_id": request.env.ref("base.main_company").id,
                                "name": partner.name,
                                "login": partner.mobile,
                                "password": partner.mobile,
                                "partner_id": partner.id,
                                "groups_id": [
                                    (
                                        6,
                                        0,
                                        [request.env.ref("base.group_portal").id,],
                                    )
                                ],
                            }
                        )
                        partner.sudo().write({"user_id" : beneficiary_user.id})
                        request.env.cr.commit()
                        
                        # تسجيل الدخول تلقائياً للمستخدم الجديد
                        request.params['login'] = partner.mobile
                        request.params['password'] = partner.mobile
                        login_result = self.web_login(*args, **kw)
                        if request.session.get('uid'):
                            return request.redirect("/my/info")