import os
import sys

if sys.version_info[0]<3:       # require python3
	raise Exception("Python3 required! Current (wrong) version: '%s'" % sys.version_info)

activate_this = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'venv',
    'bin',
    'activate_this.py')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

thisGlobals = globals()
thisGlobals['__file__'] = activate_this
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, thisGlobals)

def application(environ, start_response):
    ENVIRONMENT_VARIABLES = ['DB_CONN_STR', 'SECRET_KEY']
    for key in ENVIRONMENT_VARIABLES:
        os.environ[key] = environ.get(key)
    from fwsdemo.app import app as application
    return application(environ, start_response)
