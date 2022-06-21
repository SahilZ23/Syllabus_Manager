from django.test import TestCase
from django.test import Client
from Syllabus_Project.models import Users, Courses, PersonalInfo, Section

class TestLogin(TestCase):
    #setting up a test database to run the following tests
    def setUp(self):
        self.client = Client()
        self.admin = Users.objects.create(role="Admin", user_username="admin", user_password="admin")

    # On an unsuccessful admin login the login page is redisplayed with an error message
    def test_admin_invalid_login(self):
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': '123admin'})
        self.assertEqual(response.context['message'], 'Invalid Username/Password')

    # if the admin logins correctly, they will be directed to adminPage
    def test_admin_login(self):
        print(self.admin.user_username)
        response = self.client.post('/', {'loginEmail': 'admin', 'loginPassword': 'admin'})
        # print(response.context)
        self.assertEqual(response.url, '/adminPage')
        response2 = self.client.get('/adminPage')
        users = list(response2.context['users'])

        print(users)
        for user in users:
            self.assertEqual(user.user_username, "admin")
            self.assertEqual(user.role, "Admin")


    def test_instrcutor_login(self):
        self.instructor = Users.objects.create(role="Instructor", user_username="jason", user_password="rock")
        self.course = Courses.objects.create(courseName="Math", courseNumber="231", semester="Fall", year="2020")
        self.section = Section.objects.create(day="Monday", timeFrom="10:00 AM", timeTo="11:00 AM", class_room="123",
                                              section_number= 401,users=self.instructor, courses=self.course)
        response = self.client.post('/', {'loginEmail': 'jason', 'loginPassword': 'rock'})
        self.assertEqual(response.url, '/userView')
        response2 = self.client.get('/userView')
        courses = list(response2.context['courses'])

        for i in courses:
            self.assertEqual(i.courses,self.course)

    def test_TA_login(self):
        self.ta = Users.objects.create(role="TA", user_username="njwicker", user_password="njwicker")
        self.course = Courses.objects.create(courseName="Math", courseNumber="231", semester="Fall", year="2020")
        self.section = Section.objects.create(day="Monday", timeFrom="10:00 AM", timeTo="11:00 AM", class_room="123",
                                              section_number=401, users=self.ta, courses=self.course)
        response = self.client.post('/', {'loginEmail': 'njwicker', 'loginPassword': 'njwicker'})
        self.assertEqual(response.url, '/TAView')
        response2 = self.client.get('/TAView')
        courses = list(response2.context['courses'])

        for i in courses:
            self.assertEqual(i.courses, self.course)

    def test_instrcutor_invalid_login(self):
        self.instructor = Users.objects.create(role="Instructor", user_username="jason", user_password="rock")
        response = self.client.post('/', {'loginEmail': 'jason', 'loginPassword': '123admin'})
        self.assertEqual(response.context['message'], 'Invalid Username/Password')

    def test_TA_invalid_login(self):
        self.ta = Users.objects.create(role="TA", user_username="njwicker", user_password="njwicker")
        response = self.client.post('/', {'loginEmail': 'njwicker', 'loginPassword': '123admin'})
        self.assertEqual(response.context['message'], 'Invalid Username/Password')