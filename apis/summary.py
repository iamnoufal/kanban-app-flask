from flask_restful import Resource, fields, marshal_with, reqparse
from application.db import db
from application.models import *
from .validations import *
from sqlalchemy import exc

opFields = {
  "graph": fields.String
}

class SummaryAPI(Resource):
  def get(self, user_id):
    user = db.session.query(User).filter(User.user_id == user_id).one()
    lists = user.lists
    names = []
    completed = []
    pending = []
    passed = []
    for i in lists:
      names.append(i.name)
      user.totalLists+=1
      for j in i.cards:
        i.total += 1
        if j.done:
          i.completed += 1
        elif datetime.today()>datetime.strptime(j.deadline, '%Y-%m-%dT%H:%M'):
          i.passed += 1
      i.pending = i.total-i.completed
      user.total += i.total
      user.completed += i.completed
      completed.append(i.completed)
      user.pending += i.pending
      pending.append(i.pending)
      user.passed += i.passed
      passed.append(i.passed)
    fig, axe = plt.subplots(dpi=1000)
    plt.ylim(0, max(pending+[10]))
    axe.bar(names, completed)
    axe.bar(names, pending, bottom = completed)
    axe.legend(["Completed Tasks", "Pending Tasks"])
    fig.savefig("static/"+user_id+"_summary.png", transparent=True)
    plt.close(fig)
    return user, lists, "http://127.0.0.1:5000/static/"+user_id+"_summary.png"