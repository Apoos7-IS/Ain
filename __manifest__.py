{
    'name': "Ain",
    'author': "Abdullah",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': [
        'base', 'website', 'web', 'no_attachment_preview'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/property_view.xml',
        'views/base_menu.xml',
        'views/pages/home_template.xml',
        'views/pages/compliant_type_template.xml',
        'views/pages/my_compliant_template.xml',
        'views/pages/success_popup_template.xml',
        'views/pages/error_popup_template.xml',
        'views/pages/compliant_view_template.xml',
        'views/pages/new_verification_popup_template.xml',
        'views/pages/new_phone_popup_template.xml',
        'views/pages/view_phone_popup_template.xml',
        'views/pages/view_verification_popup_template.xml',
    ],
    'application': True,
    
    'assets': {
        'web.assets_frontend': [
            'Ain/static/src/img/*',
            'Ain/static/src/js/ain_property.js',
            'Ain/static/src/css/complaint_type_style.css',
        ],
        'web.assets_backend': [
            'Ain/static/src/js/custom_attachment_widget.js',
            'Ain/static/src/xml/custom_attachment_widget_template.xml',
        ],
    },
}