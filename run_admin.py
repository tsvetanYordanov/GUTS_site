#!/usr/bin/python
# Self executable. Run as ./run_admin.py
# See results at localhost:5000/admin

from Admin import app
app.run(debug = True)
