from flask_restplus import Resource

from app.main.dto.authorization_dto import AuthorizationDTO

api = AuthorizationDTO.api


@api.route('login')
class Login(Resource):
    @api.response(200, 'Account login successful.')
    @api.response(400, 'Invalid or non-existing account credentials entered.')
    @api.doc('Perform a login request for an account.')
    @api.expect(AuthorizationDTO.authorization, validate=True)
    def post(self):
        pass


@api.route('logout')
class Logout(Resource):
    pass
