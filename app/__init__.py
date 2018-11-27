from flask import Blueprint
from flask_restplus import Api

from app.main.controller.authorization_controller import api as authorization_namespace
from app.main.controller.account_controller import api as account_namespace
from app.main.controller.brand_controller import api as brand_namespace
from app.main.controller.synonym_controller import api as synonym_namespace

blueprint = Blueprint('sw7-gateway-api', __name__, url_prefix='/api')

api = Api(blueprint, title='SW7 Gateway API', version='1.0', authorizations={'jwt': {'type': 'apiKey',
                                                                                     'in': 'header',
                                                                                     'name': 'Authorization'},
                                                                             'key': {'type': 'apiKey',
                                                                                     'in': 'header',
                                                                                     'name': 'API-Key'}})

# Add namespaces to API
api.add_namespace(authorization_namespace, path='/authorization')
api.add_namespace(account_namespace, path='/accounts')
api.add_namespace(brand_namespace, path='/brands')
api.add_namespace(synonym_namespace, path='/synonyms')
