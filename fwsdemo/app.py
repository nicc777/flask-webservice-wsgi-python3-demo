import os
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from fwsdemo.database import init_db
from fwsdemo.database import db_session
from fwsdemo.models import User
import logging
from logging import Formatter

init_db()

app = Flask(__name__)
api = Api(app)

class UserSummary(Resource):
    def get(self):
        app.logger.info('UserSummary Called from %s' % request.remote_addr)
        users = User.query.all()
        return {'userCount': len(users)}

api.add_resource(UserSummary, '/')

log_handler_str = os.environ.get('FLASK_LOG_HANDLER') or 'file'
if log_handler_str.lower() == 'file':
    print("log handler: FileHandler")
    from logging import FileHandler
    log_handler = FileHandler('/tmp/app.log')
elif log_handler_str.lower() == 'syslog':
    print("log handler: SysLogHandler")
    from logging.handlers import SysLogHandler
    log_handler = SysLogHandler()
log_level_str = os.environ.get('FLASK_LOG_LEVEL') or 'info'
if log_handler:
    print("log_handler enabled")
    if log_level_str.lower() == 'critical':
        log_handler.setLevel(logging.CRITICAL)
        app.logger.setLevel(logging.CRITICAL)
    elif log_level_str.lower() == 'error':
        log_handler.setLevel(logging.ERROR)
        app.logger.setLevel(logging.ERROR)
    elif log_level_str.lower() == 'warning':
        log_handler.setLevel(logging.WARNING)
        app.logger.setLevel(logging.WARNING)
    elif log_level_str.lower() == 'info':
        log_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
    elif log_level_str.lower() == 'debug':
        log_handler.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    else:
        log_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)

    log_handler.setFormatter(Formatter('FLASK_LOG [%(asctime)s] [%(levelname)s] [%(module)s] [%(lineno)d] %(message)s'))
    app.logger.addHandler(log_handler)
    print("logger.hasHandlers(): %s" % app.logger.hasHandlers())
else:
    print("log_handler was not enabled")

if __name__ == '__main__':
    app.run(debug=True)
