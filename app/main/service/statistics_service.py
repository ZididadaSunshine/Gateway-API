import requests
import os


def get_statistics(request_json):
    print(request_json)
    return requests.post(f'http://{os.environ["STATISTICS_API_HOST"]}/api/statistics', json=request_json)
