from flask_restplus import Resource

from app.main.dto.synonym_dto import SynonymDTO
import app.main.service.synonym_service as service

api = SynonymDTO.api


@api.route('')
class SynonymsResource(Resource):
    @api.doc('Retrieve a list of all the currently tracked synonyms.')
    def get(self):
        return [{synonym: count} for synonym, count in service.get_active_synonyms()]
