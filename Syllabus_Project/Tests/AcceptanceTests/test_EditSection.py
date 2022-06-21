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
        self.compsci_2 = Courses.objects.create(courseName='Advanced Fortran', courseNumber=452, semester='Spring',
                                                year=2021)

        time1 = time(2, 0)
        time2 = time(12, 0)
        self.user = Users.objects.create(user_username='user', user_password='user@123', role='Instructor')
        self.sec = Section.objects.create(day='Monday', timeFrom = time2,
                                          timeTo=time1, class_room='EMS 200',
                                          section_number=122, users=self.instructor_user,
                                          courses=self.compsci_1)

    # add same section with different day
    def test_edit_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '12:00 PM',
                                                     "endTime": '2:00 PM', "Tuesday": "Tuesday"
                                                     , "sectionRoom": "EMS 200", "Course": 1, "User": 1})

        response3 = self.client.get('/adminPage')
        sections = list(response3.context["sections"])

        self.assertEqual(len(sections), 1)

        for i in sections:
            print(i.day)
            self.assertEqual(i.day, "Tuesday")

    # add the same section with different room
    def test_edit_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '12:00 PM',
                                                     "endTime": '2:00 PM', "Tuesday": "Tuesday"
                                                     , "sectionRoom": "EMS 202", "Course": 1, "User": 1})

        response3 = self.client.get('/adminPage')
        sections = list(response3.context["sections"])

        self.assertEqual(len(sections), 1)

        for i in sections:
            print(i.day)
            self.assertEqual(i.class_room, "EMS 202")

    # add the same section with different time
    def test_edit_3(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '1:00 PM',
                                                     "endTime": '2:00 PM', "Tuesday": "Tuesday"
                                                     , "sectionRoom": "EMS 200", "Course": 1, "User": 1})

        response3 = self.client.get('/adminPage')
        sections = list(response3.context["sections"])

        self.assertEqual(len(sections), 1)
        time1 = time(1, 0)
        time2 = time(2, 0)

        for i in sections:
            print(i.day)

            self.assertEqual(i.timeFrom, time1)
            self.assertEqual(i.timeTo, time2)

    # change user
    def test_edit_4(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '1:00 PM',
                                                     "endTime": '2:00 PM', "Tuesday": "Tuesday"
            , "sectionRoom": "EMS 200", "Course": 1, "User": 2})

        response3 = self.client.get('/adminPage')
        sections = list(response3.context["sections"])

        self.assertEqual(len(sections), 1)
        time1 = time(1, 0)
        time2 = time(2, 0)

        for i in sections:
            self.assertEqual(i.users, self.instructor_user)

    # change course
    def test_edit_5(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a section
        response1 = self.client.post('/addSection', {"sectionNumber": 122, "startTime": '1:00 PM',
                                                     "endTime": '2:00 PM', "Tuesday": "Tuesday"
            , "sectionRoom": "EMS 200", "Course": 2, "User": 2})

        response3 = self.client.get('/adminPage')
        sections = list(response3.context["sections"])

        self.assertEqual(len(sections), 1)
        time1 = time(1, 0)
        time2 = time(2, 0)

        for i in sections:
            self.assertEqual(i.users, self.instructor_user)