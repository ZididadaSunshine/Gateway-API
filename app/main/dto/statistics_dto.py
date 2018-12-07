from flask_restplus import Namespace, fields


class StatisticsDTO:
    api = Namespace('Statistics', description='Statistics operations.')

    timerange = api.model('Time range', {
        'from': fields.DateTime(required=True, description='The date and time which the time range spans from.'),
        'to': fields.DateTime(required=True, description='The date and time which the time range spans to.'),
        'brand_id': fields.Integer(required=True, description='Brand identifier to retrieve statistics for.'),
        'granularity': fields.String(required=True, description='The granularity of the returned statistics')
    })
