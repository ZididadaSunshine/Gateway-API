from flask_restplus import fields, Namespace


class AccountDTO:
    api = Namespace('Account', description='Account operations.')
    account = api.model('Account details', {
        'email': fields.String(required=True, description='E-mail address for account.'),
        'username': fields.String(required=True, description='Password associated with the e-mail address.'),
        'first_name': fields.String(required=True, description='First name of account owner.'),
        'last_name': fields.String(required=True, description='Last name of account owner.'),
    })
