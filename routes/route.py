from flask import current_app as app
from flask import redirect
from flask import session

from application.models import *

@app.route('/', methods=['GET'])
def home():
  if "auth" not in session or ("auth" in session and not session['auth']):
    return redirect("/auth/signup")
  user_id = session['user_id']
  return redirect("/"+user_id+"/lists")