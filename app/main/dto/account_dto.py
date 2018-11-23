from flask_restplus import fields, Namespace


class AccountDTO:
    api = Namespace('Account', description='Account operations.')

    account = api.model('Account details', {
        'email': fields.String(required=True, description='E-mail address for account.'),
        'username': fields.String(required=True, description='A non-unique name associated with the account owner.'),
        'password': fields.String(required=True, description='Password associated with the e-mail address.')
    })
