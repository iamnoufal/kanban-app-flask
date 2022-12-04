from .db import db

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, autoincrement = True, primary_key = True)
  name = db.Column(db.String, nullable = False)
  user_id = db.Column(db.String, unique = True, nullable = False)
  pwd = db.Column(db.String, nullable = True)
  created_on = db.Column(db.String, nullable = False)
  last_login = db.Column(db.String)
  lists = db.relationship("List", secondary = "userlist")
  total = 0
  totalLists = 0
  completed = 0
  pending = 0
  passed = 0

class UL(db.Model):
  __tablename__ = "userlist"
  id = db.Column(db.Integer, autoincrement = True, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True, nullable = False)
  list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), primary_key = True, nullable = False)

class List(db.Model):
  __tablename__ = "lists"
  id = db.Column(db.Integer, autoincrement = True, primary_key = True)
  name = db.Column(db.String, nullable = False)
  desc = db.Column(db.String)
  created_on = db.Column(db.String, nullable = False)
  cards = db.relationship("Card", secondary = "listcard", order_by = "Card.deadline")
  total = 0
  completed = 0
  pending = 0
  passed = 0

class LC(db.Model):
  __tablename__ = "listcard"
  id = db.Column(db.Integer, autoincrement = True, primary_key = True)
  list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), primary_key = True, nullable = False)
  card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), primary_key = True, nullable = False)
  
class Card(db.Model):
  __tablename__ = "cards"
  id = db.Column(db.Integer, autoincrement = True, primary_key = True)
  name = db.Column(db.String, nullable = False)
  description = db.Column(db.String)
  created_date = db.Column(db.String)
  edited_date = db.Column(db.String)
  deadline = db.Column(db.String)
  completed_date = db.Column(db.String)
  done = db.Column(db.Integer)