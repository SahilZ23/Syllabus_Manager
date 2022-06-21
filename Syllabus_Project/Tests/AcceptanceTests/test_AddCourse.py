from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users


class TestAddCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create(user_username='user', user_password='user@123', role='Instructor')
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    def test_add_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # create a course
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

    def test_add_2(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # create a course with course number being an invalid type
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": "362", "semester": 'Fall',
                                                   "year": 2020, "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            if isinstance(i.courseNumber, str):
                self.assertFalse("Course Number cannot be a string")

    def test_add_3(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # create a course with year being an invalid type
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": 362, "semester": 'Fall',
                                                   "year": "2020", "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            if isinstance(i.year, str):
                self.assertFalse("year cannot be a string")

    def test_add_4(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # create a course with course number being an invalid type
        response = self.client.post('/addCourse', {"course": 200, "courseNumber": 362, "semester": 'Fall',
                                                   "year": 2020, "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            if isinstance(i.courseName, int):
                self.assertFalse("Course Name cannot be an Integer")

    def test_add_5(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # create a course with course number being an invalid type
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": 362, "semester": 150,
                                                   "year": 2020, "addUsers": '1'})
        # go to the admin page
        response2 = self.client.get('/adminPage')
        # get a list of courses
        course = list(response2.context['courses'])

        for i in course:
            if isinstance(i.semester, int):
                self.assertFalse("Semester cannot be an Integer")