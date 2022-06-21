from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Courses, Users


class TestEditCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create(user_username='user', user_password='user@123', role='Instructor')
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")
        self.compsci= Courses.objects.create(courseName='CompSci', courseNumber=362, semester='Fall',
                                             year=2021)

    def test_edit_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add the same course with different name
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": 362, "semester": 'Fall',
                                                   "year": 2020, "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            self.assertEqual(i.courseName, "CS")
            self.assertEqual(i.courseNumber, 362)
            self.assertEqual(i.semester, "Fall")
            self.assertEqual(i.year, 2020)

    def test_edit_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add the same course with different name
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": 362, "semester": 'Spring',
                                                   "year": 2020, "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            self.assertEqual(i.semester, "Spring")

    def test_edit_3(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add the same course with different name
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": 362, "semester": 'Fall',
                                                   "year": 2021, "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            self.assertEqual(i.year, 2021)

