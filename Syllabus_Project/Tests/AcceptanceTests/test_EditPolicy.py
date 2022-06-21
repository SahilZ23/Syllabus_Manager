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
        self.Policy = Policies.objects.create(policies="Hello", policy_user=self.instructor, policy_course=self.course,
                                              policy_name="Hey")
    # changing content
    def test_edit_1(self):
        response = self.client.post('/', {'loginEmail': 'jason', 'loginPassword': 'rock'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/addPolicy', {"policyText": "Bye", "policyName": "Hey", "course": 1})

        self.policy = Policies.objects.all()
        self.assertEqual(len(self.policy), 1)

        for i in self.policy:
            self.assertEqual(i.policies, "Bye")
            self.assertEqual(i.policy_course, self.course)

    # changing name
    def test_edit_2(self):
        response = self.client.post('/', {'loginEmail': 'jason', 'loginPassword': 'rock'})
        self.assertEqual(response.url, '/userView')

        response = self.client.post('/addPolicy', {"policyText": "Bye", "policyName": "Bye", "course": 1})

        self.policy = Policies.objects.all()

        self.assertEqual(len(self.policy), 1)

        for i in self.policy:
            self.assertEqual(i.policy_name, "Bye")
            self.assertEqual(i.policy_course, self.course)
