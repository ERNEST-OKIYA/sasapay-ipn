DEBUG = True
ALLOWED_HOSTS = ['*', ]

DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sasapayipn',
        'USER':'sasapay',
        'PASSWORD':'qwertea21',
        'TIMEZONE':'Africa/Nairobi',
        'HOST': '10.115.128.4'
    },
}   

ALLOWED_CLIENTS = [
        '138.68.111.248',
        '196.201.214.200',
        '196.201.214.207',
        '35.246.150.253',

        '154.70.51.119', # LOCAL PUBLIC IP (ZUKU) TEST ONLY

]
