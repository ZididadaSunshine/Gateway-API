from flask import request
from flask_restplus import Resource

from app.main.dto.statistics_dto import StatisticsDTO
from app.main.service.statistics_service import get_statistics

api = StatisticsDTO.api


@api.route('')
class StatisticsResource(Resource):
    @api.doc('Retrieve statistics from a time range.')
    @api.expect(StatisticsDTO.timerange, validate=True)
    def post(self):
        response = get_statistics(request.json)

        return response.json(), response.status_code
