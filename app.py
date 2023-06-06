import os
from flask import Flask
from flask_restful import Resource, Api
from application.db import db
from flask_cors import CORS

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, ".db/db.sqlite3") 
app.secret_key = "secretkeyforapp"
db.init_app(app)
api = Api(app)
app.app_context().push()

from routes.route import *
from routes.card import *
from routes.auth import *
from routes.list import *
from routes.summary import *

from apis.list import *
from apis.user import *
from apis.card import *
from apis.summary import *

api.add_resource(ListAPI, "/api/list", "/api/list/<int:list_id>")
api.add_resource(UserListAPI, "/api/<user_id>/list")
api.add_resource(UserAPI, "/api/user", "/api/user/<user_id>/<pwd>")
api.add_resource(CardAPI, "/api/card", "/api/card/<int:card_id>")
api.add_resource(ListCardAPI, "/api/list/<int:list_id>/card")
api.add_resource(SummaryAPI, "/api/<user_id>/summary")

if __name__ == "__main__":
  app.run(
    host="0.0.0.0", 
    debug=True
  )