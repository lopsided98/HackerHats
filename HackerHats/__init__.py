from flask import Flask
import os

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/data.db'),
    SECRET_KEY='devel-key',
    SESSION_COOKIE_NAME = "HackerHatsSession",
    TEMPLATES_AUTO_RELOAD = True
))
app.config.from_envvar('HACKER_HATS_SETTINGS', silent=True)

import HackerHats.views
import HackerHats.database
