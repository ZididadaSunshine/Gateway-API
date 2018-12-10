from locust import HttpLocust, TaskSet, task, seq_task
from random import randint

USER_CREDENTIALS = list()
WORDS = [line.strip() for line in open('/usr/share/dict/words')]

for i in range(1000, 0, -1):
    USER_CREDENTIALS.append({'username': f'User {i}', 'email': f'email{i}@example.com', 'password': f'password{i}'})


class UserBehavior(TaskSet):
    token = None
    credentials = None
    
    def login(self):
        res = self.client.post('/authorization/login', json={'email': self.credentials['email'],
                                                             'password': self.credentials['password']}).json()
        
        if res['success']:
            self.token = res['token']

        return res['success']

    def register(self):
        self.client.post('/accounts', json=self.credentials).json()

    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            self.credentials = USER_CREDENTIALS.pop()
        else:
            raise Exception('No available user credentials.')

        if not self.login():
            self.register()

        self.login()

    def on_stop(self):
        self.delete_all_brands()

        self.client.get('/authorization/logout', headers={'Authorization': self.token})

    def get_brand_dicts(self):
        return self.client.get('/brands', headers={'Authorization': self.token}).json()

    def delete_all_brands(self):
        for brand in self.get_brand_dicts():
            self.client.delete(f'/brands/{brand["id"]}', headers={'Authorization': self.token})

    @task
    def create_brand(self):
        self.client.post('/brands', json={'name': f'Locust {randint(0, 10000000)}'}, headers={'Authorization': self.token})

    @task
    def update_brand(self):
        for brand in self.get_brand_dicts():
            self.client.put(f'/brands/{brand["id"]}/synonyms', headers={'Authorization': self.token},
                            json={'name': f'Locust {randint(0, 10000000)}'})

    @task
    def get_brands(self):
        self.get_brand_dicts()

    @task
    def get_brand_synonyms(self):
        for brand in self.get_brand_dicts():
            self.client.get(f'/brands/{brand["id"]}/synonyms', headers={'Authorization': self.token})

    @task
    def delete_brand_synoynms(self):
        for brand in self.get_brand_dicts():
            synonyms = self.client.get(f'/brands/{brand["id"]}/synonyms', headers={'Authorization': self.token})

            for synonym in synonyms:
                self.client.delete(f'/brands/{brand["id"]}/synonyms/{synonym["synonym"]}',
                                   headers={'Authorization': self.token})


    @task
    def add_brand_synonyms(self):
        for brand in self.get_brand_dicts():
            self.client.post(f'/brands/{brand["id"]}/synonyms',json={'synonym': f'Synonym {randint(0, 10000000)}'},
                             headers={'Authorization': self.token})

    @task
    def delete_brands(self):
        self.delete_all_brands()


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 6000
