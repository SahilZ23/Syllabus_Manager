from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Courses, PersonalInfo, Users


class TestDeleteCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    def test_1(self):
        # login
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})

        # add a course
        response = self.client.post('/addCourse', {"course": 'CS', "courseNumber": 362, "semester": 'Fall',
                                                   "year": 2020, "section": 334, "addUsers": '1'})

        # delete the course
        response2 = self.client.post('/deleteCourse', {"Course": 1})

        # go to the admin page
        response3 = self.client.get('/adminPage')

        # get a list of courses
        course = list(response3.context['courses'])

        # since only one course was added and deleted the list should be empty
        if len(course) == 0:
            self.assertTrue("Successful Deletion")
        else:
            self.assertFalse("Successful Deletion")
