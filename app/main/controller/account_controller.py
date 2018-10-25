from flask_restplus import Resource

from app.main.dto.account_dto import AccountDTO

api = AccountDTO.api


@api.route('/')
class UnspecifiedAccount(Resource):
    @api.response(200, 'Account successfully created.')
    @api.response(400, 'An account already exists with the requested e-mail.')
    @api.expect(AccountDTO.account, validate=True)
    @api.doc('Register a new account.')
    def post(self):
        return 200, ''
