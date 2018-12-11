import datetime
import os

import requests

from app.main import db
from app.main.model.brand_model import Brand
from app.main.service import synonym_service


def get_overview_statistics(granularity, request_json):
    return requests.post(f'http://{os.environ["STATISTICS_API_HOST"]}/api/statistics/{granularity}/overview',
                         json=request_json)


def get_brand_sentiment(brand):
    # If delta is updated, the delta string in the POST request should also be updated
    delta = datetime.timedelta(days=1)

    average = None
    trend = None

    # Check if an update is necessary
    last_updated = brand.sentiment_updated_at
    now = datetime.datetime.utcnow()
    if not last_updated or now - last_updated > delta:
        synonyms = [synonym.synonym for synonym in synonym_service.get_brand_synonyms(brand.id)]
        if synonyms:
            response = requests.post(f'http://{os.environ["STATISTICS_API_HOST"]}/api/statistics/day/average',
                                     json=dict(synonyms=synonyms)).json()

            # Update brand with new values
            average = response['average']
            trend = response['trend']

            # Update brand with new values
            Brand.query.filter_by(id=brand.id).update(dict(sentiment_average=average, sentiment_trend=trend,
                                                           sentiment_updated_at=now))
            db.session.commit()
    else:
        average = brand.sentiment_average
        trend = brand.sentiment_trend

    return {
        'average': average,
        'trend': trend
    }
