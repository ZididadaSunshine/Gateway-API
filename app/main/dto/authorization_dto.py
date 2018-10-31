
from flask_restplus import fields, Namespace


class AuthorizationDTO:
    api = Namespace('Authorization', description='Authorization operations.')

    authorization = api.model('Authorization details', {
        'email': fields.String(required=True, description='E-mail address associated with the account to login.'),
        'password': fields.String(required=True, description='Password associated with the account to login.')
    })
