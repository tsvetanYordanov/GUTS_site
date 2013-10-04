#!/usr/bin/python
# Self executable. Run as ./run.py
# See results at localhost:5000

from guts_website import app
from guts_website.sensitive import IS_DEBUG
app.run(debug = IS_DEBUG)
