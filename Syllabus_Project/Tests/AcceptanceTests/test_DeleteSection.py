from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Section, Users, Courses
import datetime


class TestDeleteSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")
        self.instructor_user = Users.objects.create(role=("Instructor", "Instructor"), user_username='prof01',
                                                    user_password='password')
        self.compsci_1 = Courses.objects.create(courseName='Introduction to the calculator',
                                                courseNumber=150, semester='Spring', year=2021)
        self.user = Users.objects.create(user_username='user', user_password='user@123', role='Instructor')
        self.sec = Section.objects.create(day='Monday, Wednesday, Friday', timeFrom = '12:30 PM',
                                          timeTo='3:00 PM', class_room='EMS Lecture 105',
                                          section_number=418, users=self.instructor_user,
                                          courses=self.compsci_1)

    def test_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # delete
        response2 = self.client.post('/deleteSection', {"Section": 1})

        response3 = self.client.get('/adminPage')

        sections = list(response3.context["sections"])

        if len(sections) == 0:
            self.assertTrue("Successful Deletion")
        else:
            self.assertFalse("Successful Deletion")
