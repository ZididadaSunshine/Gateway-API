from flask import Blueprint
from flask_restplus import Api

from app.main.controller.authorization_controller import api as authorization_namespace
from app.main.controller.account_controller import api as account_namespace
from app.main.controller.brand_controller import api as brand_namespace

blueprint = Blueprint('sw7-gateway-api', __name__)

api = Api(blueprint, title='SW7 Gateway API', version='1.0', authorizations={'jwt': {'type': 'apiKey',
                                                                                     'in': 'header',
                                                                                     'name': 'Authorization'}})

# Add namespaces to API
api.add_namespace(authorization_namespace, path='/authorization')
api.add_namespace(account_namespace, path='/accounts')
api.add_namespace(brand_namespace, path='/brands')
