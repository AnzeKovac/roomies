"""Test class"""
import unittest
import json
import requests

VARS = {'room_id': '',
        'task_id': '',
        'user_id': ''}


# noinspection PyCompatibility
class TestROOMIES(unittest.TestCase):
    """ Class for testing the robustness of the code
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = 'TestingUser'
        self.password = 'TestingUser'
        self.room_name = 'TestingUser'
        self.awardPoints = 10

        self.url = 'http://127.0.0.1:5000/'
        #self.url = 'http://lazykiller.herokuapp.com/'
        self.headers = {'content-type': 'application/json'}

    def test000_register_conflict(self):
        parameter = {'newRoom': 'false'}
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'register', params=parameter, data=json.dumps(payload),
                                 headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 409)
        self.assertEqual(token['error'], 'There was a conflict. Room name does not exist')

    def test001_register_with_room(self):
        parameter = {'newRoom': 'true'}
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'register', params=parameter, data=json.dumps(payload),
                                 headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 200)
        self.assertEqual(token['room']['name'], self.room_name)
        self.assertEqual(token['username'], self.username)

        VARS['user_id'] = token['_id']
        VARS['room_id'] = token['room']['id']

    def test002_login(self):
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'login', data=json.dumps(payload), headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 200)
        self.assertEqual(token['room']['name'], self.room_name)
        self.assertEqual(token['username'], self.username)

    def test003_register_conflict(self):
        parameter = {'newRoom': 'true'}
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'register', params=parameter, data=json.dumps(payload),
                                 headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 409)
        self.assertEqual(token['error'], 'There was a conflict. Room name is already taken')

    def test004_login_conflict(self):
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': 'Login to the room which does not exist'
            }
        }

        response = requests.post(self.url + 'login', data=json.dumps(payload), headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 401)
        self.assertEqual(token['error'], 'Room is not existent')

    def test005_login_conflict(self):
        payload = {
            'username': self.username,
            'password': 'wrong password',
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'login', data=json.dumps(payload), headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 401)
        self.assertEqual(token['error'], 'Login failed')

        payload = {
            'username': 'wrong username',
            'password': 'wrong password',
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'login', data=json.dumps(payload), headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 401)
        self.assertEqual(token['error'], 'Login failed')

        payload = {
            'username': 'wrong username',
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'login', data=json.dumps(payload), headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 401)
        self.assertEqual(token['error'], 'Login failed')

    def test006_wrong_parameter(self):
        parameter = {'newRoom': 'typoInParameter'}
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'register', params=parameter, data=json.dumps(payload),
                                 headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 400)
        self.assertEqual(token['error'], 'The request could not be understood by the server due to malformed syntax.')

    def test007_register_in_room(self):
        parameter = {'newRoom': 'false'}
        payload = {
            'username': 'new username',
            'password': 'new password',
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'register', params=parameter, data=json.dumps(payload),
                                 headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 200)
        self.assertEqual(token['room']['name'], self.room_name)
        self.assertEqual(token['username'], 'new username')

    def test008_register_conflict(self):
        parameter = {'newRoom': 'false'}
        payload = {
            'username': self.username,
            'password': self.password,
            'room': {
                'name': self.room_name
            }
        }

        response = requests.post(self.url + 'register', params=parameter, data=json.dumps(payload),
                                 headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 409)
        self.assertEqual(token['error'], 'There was a conflict. Username for this room is taken')

    def test009_add_tasks(self):
        payload = {
            'taskName': 'Pospravi kuhinjo',
            'additionalDescription': 'Počisti lijak, hladilnik in posesaj!',
            'awardPoints': self.awardPoints,
            'room': VARS['room_id']
        }

        response = requests.post(self.url + 'task/add', data=json.dumps(payload), headers=self.headers)
        token = response.json()

        self.assertTrue(response.status_code, 200)
        self.assertTrue(token['status'], 'new')
        VARS['task_id'] = token['id']

    def test010_update_task(self):
        payload = {
            'taskName': 'Pospravi kuhinjo - popravljeno ime'
        }

        response = requests.put(self.url + 'task/' + VARS['task_id'], data=payload)
        token = response.content

        self.assertTrue(response.status_code, 200)
        self.assertTrue(token, 'Update OK')

        response = requests.get(self.url + 'task/' + VARS['task_id'])
        token = response.json()

        self.assertTrue(response.status_code, 200)
        self.assertTrue(token['id'], VARS['room_id'])
        self.assertTrue(token['taskName'], 'Pospravi kuhinjo - popravljeno ime')

    def test011_accomplish_task(self):
        endpoint = 'task/' + VARS['task_id'] + '/accomplish/' + VARS['user_id']
        response = requests.put(self.url + endpoint)

        token = response.json()

        self.assertTrue(response.status_code, 200)
        self.assertTrue(token['roomId'], VARS['room_id'])
        self.assertTrue(token['taskId'], VARS['task_id'])
        self.assertTrue(token['userId'], VARS['user_id'])
        self.assertTrue(token['userName'], self.username)

    def test012_statistics(self):
        endpoint = 'statistics/' + VARS['room_id']
        response = requests.get(self.url + endpoint)
        self.assertTrue(response.status_code, 200)

        token = response.json()

        self.assertEqual(len(token), 2)
        self.assertEqual(token[0]['points'], 0)
        self.assertEqual(token[0]['tasksNumber'], 0)
        self.assertEqual(token[1]['points'], 10)
        self.assertEqual(token[1]['tasksNumber'], 1)

    def test013_testServer_online(self):
        response = requests.get(self.url)
        self.assertTrue(response.status_code, 200)
