import datetime
import fcntl
import json
import random
from random import randint
from time import sleep

from locust import HttpLocust, TaskSet, task, events


def _format_log_date():
    return datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%d %H:%M:%S.%f')


def _append_line_exclusive(file, contents):
    with open(file, 'a') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(contents + '\n')
        fcntl.flock(file, fcntl.LOCK_UN)


def success(request_type, name, response_time, response_length):
    _append_line_exclusive('response_times.dat', f'{_format_log_date()}={response_time}')


events.request_success += success


consumer_count = 0
SYNONYMS = 250000
USERS = 100000

AVAILABLE_USERS = list(range(1, USERS + 1))


def get_brand():
    return f'Synonym {random.randint(1, SYNONYMS)}'


def get_account():
    id = AVAILABLE_USERS.pop()

    return {'username': f'User {id}', 'email': f'email{id}@example.com', 'password': f'password4'}


def get_extra_account():
    id = random.uniform(0, 1)

    return {'username': f'ExtraUser {id}', 'email': f'extra_email{id}@example.com', 'password': f'password4'}


class UserBehavior(TaskSet):
    token = None
    credentials = None
    logged_in = False

    def login(self):
        res = self.client.post('/authorization/login', json={'email': self.credentials['email'],
                                                             'password': self.credentials['password']}).json()

        if res['success']:
            self.token = res['token']
            #print(self.token)
            self.logged_in = res['success']

        return res['success']

    def logout(self):
        self.logged_in = False
        self.client.get('/authorization/logout', headers={'Authorization': self.token})

    def register(self, credentials):
        self.client.post('/accounts', json=credentials).json()

    def on_start(self):
        global consumer_count
        consumer_count += 1
        _append_line_exclusive('concurrent_consumers.dat', f'{_format_log_date()}={consumer_count}')

        self.credentials = get_account()
        #print(self.credentials)
        self.login()

    def ensure_logged_in(self):
        if not self.logged_in:
            self.login()

            sleep(5)

    #def on_stop(self):
    #    self.ensure_logged_in()
    #
    #    self.logout()

    def get_brand_dicts(self):
        self.ensure_logged_in()

        response = self.client.get('/brands', headers={'Authorization': self.token})
        if response.status_code != 200:
            print(response.text)

        self.wait()

        return response.json()

    def delete_brand(self):
        self.ensure_logged_in()

        for brand in self.get_brand_dicts():
            self.client.delete(f'/brands/{brand["id"]}', headers={'Authorization': self.token})

            continue

    @task(5)
    def create_user(self):
        self.register(get_extra_account())

    @task(1)
    def random_logout(self):
        self.logout()

    @task(5)
    def create_brand(self):
        self.ensure_logged_in()

        self.client.post('/brands', json={'name': get_brand()},
                         headers={'Authorization': self.token})

    @task(15)
    def update_brand(self):
        self.ensure_logged_in()

        for brand in self.get_brand_dicts():
            self.client.put(f'/brands/{brand["id"]}', headers={'Authorization': self.token},
                            json={'name': get_brand()})

    @task(10)
    def get_brands(self):
        self.ensure_logged_in()

        self.get_brand_dicts()

    @task(10)
    def get_brand_synonyms(self):
        self.ensure_logged_in()

        for brand in self.get_brand_dicts():
            #print(brand)

            self.client.get(f'/brands/{brand["id"]}/synonyms', headers={'Authorization': self.token})

    @task(10)
    def add_brand_synonyms(self):
        self.ensure_logged_in()

        for brand in self.get_brand_dicts():
            self.client.post(f'/brands/{brand["id"]}/synonyms', json={'synonym': f'Synonym {randint(0, 10000000)}'},
                             headers={'Authorization': self.token})

    @task(5)
    def delete_brands(self):
        self.ensure_logged_in()

        self.delete_brand()


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 10000
