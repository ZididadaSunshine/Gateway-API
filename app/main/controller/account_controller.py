from flask import request
from flask_restplus import Resource

from app.main.dto.account_dto import AccountDTO
import app.main.service.account_service as service

api = AccountDTO.api


@api.route('')
class AccountsResource(Resource):
    @api.response(service.AccountServiceResponse.Created, 'Account successfully created.')
    @api.response(service.AccountServiceResponse.AlreadyExists, 'An account already exists with the requested e-mail.')
    @api.doc('Register a new account.')
    @api.expect(AccountDTO.account, validate=True)
    def post(self):
        return service.create_account(request.json)
