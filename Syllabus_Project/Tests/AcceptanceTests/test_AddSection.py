from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Section, Users, Courses
from datetime import time


class TestAddSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")
        self.instructor_user = Users.objects.create(role=("Instructor", "Instructor"), user_username='prof01',
                                                    user_password='password')
        self.compsci_1 = Courses.objects.create(courseName='Introduction to the calculator',
                                                courseNumber=150, semester='Spring', year=2021)

        time1 = time(2, 0)
        time2 = time(12, 0)
        self.user = Users.objects.create(user_username='user', user_password='user@123', role='Instructor')
        self.sec = Section.objects.create(day='Monday', timeFrom = time2,
                                          timeTo=time1, class_room='EMS 200',
                                          section_number=122, users=self.instructor_user,
                                          courses=self.compsci_1)

    # add a valid section
    def test_add_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '12:00 PM',
                                                     "endTime": '2:00 PM', "Monday": 'Monday'
                                                     , "sectionRoom": "EMS 200", "Course": 1, "User": 1})

        response3 = self.client.get('/adminPage')
        sections = list(response3.context["sections"])

        for i in sections:
            print(i.day)
            self.assertEqual(i.day, self.sec.day)
            self.assertEqual(i.timeFrom, self.sec.timeFrom)
            self.assertEqual(i.timeTo, self.sec.timeTo)
            self.assertEqual(i.section_number, self.sec.section_number)

    def test_add_invalid_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '12:00 PM',
                                                     "endTime": '2:00 PM', "Monday": 'Monday'
                                                     , "sectionRoom": "EMS 200", "Course": 1, "User": "1"})

    def test_add_invalid_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '12:00 PM',
                                                     "endTime": '2:00 PM', "Monday": 'Monday'
                                                     , "sectionRoom": "EMS 200", "Course": "1", "User": 1})

        # if the input is invalid it refreshes
        # this test fails because upon adding invalid input it does not redirect to same page
        self.assertEqual(response1.url, '/addSection')
