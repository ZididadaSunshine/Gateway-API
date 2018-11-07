from flask import request
from flask_restplus import Resource

from app.main.dto.authorization_dto import AuthorizationDTO
import app.main.service.authorization_service as service

api = AuthorizationDTO.api


def get_token():
    return request.headers.get('Authorization')


def auth_required(api):
    def wrapper(func):
        def check_auth(*args, **kwargs):
            if not service.is_authorized(get_token()):
                api.abort(403)

            return func(*args, **kwargs)

        return check_auth

    return wrapper


@api.route('/login')
class Login(Resource):
    @api.response(service.AuthorizationResponse.Success, 'Account login successful.')
    @api.response(service.AuthorizationResponse.InvalidCredentials, 'Invalid account credentials entered.')
    @api.doc('Perform a login request for an account.')
    @api.expect(AuthorizationDTO.authorization, validate=True)
    def post(self):
        return service.login(request.json)


@api.route('/logout')
class Logout(Resource):
    @api.response(service.AuthorizationResponse.Success, 'Logout successful.')
    @api.doc('Logout from a session.', security='jwt')
    def get(self):
        return service.logout(get_token())
