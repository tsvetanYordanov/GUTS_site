from flask.ext.login import UserMixin

from werkzeug.security import generate_password_hash, \
     check_password_hash

from guts_website.sensitive import ADMIN_USER, ADMIN_PASSWORD

class User(UserMixin):

    def __init__(self, name, id, active=True,password="weak"):
        self.name = name
        self.id = id
        self.active = active
        self.set_password(password)

    def is_active(self):
        return self.active
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

# Admin user name

USERS = {
    1: User(ADMIN_USER,1,True, ADMIN_PASSWORD),
    }

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())
