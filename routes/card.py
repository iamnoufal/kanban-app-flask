from flask import current_app as app
from flask import request, redirect, render_template, session
from datetime import date, datetime
from sqlalchemy import exc
from application.models import *

@app.route("/list/<list_id>/create", methods = ['POST'])
def createCard(list_id):
  card = Card()
  card.name = request.form['name']
  card.description = request.form['desc']
  card.created_date = str(datetime.today())[:16]
  card.deadline = request.form['deadline']
  card.done = False
  try:
    db.session.add(card)
    db.session.commit()
    listcard = LC()
    listcard.list_id = list_id
    listcard.card_id = card.id
    db.session.add(listcard)
    db.session.commit()
  except exc.NoForeignKeysError:
    return "no list found"
  else:
    return redirect("/")

@app.route("/card/<card_id>/delete", methods=["GET", "POST"])
def deleteCard(card_id):
  db.session.query(LC).filter(LC.card_id == card_id).delete()
  db.session.query(Card).filter(Card.id == card_id).delete()
  db.session.commit()
  return redirect("/")

@app.route("/card/<card_id>/edit", methods=["GET", "POST"])
def editCard(card_id):
  card = db.session.query(Card).filter(Card.id == card_id).one()
  listcard = db.session.query(LC).filter(LC.card_id == card_id).one()
  card.name = request.form['name']
  card.description = request.form['desc']
  card.deadline = request.form['deadline']
  card.edited_date = str(datetime.today())[:16]
  listcard.list_id = int(request.form['list'])
  db.session.commit()
  return redirect("/")

@app.route("/card/<card_id>/done")
def doneCard(card_id):
  card = db.session.query(Card).filter(Card.id == card_id).one()
  card.done = not card.done
  card.completed_date = str(datetime.today())[:16] if card.done else None
  db.session.commit()
  return redirect("/")

@app.route("/card/<card_id>/change/<list_id>")
def changeList(card_id, list_id):
  lc = db.session.query(LC).filter(LC.card_id == card_id).one()
  lc.list_id = list_id
  db.session.commit()
  return redirect('/')