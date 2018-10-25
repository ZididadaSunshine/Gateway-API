
from flask_restplus import fields, Namespace


class AuthorizationDTO:
    api = Namespace('Authorization', description='Authorization operations.')
    authorization = api.model('Authorization Details', {
        'email': fields.String(required=True, description='E-mail address to login with.'),
        'username': fields.String(required=True, description='Password associated with the e-mail address.')
    })
