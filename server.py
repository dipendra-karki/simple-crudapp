from werkzeug.wrappers import Response
from werkzeug.wsgi import SharedDataMiddleware
import os
from lib.app import App
import logging
logging.basicConfig(level=logging.DEBUG)

def create_app(config):
    app = App(config)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app,{'/static': config['static_path']})
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    config = {
        'db':{
            'host':'localhost',
            'user':'dipendra',
            'password':'postgres',
            'dbname':'webproject',
        },
        'static_path': os.path.join(os.path.dirname(__file__),'static'),
        'template_path': os.path.join(os.path.dirname(__file__),'templates')
    }

    app = create_app(config)
    run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
logging.info('we are here')
