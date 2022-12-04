from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from application.db import db
from application.models import *
from .validations import *

from sqlalchemy import exc

from datetime import datetime

ipFields = reqparse.RequestParser()
ipFields.add_argument("name")
ipFields.add_argument("desc")

opFields = {
  "id": fields.Integer,
  "name": fields.String,
  "desc": fields.String,
  "created_on": fields.String
}

class ListAPI(Resource):
  @marshal_with(opFields)
  def get(self, list_id):
    try:
      list = List.query.filter_by(id = list_id).one()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "List Not Found")
    else:
      return list
  @marshal_with(opFields)
  def put(self, list_id):
    args = ipFields.parse_args()
    name = args.get("name")
    desc = args.get("desc")
    try:
      list = List.query.filter_by(id = list_id).one()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "List Not Found")
    else:
      list.name = name
      list.desc = desc
      db.session.commit()
      return list
  def delete(self, list_id):
    try:
      list = List.query.filter_by(id = list_id).one()
      for i in list.cards:
        Card.query.filter_by(id = i.id).delete()
      LC.query.filter_by(list_id = list_id).delete()
      UL.query.filter_by(list_id = list_id).delete()
      List.query.filter_by(id = list_id).delete()
      db.session.commit()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "List not found")
    else:
      db.session.commit()
      return ""

class UserListAPI(Resource):
  @marshal_with(opFields)
  def get(self, user_id):
    try:
      list = User.query.filter_by(user_id = user_id).one().lists
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "Lists for this User Not Found")
    else:
      return list
  @marshal_with(opFields)
  def post(self, user_id):
    args = ipFields.parse_args()
    name = args.get("name")
    desc = args.get("desc")
    list = List()
    list.name = name
    list.desc = desc
    list.created_on = str(datetime.today())[:16]
    try:
      db.session.add(list)
      db.session.commit()
      userlist = UL()
      userlist.user_id = db.session.query(User).filter(User.user_id == user_id).one().id
      userlist.list_id = list.id
      db.session.add(userlist)
      db.session.commit()
    except:
      raise 400
    else:
      return list