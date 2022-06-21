from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users, PersonalInfo


class TestDeleteUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    def test_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a user
        response1 = self.client.post('/addUser', {"fullname": 'Hmmm', "username": 'Hmmm', "password": 'Hmmm',
                                                  "role": 'Instructor'})
        # delete the user
        response2 = self.client.post('/deleteUser', {"User": 2})

        # go to the admin page
        response3 = self.client.get('/adminPage')

        users = list(response3.context['users'])
        print(users)

        # since we only add 1 user, on deleting one the list should be of size 1
        if len(users) == 1:
            self.assertTrue("Successful Deletion")
        else:
            self.assertFalse("Successful Deletion")

    def test_2(self):
        pass