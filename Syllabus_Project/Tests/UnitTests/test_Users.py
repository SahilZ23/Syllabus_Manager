from django.test import TestCase
from Syllabus_Project.models import Users, PersonalInfo
from Syllabus_Project.Validations import *
from django.core.exceptions import ValidationError

class TestUsers(TestCase):
    def setUp(self):
        self.validate = Validations()
        self.compsci_1 = Courses.objects.create(courseName='Introduction to the calculator', courseNumber=150,
                                                semester='Spring', year=2021)
        self.instructor_info = PersonalInfo.objects.create(myName='Test Instructor', officeLocation='EMS FLOOR 5',
                                                                officeNumber=512, phoneNumber='414-555-5501',
                                                                email='csdept@example.com', day='Monday, Tuesday',
                                                                timeFrom='8:00 AM', timeTo='10:00 AM')
        self.instructor_user = Users.objects.create(role= "Instructor", user_username='prof01',
                                                    user_password='password', info=self.instructor_info)

    # checking checkAddUserPost method validates valid user
    def test_valid_user(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, self.instructor_user.user_username,
                                                        self.instructor_user.user_password, self.instructor_user.role), [])

    #test invalid user role
    def test_invalid_userRole(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, self.instructor_user.user_username,
                         self.instructor_user.user_password, "Tutor"), ["Role not a valid role"])

    # test invalid user role with addition to the specified role
    def test_invalid_userRole2(self):
        self.assertEqual(
            self.validate.checkAddUserPost(self.instructor_user.info.myName, self.instructor_user.user_username,
                                           self.instructor_user.user_password, "Math"+self.instructor_user.role), ["Role not a valid role"])

    #test invalid user full name with numbers
    def test_invalid_num_userFullName(self):
        self.assertEqual(self.validate.checkAddUserPost("35689", self.instructor_user.user_username,
                         self.instructor_user.user_password, self.instructor_user.role), ["Name cannot have numbers"])

    #test invalid user user_name with various chars
    def test_invalid_char_userName(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, "@@ja:}",
                         self.instructor_user.user_password, self.instructor_user.role), ["Username must be only letters or numbers or -._"])


    #test invalid user user_name with numbers at the beggining
    def test_invalid_num_userName(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, "1233ta",
                         self.instructor_user.user_password, self.instructor_user.role), ["Username must be only letters or numbers or -._"])

    # test invalid user user_name with numbers and chars
    def test_invalid_numChar_userName(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, "123#*@",
                                                        self.instructor_user.user_password,
                                                        self.instructor_user.role), ["Username must be only letters or numbers or -._"])


    #test if there is no password given by the user
    def test_invalid_password(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, self.instructor_user.user_username,
                                                        "", self.instructor_user.role), ["Password is required"])

    # test if there is weak password given by the user
    def test_weak_password(self):
        self.assertEqual(self.validate.checkAddUserPost(self.instructor_user.info.myName, self.instructor_user.user_username,
                                           "g", self.instructor_user.role), ["Password is weak"])

    # check whether models checks Users user_username maxlength
    def test_invalid_maxLength_userName(self):
        self.invalid_userName = Users.objects.create(role= "Instructor", user_username= ("willYu"*25),
                                                    user_password='password', info=self.instructor_info)
        try:
            self.invalid_userName.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks Users user_password maxlength
    def test_invalid_maxLength_userPassword(self):
        self.invalid_userPassword = Users.objects.create(role="Instructor", user_username=self.instructor_user.user_username,
                                                     user_password=('password'*50), info=self.instructor_info)
        try:
            self.invalid_userPassword.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks Users user_Role maxlength
    def test_invalid_maxLength_userRole(self):
        self.invalid_userRole = Users.objects.create(role=("Instructor"*30),
                                                         user_username=self.instructor_user.user_username,
                                                         user_password=self.instructor_user.user_password, info=self.instructor_info)
        try:
            self.invalid_userRole.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks Users foreign key (PersonalInfo) is assigned PersonalInfo object
    def test_invalid_UserForeignKey(self):
        try:
            self.invalid_userRole = Users.objects.create(role=self.instructor_user.role,
                                                         user_username=self.instructor_user.user_username,
                                                         user_password=self.instructor_user.user_password,
                                                         info=self.compsci_1)
            self.invalid_userRole.full_clean()
        except ValueError as exp:
            self.fail(print(exp))


# if __name__ == '__main__':
#     unittest.main()
