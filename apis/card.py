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
ipFields.add_argument("description")
ipFields.add_argument("deadline")
ipFields.add_argument("done")

opFields = {
  "id": fields.Integer,
  "name": fields.String,
  "description": fields.String,
  "created_date": fields.String,
  "edited_date": fields.String,
  "completed_date": fields.String,
  "deadline": fields.String,
  "done": fields.String
}

class CardAPI(Resource):
  @marshal_with(opFields)
  def get(self, card_id):
    try:
      card = Card.query.filter_by(id = card_id).one()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "Card Not Found")
    else:
      return card
  def delete(self, card_id):
    card = db.session.query(Card).filter(Card.id == card_id).delete()
    if card:
      db.session.query(LC).filter(LC.card_id == card_id).delete()
      db.session.commit()
      return ""
    else:
      raise NotFoundError(code = 404, emsg = "Card Not Found")
  @marshal_with(opFields)
  def put(self, card_id):
    args = ipFields.parse_args()
    try:
      card = Card.query.filter_by(id = card_id).one()
      card.name = args.get("name")
      card.description = args.get("description")
      card.deadline = args.get("deadline")[:16]
      card.done = int(args.get("done"))
      if card.done:
        card.completed_date = str(datetime.today())[:16]
      card.edited_date = str(datetime.today())[:16]
      db.session.commit()
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "Card Not Found")
    else:
      return card

class ListCardAPI(Resource):
  @marshal_with(opFields)
  def get(self, list_id):
    try:    
      cards = List.query.filter_by(id = list_id).one().cards
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "Card Not Found")
    else:
      return cards
  @marshal_with(opFields)
  def post(self, list_id):
    args = ipFields.parse_args()
    card = Card()
    card.name = args.get("name")
    card.description = args.get("description")
    card.deadline = args.get("deadline")[:16]
    card.done = int(args.get("done"))
    card.created_date = str(datetime.today())[:16]
    card.edited_date = str(datetime.today())[:16]
    try:
      db.session.add(card)
      db.session.commit()
      listcard = LC()
      listcard.list_id = list_id
      listcard.card_id = card.id
      db.session.add(listcard)
      db.session.commit()
    except Exception as e:
      Card.query.filter_by(id = card.id).delete()
      db.session.commit()
      raise NotFoundError(code = 400, emsg = "List ID invalid")
    else:
      return card