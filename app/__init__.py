from flask import Blueprint
from flask_restplus import Api

from app.main.controller.authorization_controller import api as authorization_namespace
from app.main.controller.account_controller import api as account_namespace

blueprint = Blueprint('sw7-gateway-api', __name__)

api = Api(blueprint, title='SW7 Gateway API', version='1.0')

# Add namespaces to API
api.add_namespace(authorization_namespace, path='/')
api.add_namespace(account_namespace, path='/account')
