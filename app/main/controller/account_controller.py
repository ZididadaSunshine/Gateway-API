from flask import request
from flask_restplus import Resource

from app.main.dto.account_dto import AccountDTO
from app.main.service.account_service import AccountServiceResponse, create_account

api = AccountDTO.api


@api.route('')
class AccountsResource(Resource):
    @api.response(AccountServiceResponse.Created, 'Account successfully created.')
    @api.response(AccountServiceResponse.AlreadyExists, 'An account already exists with the requested e-mail.')
    @api.doc('Register a new account')
    @api.expect(AccountDTO.account, validate=True)
    def post(self):
        return create_account(request.json)

