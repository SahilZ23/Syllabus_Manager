from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users, Courses, Policies, Section


class TestAddPolicy(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor = Users.objects.create(role="Instructor", user_username="jason", user_password="rock")
        self.course = Courses.objects.create(courseName="Math", courseNumber="231", semester="Fall", year="2020")
        self.section = Section.objects.create(day="Monday", timeFrom="10:00 AM", timeTo="11:00 AM", class_room="123",
                                              section_number=401, users=self.instructor, courses=self.course)

    def test_add_1(self):
        response = self.client.post('/', {'loginEmail': 'jason', 'loginPassword': 'rock'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/addPolicy', {"policyText": "Hello", "policyName": "Hey", "course": 1})

        self.policy = Policies.objects.all()

        for i in self.policy:
            self.assertEqual(i.policy_name, "Hey")
            self.assertEqual(i.policy_course, self.course)