import marshal
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from application.db import db
from application.models import *
from .validations import *

from sqlalchemy import exc

from datetime import datetime

ipFields = reqparse.RequestParser()
ipFields.add_argument("user_id")
ipFields.add_argument("first_name")
ipFields.add_argument("last_name")
ipFields.add_argument("password")

opFields = {
  "id": fields.Integer,
  "name": fields.String,
  "user_id": fields.String,
  "created_on": fields.String,
  "last_login": fields.String
}

class UserAPI(Resource):

  @marshal_with(opFields)
  def post(self):
    args = ipFields.parse_args()
    user = User()
    user.name = args.get("first_name")+" "+args.get("last_name")
    user.user_id = args.get("user_id")
    user.pwd = args.get("password")
    user.created_on = str(datetime.today())[:16]
    user.last_login = str(datetime.today())[:16]
    try:
      db.session.add(user)
      db.session.commit()
    except exc.IntegrityError:
      raise DuplicateError(code = 400, emsg = "User ID already exists")
    else:
      return user

  @marshal_with(opFields)  
  def get(self, user_id):
    try:
      user = User.query.filter_by(user_id = user_id).one()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "User Not Found")
    else:
      return user

  @marshal_with(opFields)
  def put(self, user_id):
    args = ipFields.parse_args()
    try:
      user = User.query.filter_by(user_id = user_id).one()
      user.name = args.get("first_name")+" "+args.get("last_name")
      user.user_id = args.get("user_id")
      db.session.commit()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "User Not Found")
    except exc.IntegrityError:
      raise DuplicateError(code = 400, emsg = "User ID already exists")
    else:
      return user

  def delete(self, user_id):
    try:
      user = User.query.filter_by(user_id = user_id).one()
      for i in user.lists:
        list = List.query.filter_by(id=i.id).one()
        for j in list.cards:
          Card.query.filter_by(id = j.id).delete()
        LC.query.filter_by(list_id = i.id).delete()
        UL.query.filter_by(list_id = i.id).delete()
        List.query.filter_by(id = i.id).delete()
      User.query.filter_by(user_id = user_id).delete()
      db.session.commit()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "User Not Found")
    except exc.IntegrityError:
      raise DuplicateError(code = 400, emsg = "Cannot delete user since user_id is associated with many lists")
    else:
      return ""