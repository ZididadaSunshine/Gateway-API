import datetime
import os

import requests

from app.main import db
from app.main.model.brand_model import Brand
from app.main.service import synonym_service


def get_overview_statistics(granularity, request_json):
    return requests.post(f'http://{os.environ["STATISTICS_API_HOST"]}/api/statistics/{granularity}/overview',
                         json=request_json)


def get_brand_statistics(brand):
    # If delta is updated, the delta string in the POST request should also be updated
    delta = datetime.timedelta(days=1)

    sentiment_average = None
    sentiment_trend = None
    posts = None

    # Check if an update is necessary
    last_updated = brand.statistics_updated_at
    now = datetime.datetime.utcnow()
    if not last_updated or now - last_updated > delta / 4:
        synonyms = [synonym.synonym for synonym in synonym_service.get_brand_synonyms(brand.id)]
        if synonyms:
            response = requests.post(f'http://{os.environ["STATISTICS_API_HOST"]}/api/statistics/day/brand',
                                     json=dict(synonyms=synonyms)).json()

            # Update brand with new values
            sentiment_average = response['sentiment_average']
            sentiment_trend = response['sentiment_trend']
            posts = response['posts']

            # Update brand with new values
            Brand.query.filter_by(id=brand.id).update(dict(sentiment_average=sentiment_average, posts=posts,
                                                           sentiment_trend=sentiment_trend, statistics_updated_at=now))
            db.session.commit()
    else:
        sentiment_average = brand.sentiment_average
        sentiment_trend = brand.sentiment_trend
        posts = brand.posts

    return {
        'sentiment_average': sentiment_average,
        'sentiment_trend': sentiment_trend,
        'posts': posts
    }
