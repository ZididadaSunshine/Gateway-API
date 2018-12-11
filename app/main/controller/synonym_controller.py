from flask import request
from flask_restplus import Resource

import app.main.service.authorization_service as authorization_service
import app.main.service.synonym_service as synonym_service
from app.main.dto.synonym_dto import SynonymDTO

api = SynonymDTO.api


def get_key():
    return request.headers.get('Authorization')


def key_required(api):
    def wrapper(func):
        def check_auth(*args, **kwargs):
            if not authorization_service.is_key_correct(get_key()):
                api.abort(authorization_service.AuthorizationResponse.Unauthorized)

            return func(*args, **kwargs)

        return check_auth

    return wrapper


@api.route('')
class SynonymsResource(Resource):
    @api.doc('Retrieve a list of all the currently tracked synonyms.', security='key')
    @key_required(api)
    def get(self):
        return dict(synonym_service.get_active_synonyms())
