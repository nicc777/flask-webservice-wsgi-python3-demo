from flask import Flask
from flask_restful import Resource, Api
from fwsdemo.database import init_db
from fwsdemo.database import db_session
from fwsdemo.models import User

init_db()

app = Flask(__name__)
api = Api(app)

class UserSummary(Resource):
    def get(self):
        users = User.query.all()
        return {'userCount': len(users)}

api.add_resource(UserSummary, '/')

if __name__ == '__main__':
    app.run(debug=True)
