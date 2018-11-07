from flask import request
from flask_restplus import Resource

from app.main.decorator.auth_decorator import auth_required
from app.main.dto.authorization_dto import AuthorizationDTO
import app.main.service.authorization_service as service

api = AuthorizationDTO.api


@api.route('/login')
class Login(Resource):
    @api.response(service.AuthorizationResponse.Success, 'Account login successful.')
    @api.response(service.AuthorizationResponse.InvalidCredentials, 'Invalid or non-existing account credentials entered.')
    @api.doc('Perform a login request for an account.')
    @api.expect(AuthorizationDTO.authorization, validate=True)
    def post(self):
        return service.login(request.json)


@api.route('/logout')
class Logout(Resource):
    @api.response(service.AuthorizationResponse.Success, 'Logout successful.')
    @api.doc('Logout from a session.', security='jwt')
    @auth_required(api)
    def get(self):
        return service.logout(service.get_token())
