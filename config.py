
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1234@localhost/vacimaps'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'um-nome-bem-seguro' 

MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'vacimaps@gmail.com'
MAIL_PASSWORD = 'senha do gmail'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
