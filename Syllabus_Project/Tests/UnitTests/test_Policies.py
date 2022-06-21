from django.test import TestCase
from Syllabus_Project.models import Users, PersonalInfo, Courses, Section
from Syllabus_Project.Validations import *
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class TestPolicies(TestCase):
    def setUp(self):
        self.validate = Validations()
        self.compsci_1 = Courses.objects.create(courseName='Introduction to the calculator', courseNumber=150,
                                                semester='Spring', year=2021)
        self.compsci_2 = Courses.objects.create(courseName='Introduction to the calculator 2', courseNumber=151,
                                                semester='Spring', year=2021)
        self.instructor_info = PersonalInfo.objects.create(myName='Test Instructor', officeLocation='EMS FLOOR 5',
                                                           officeNumber=512, phoneNumber='414-555-5501',
                                                           email='csdept@example.com', day='Monday, Tuesday',
                                                           timeFrom='8:00 AM', timeTo='10:00 AM')
        self.instructor = Users.objects.create(role="Instructor", user_username='prof01',
                                                    user_password='password', info=self.instructor_info)
        self.policy = Policies.objects.create(policies="Late Policy: Hw should be turned before Midnight every Monday", policy_user=self.instructor,
                                              policy_course=self.compsci_1, policy_name="Late Policy")
        self.section1 = Section.objects.create(day="Thursday, Friday", timeFrom="2:00 PM", timeTo="3:45 PM", class_room="EMS 340", section_number=805,
                                               users=self.instructor, courses=self.compsci_1)

        self.instructor2_info = PersonalInfo.objects.create(myName='Instructor2', officeLocation='EMS FLOOR 8',
                                                           officeNumber=530, phoneNumber='432-550-5567',
                                                           email='inst2@example.com', day='Monday, Thursday',
                                                           timeFrom='8:00 AM', timeTo='10:00 AM')
        self.instructor2 = Users.objects.create(role="Instructor", user_username='prof02',
                                               user_password='password', info=self.instructor2_info)

    def test_valid_Policy(self):
        self.assertEqual(self.validate.userCanAddPolicy(self.instructor, self.compsci_1), True)

    def test_invalid_User_Policy(self):
        self.assertEqual(self.validate.userCanAddPolicy(self.instructor2, self.compsci_1), False)

    def test_add_policy_with_null_course(self):
        self.assertRaises(IntegrityError, Policies.objects.create, policies='policy text', policy_user=self.instructor, policy_course=None, policy_name='policy bad')

    def test_add_policy_bad_course(self):
        self.assertRaises(ValueError, Policies.objects.create, policies='policy text', policy_user=self.instructor,
                          policy_course=self.instructor2, policy_name='policy bad')

    def test_add_policy_with_null_user(self):
        self.assertRaises(IntegrityError, Policies.objects.create, policies='policy text', policy_user=None,
                          policy_course=self.compsci_1, policy_name='policy bad')

    def test_policy_delete_course_with_policy(self):
        course = Courses.objects.create(courseName='Introduction to the calculator 2', courseNumber=150,
                                                semester='Spring', year=2022)

        policy = Policies.objects.create(policies="Late Policy: Hw should be turned before Midnight every Monday", policy_user=self.instructor,
                                              policy_course=self.compsci_1, policy_name="Late Policy")

        course.delete()
        self.assertNotIn(policy, list(Policies.objects.all()))

    def test_add_policy_bad_user(self):
        self.assertRaises(ValueError, Policies.objects.create, policies='policy text', policy_user=self.section1,
                          policy_course=self.compsci_1, policy_name='policy bad')

# if __name__ == '__main__':
#     unittest.main()
