from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users, Courses, PersonalInfo


class TestAddUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.inst_personal_info = PersonalInfo.objects.create(myName='Test admin user')
        self.user = Users.objects.create(user_username='Hmmm', user_password='Hmmm', role='Instructor',
                                         info=self.inst_personal_info)
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    # adding a user with valid types
    def test_add_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": 'Hmmm', "password": 'Hmmm',
                                                  "role": 'Instructor'})

        response2 = self.client.get('/adminPage')

        user = list(response2.context['users'])
        print(user)

        for i in user:
            if i.role == "Admin":
                pass
            else:
                self.assertEqual(i.user_username, "Hmmm")
                self.assertEqual(i.role, "Instructor")

    # adding user with username being an invalid type
    def test_add_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a user with invalid type
        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": 111, "password": 'Hmmm',
                                                  "role": 'Instructor'})

        response2 = self.client.get('/adminPage')

        user = list(response2.context['users'])
        print(user)

        for i in user:
            if isinstance(i.user_username, int):
                self.assertFalse("username cannot be an integer")

    # adding user with role being an invalid type
    def test_add_3(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a user with invalid type
        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": "Yo", "password": 'Hmmm',
                                                  "role": 100})

        response2 = self.client.get('/adminPage')

        user = list(response2.context['users'])
        print(user)

        for i in user:
            if isinstance(i.role, int):
                self.assertFalse("username cannot be an integer")

    # adding user with password being an invalid type
    def test_add_4(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a user with invalid type
        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": "yo", "password": 222,
                                                  "role": "TA"})

        response2 = self.client.get('/adminPage')

        user = list(response2.context['users'])

        for i in user:
            if isinstance(i.user_password, int):
                self.assertFalse("password cannot be an integer")
