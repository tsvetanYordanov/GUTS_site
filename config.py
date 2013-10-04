# CONFIG
# ================================================
# Various configurations for the application

from guts_website.sensitive import DB_PASSWORD, CSRF_KEY

# CSRF prevention
CSRF_ENABLED = True
SECRET_KEY = CSRF_KEY 

# DB address
SQLALCHEMY_DATABASE_URI = 'mysql://guts:' + DB_PASSWORD + '@localhost/guts'
