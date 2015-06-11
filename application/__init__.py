from flask import Flask
import re
import os
import sys


MODULES = [
    {'name': 'auth', 'url_prefix': '/b'},
]
# Load the local modules


def load_module_models(app, module):
    if 'models' in module and module['models'] == False:
        return

    name = module['name']
    if app.config['DEBUG']:
        print("[MODEL] Loading db model %s" % (name))
    model_name = '%s.models' % (name)
    try:
        mod = __import__(model_name, globals(), locals(), [], 0)
    except ImportError as e:
        if re.match(r'No module named ', str(e)) == None:
            print('[MODEL] Unable to load the model for %s: %s' % (model_name, str(e)))
        else:
            print('[MODEL] Other(%s): %s' % (model_name, str(e)))
        return False
    return True


def register_local_modules(app):
    cur = os.path.abspath(__file__)
    sys.path.append(os.path.dirname(cur) + '/modules')
    for m in MODULES:
        mod_name = '%s.views' % m['name']
        try:
            views = __import__(mod_name, globals(), locals(), [], 0)
        except ImportError:
            load_module_models(app, m)
        else:
            url_prefix = None
            if 'url_prefix' in m:
                url_prefix = m['url_prefix']

            if app.config['DEBUG']:
                print('[VIEW ] Mapping views in %s to prefix: %s' % (mod_name, url_prefix))

            # Automatically map '/' to None to prevent modules from
            # stepping on one another.
            if url_prefix == '/':
                url_prefix = None
            load_module_models(app, m)
            app.register_module(views.module, url_prefix=url_prefix)



app = Flask(__name__)
app.debug = True
app.testing = True
app.secret_key = "Couscous la cle"


@app.route("/")
def root():
    return ""

register_local_modules(app)

