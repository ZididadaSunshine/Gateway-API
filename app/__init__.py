from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('sw7-restful-api', __name__)

api = Api(blueprint, title='SW7 RESTful API', version='1.0')

#api.add_namespace(account_namespace, path='/account')