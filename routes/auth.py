from datetime import datetime
from flask import current_app as app
from flask import request, render_template, session, redirect
from application.db import db
from application.models import *
from sqlalchemy import exc

@app.route("/auth/<method>", methods = ["GET", "POST"])
def auth(method):
  if request.method == "GET":
    session['auth'] = False
    return render_template("login.html") if method=="login" else render_template("signup.html")
  else:
    user_id = request.form['user_id']
    pwd = request.form['pwd']
    if method == "login":
      try:
        user = db.session.query(User).filter(User.user_id == user_id).one()
      except exc.NoResultFound:
        return render_template("login.html", msg="User ID doesn't exist")
      else:
        if user.pwd == pwd:
          session['auth'] = True
          session['user_id'] = user_id
          user.last_login = str(datetime.today())[:16]
          db.session.commit()
          return redirect("/"+user_id+"/lists")
        else:
          return render_template("login.html", msg="Password doesn't match")
    else:
      user = User()
      user.user_id = request.form['user_id']
      user.pwd = request.form['pwd']
      user.name = request.form['fname']+" "+request.form['lname']
      user.created_on = str(datetime.today())[:16]
      user.last_login = str(datetime.today())[:16]
      try:
        db.session.add(user)
        db.session.commit()
      except exc.IntegrityError:
        return render_template('signup.html', msg="User ID already exists")
      else:
        session['auth'] = True
        session['user_id'] = user.user_id
        return redirect('/'+user.user_id+'/lists')

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")