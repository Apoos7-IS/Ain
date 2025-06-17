# -*- coding: utf-8 -*-
import base64
import logging
import mimetypes

from odoo import http, Command
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Confirm(http.Controller):

    @http.route(
        "/ain/confirm",
        type="http",
        auth="public",
        website=True,
        csrf=True,
        methods=["POST"],
    )
    def handle_compliant_submission(self, **kw):
        """Create a Property record from portal form and attach an optional file."""
        try:
            _logger.debug("Received data: %s", kw)

            file = kw.get("attachment")
            b64_data = False
            filename = False

            if file and hasattr(file, "read"):
                raw = file.read()
                if raw:
                    b64_data = base64.b64encode(raw).decode()
                    filename = file.filename
                    mime_type, _ = mimetypes.guess_type(filename)
                    if not mime_type:
                        mime_type = 'application/octet-stream'  # نوع عام كاحتياط
                else:
                    _logger.warning("Uploaded file is empty: %s", file.filename)
            
            compliant_class_from_portal = kw.get("selected_category")

            non_criminal_categories = [
                "fire", "accident", "cleanliness"
            ]

            if compliant_class_from_portal in non_criminal_categories:
                compliant_class_from_portal = "non_criminal"
            else:
                compliant_class_from_portal = "criminal"

            phone_number = request.session.get('phone_number')
            vals = {
                "location": kw.get("selected_location"),
                "compliant_type": kw.get("selected_category"),
                "compliant_description": kw.get("description"),
                "reporter_name": kw.get("reporter_name"),
                "phone_number": phone_number,
                "compliant_class": compliant_class_from_portal,
                "attachment": b64_data,
                # "attachment_backend": kw.get("attachment")
                "attachment_name": filename,
                "attachment_type": mime_type,
                # "attachment_ids": [
                #     Command.create({
                #         'name': kw.get("attachment").filename if kw.get("attachment") else False,
                #         'datas': base64.b64encode(kw.get("attachment").read()) if kw.get("attachment") else False
                #     })
                # ]
            }
            _logger.info(vals)
            # if attachment_vals:
                # vals["attachment_ids"] = [attachment_vals]

            # --- 3) أنشئ السجل -----------------------------------------------------------
            new_property = request.env["property"].sudo().create(vals)

            # --- 4) أعد صفحة النجاح ------------------------------------------------------
            return request.render("Ain.success_popup_template", {
                "reference": new_property.id,
                "message": "تم استلام بلاغك بنجاح",
            })

        # --------------- معالجة الأخطاء المتوقَّعة ----------------
        except ValidationError as e:
            _logger.warning("Validation error: %s", e)
            return request.render("Ain.error_popup_template", {
                "error": "خطأ في التحقُّق من البيانات",
                "form_data": kw,
            })

        # --------------- أي خطأ آخر -------------------------------
        except Exception as e:
            _logger.exception("Property submission error")  # يسجّل Traceback
            return request.render("Ain.error_popup_template", {
                "error": "حدث خطأ غير متوقَّع أثناء حفظ البلاغ",
                "form_data": kw,
            })