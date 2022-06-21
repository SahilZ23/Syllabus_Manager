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

        self.test_instructor_info = PersonalInfo.objects.create(myName='Test Instructor', officeLocation='EMS FLOOR 5',
                                                           officeNumber=512, phoneNumber='414-555-5501',
                                                           email='csdept@example.com', day='Monday, Tuesday',
                                                           timeFrom='8:00 AM', timeTo='10:00 AM')

    # changing the location
    def test_edit_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'password'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo', {"name": "Test Instructor", "OfficeLocation": "EMS", "OfficeNumber": 512,
                                                         "PhoneNumber": "414-555-5501", "email": "csdept@example.com",
                                                         "sectionStartTime": "8:00 AM", "sectionEndTime": "10:00 AM",
                                                         "Monday": "Monday"})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
            if i.officeLocation == "EMS":
                self.assertTrue("Successfully edited Office location")

    # changing the office number
    def test_edit_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'password'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo', {"name": "Test Instructor", "OfficeLocation": "EMS", "OfficeNumber": 122,
                                                         "PhoneNumber": "414-555-5501", "email": "csdept@example.com",
                                                         "sectionStartTime": "8:00 AM", "sectionEndTime": "10:00 AM",
                                                         "Monday": "Monday"})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
            if i.officeLocation == "EMS":
                self.assertTrue("Successfully edited Office location")

    # changing the phone number
    def test_edit_3(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'password'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo', {"name": "Test Instructor", "OfficeLocation": "EMS", "OfficeNumber": 122,
                                                         "PhoneNumber": "416-555-5501", "email": "csdept@example.com",
                                                         "sectionStartTime": "8:00 AM", "sectionEndTime": "10:00 AM",
                                                         "Monday": "Monday"})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
                if i.phoneNumber == "416-555-5501":
                    self.assertTrue("Successfully edited phone number")

    # changing email
    def test_edit_4(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'password'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo', {"name": "Test Instructor", "OfficeLocation": "EMS", "OfficeNumber": 122,
                                                         "PhoneNumber": "416-555-5501", "email": "csdept@uwm.com",
                                                         "sectionStartTime": "8:00 AM", "sectionEndTime": "10:00 AM",
                                                         "Monday": "Monday"})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
                if i.myName == "Jayson":
                    self.assertTrue("Successfully added personal info")

    # changing the time
    def test_edit_5(self):
        # login
        response = self.client.post('/', {'loginEmail': 'prof01', 'loginPassword': 'password'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/AddPersonalInfo', {"name": "Test Instructor", "OfficeLocation": "EMS", "OfficeNumber": 122,
                                                         "PhoneNumber": "416-555-5501", "email": "csdept@uwm.com",
                                                         "sectionStartTime": "11:00 AM", "sectionEndTime": "1:00 PM",
                                                         "Monday": "Monday"})

        self.pi = PersonalInfo.objects.all()

        self.assertEqual(len(self.pi), 1)

        for i in self.pi:
                if i.timeFrom == "11:00 AM":
                    self.assertTrue("Successfully edited time")