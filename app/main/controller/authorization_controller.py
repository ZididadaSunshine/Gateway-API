from flask_restplus import Resource

from app.main.dto.authorization_dto import AuthorizationDTO

api = AuthorizationDTO.api


@api.route('login')
class Login(Resource):
    @api.doc('User login.')
    @api.expect(AuthorizationDTO.authorization, validate=True)
    def get(self):
        pass
