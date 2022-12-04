from flask import current_app as app
from flask import render_template, request, redirect
from sqlalchemy import exc
from application.models import *
from application.db import db
from datetime import date, datetime

@app.route("/<user_id>/lists")
def lists(user_id):
  user = db.session.query(User).filter(User.user_id == user_id).one()
  lists = user.lists
  for i in lists:
    cards = []
    completedCards = []
    for j in i.cards:
      cards.append(j) if not j.done else completedCards.append(j)
    cards+=completedCards
    i.cards = cards
  return render_template("lists.html", lists = lists, date=date, datetime = datetime)
  
@app.route("/<user_id>/create", methods=['POST'])
def addList(user_id):
  list = List()
  list.name = request.form['name']
  list.desc = request.form['desc']
  list.created_on = str(datetime.today())[:16]
  try:
    db.session.add(list)
    db.session.commit()
    userlist = UL()
    userlist.user_id = db.session.query(User).filter(User.user_id == user_id).one().id
    userlist.list_id = list.id
    db.session.add(userlist)
    db.session.commit()
  except exc.NoForeignKeysError:
    return "no user found"
  else:
    return redirect("/")

@app.route("/list/<list_id>/edit", methods=['POST'])
def editList(list_id):
  list = db.session.query(List).filter(List.id == list_id).one()
  list.name = request.form['name']
  list.desc = request.form['desc']
  try:
    db.session.commit()
  except:
    return "error"
  else:
    return redirect("/")

@app.route("/list/<list_id>/delete", methods=["GET", 'POST'])
def deleteList(list_id):
  db.session.query(List).filter(List.id == list_id).delete()
  db.session.query(UL).filter(UL.list_id == list_id).delete()
  db.session.commit()
  return redirect("/")
