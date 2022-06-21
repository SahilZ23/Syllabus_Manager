from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users, PersonalInfo
from datetime import time


class TestAddPersonalInfo(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor_user = Users.objects.create(role="Instructor", user_username='prof01',
                                                    user_password='password')
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    def test_add_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'password'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo', {"name": "Prof", "OfficeLocation": "EMS", "OfficeNumber": 122,
                                                         "PhoneNumber": "4144144144", "email": "prof@uwm.edu",
                                                         "sectionStartTime": "12:00 PM", "sectionEndTime": "1:00 PM",
                                                         "Monday": "Monday"})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 0)

        for i in self.pi:
            if i.myName == "Prof":
                self.assertTrue("Successfully added personal info")

