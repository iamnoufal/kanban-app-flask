from werkzeug.exceptions import HTTPException
from flask import make_response
import json

class NotFoundError(HTTPException):
  def __init__(self, code, emsg):
    self.response = make_response(emsg, code)

class ValidationError(HTTPException):
  def __init__(self, code, emsg):
    self.response = make_response(emsg, code)

class DuplicateError(HTTPException):
  def __init__(self, code, emsg):
    self.response = make_response(emsg, code)