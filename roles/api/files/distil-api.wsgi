from distil.api import app

application = app.make_app(['--config-file', '/etc/distil/distil.conf'])
