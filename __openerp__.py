{
    'name': 'Simple Contact',
    'category': 'Website',
    'summary': 'Simple contact form to collect email adresses',
    'version': '1.0',
    'description': """
OpenERP Simple Contact Form
===========================

        """,
    'author': 'OpenBIG',
    'depends': ['crm','survey','website'],
    'data': [
        'views/website_simple_contact.xml',
        'views/snippets.xml',
        'website_simple_contact_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
