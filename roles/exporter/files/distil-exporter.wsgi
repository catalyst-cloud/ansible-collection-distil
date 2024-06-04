from distil.api.metrics.prometheus import make_app

application = make_app(['--config-file', '/etc/distil/distil.conf'])
