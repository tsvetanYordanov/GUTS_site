# WSGI MODULE
# =================================================
# Used as a connection to apache webserver.

import os,sys

# Store current working directory
pwd = os.path.dirname(__file__)
# Append current directory to the python path
sys.path.append(pwd)
from guts_website import app as application
application.debug = True
