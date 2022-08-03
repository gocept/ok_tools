from setuptools import setup


setup(
    name='ok-tools',
    version='0.1',
    install_requires=[
        'Django>=4.0.5',
        'django-revproxy>=0.10.0',
        'django-crispy-forms',
        'django-bootstrap-datepicker-plus',
        'django-durationwidget2',
        'reportlab',
        'PyPDF2',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-django',
            'zope.testbrowser',
        ]
    }
)
