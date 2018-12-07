from flask import request
from flask_restplus import Resource

from app.main.controller.authorization_controller import auth_required, get_token
from app.main.dto.statistics_dto import StatisticsDTO
from app.main.service import brand_service, synonym_service
from app.main.service.authorization_service import get_account_id
from app.main.service.statistics_service import get_statistics

api = StatisticsDTO.api


@api.route('')
class StatisticsResource(Resource):
    @api.doc('Retrieve statistics from a time range.', security='jwt')
    @api.expect(StatisticsDTO.timerange, validate=True)
    @api.response(404, 'Requested brand does not exist or does not belong to the user.')
    @api.response(400, 'Requested brand does not have any synonyms.')
    @auth_required(api)
    def post(self):
        brand = brand_service.get_brand_by_id(get_account_id(get_token()), request.json['brand_id'])

        if not brand:
            api.abort(404)

        # Get synonyms from brand
        synonyms = [synonym.synonym for synonym in synonym_service.get_brand_synonyms(brand.id)]
        if not synonyms:
            api.abort(400)

        request_data = {
            'from': request.json['from'],
            'to': request.json['to'],
            'granularity': request.json['granularity'],
            'synonyms': synonyms
        }

        statistics_response = get_statistics(request_data)

        return statistics_response.json(), statistics_response.status_code
