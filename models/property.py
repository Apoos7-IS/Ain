from odoo import models, fields, api

class Property(models.Model):
    _name = 'property'
    
    number = fields.Char("Compliant Number", readonly=True)

    state = fields.Selection([
        ('new','New'),
        ('escalation','Escalation'),
        ('done','Done')
    ], default="new")

    location = fields.Selection([
        ('computer_lab', 'معمل الحاسب الآلي'),
        ('library', 'المكتبة'),
        ('main_hall', 'القاعة الكبرى'),
        ('blue_hall', 'القاعة الزرقاء'),
        ('meeting_room', 'قاعة الاجتماعات'),
        ('agriculture_lab', 'معمل الزراعة'),
        ('administrative_office', 'مكتب إداري'),
        ('clinic', 'العيادة'),
        ('cafeteria', 'البوفيه'),
        ('male_restrooms', 'حمامات الطلاب'),
        ('female_restrooms', 'حمامات الطالبات'),
        ('girls_lounge', 'استراحة البنات'),
        ('girls_garden', 'حديقة البنات'),
        ('mosque', 'المسجد'),
        ('football_field', 'ملعب كرة القدم'),
        ('parking_lot', 'المواقف'),
        ('corridor', 'الممر'),
        ('staff_restrooms', 'حمامات الموظفين'),
        ('campus', 'الحرم الجامعي'),
        ('classroom', 'قاعة دراسية')
    ])

    compliant_type = fields.Selection([
        ('cleanliness', 'نظافة'),
        ('harassment', 'تحرش'),
        ('theft', 'سرقة'),
        ('verbal_abuse', 'تلفظ'),
        ('blackmail', 'ابتزاز'),
        ('threat', 'تهديد'),
        ('kidnapping', 'خطف'),
        ('vandalism', 'تخريب'),
        ('incitement', 'تحريض'),
        ('assault', 'اعتداء'),
        ('accident', 'حادث'),
        ('disturbance', 'ازعاج'),
        ('terrorism', 'إرهاب'),
        ('fire', 'حريق'),
        ('fraud', 'احتيال'),
        ('bribery', 'رشوة'),
        ('bullying', 'تنمر')
    ])

    compliant_class = fields.Selection([
        ('criminal', 'جنائي'),
        ('non_criminal', 'غير جنائي'),
    ])

    compliant_description = fields.Text()
    reporter_name = fields.Char()
    phone_number = fields.Char()
    level = fields.Char(default="الرابع")
    major = fields.Char(default="أمن المعلومات")
    collage = fields.Char(default="الحاسبات")
    registration = fields.Char(default="20202041080")

    # مرفق واحد مع الاسم
    attachment = fields.Binary(string="Attachment")
    attachment_backend = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment Name")
    attachment_type = fields.Char(string="Attachment Type")


    # للحالة
    def action_escalation(self):
        self.state = "escalation"

    def action_done(self):
        self.state = "done"

    # توليد رقم الشكوى تلقائيًا
    @api.model
    def create(self, vals):
        vals["number"] = self.env['ir.sequence'].next_by_code('compliant.number')
        return super(Property, self).create(vals)

# هنا تضاف دالة رابط الذكاء الاصطناعي 
