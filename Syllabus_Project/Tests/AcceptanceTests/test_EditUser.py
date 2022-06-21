from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users, Courses, PersonalInfo


class TestEditUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.inst_personal_info = PersonalInfo.objects.create(myName='Test admin user')
        self.user = Users.objects.create(user_username='Hmmm', user_password='Hmmm', role='Instructor',
                                         info=self.inst_personal_info)
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    # adding the same user with different role
    def test_add_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": 'Hmmm', "password": 'Hmmm',
                                                  "role": 'TA'})

        response2 = self.client.get('/adminPage')

        user = list(response2.context['users'])
        self.assertEqual(len(user), 2)
        print(user)

        for i in user:
            if i.role == "Admin":
                pass
            else:
                self.assertEqual(i.user_username, "Hmmm")
                self.assertEqual(i.role, "TA")

    # check if the changing the password works
    def test_add_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": 'Hmmm', "password": 'Yo',
                                                  "role": 'TA'})

        response2 = self.client.get('/adminPage')

        user = list(response2.context['users'])
        self.assertEqual(len(user), 2)
        print(user)

        for i in user:
            if i.role == "Admin":
                pass
            else:
                self.assertEqual(i.user_password, "Yo")
                self.assertEqual(i.role, "TA")