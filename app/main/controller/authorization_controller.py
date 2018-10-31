from flask import request
from flask_restplus import Resource

from app.main.dto.authorization_dto import AuthorizationDTO
from app.main.service.authorization_service import AuthorizationResponse, login, logout, get_is_authorized

api = AuthorizationDTO.api


@api.route('/login')
class Login(Resource):
    @api.response(AuthorizationResponse.Success, 'Account login successful.')
    @api.response(AuthorizationResponse.InvalidCredentials, 'Invalid or non-existing account credentials entered.')
    @api.doc('Perform a login request for an account.')
    @api.expect(AuthorizationDTO.authorization, validate=True)
    def post(self):
        return login(request.json)


@api.route('/logout')
class Logout(Resource):
    @api.response(AuthorizationResponse.Success, 'Logout successful.')
    @api.doc('Logout from a session.', security='jwt')
    def get(self):
        if not get_is_authorized():
            api.abort(403)

        return logout()
