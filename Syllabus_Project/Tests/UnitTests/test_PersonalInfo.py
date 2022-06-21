from django.test import TestCase
from Syllabus_Project.models import PersonalInfo
from Syllabus_Project.Validations import *
from django.core.exceptions import ValidationError

class TestPersonalInfo(TestCase):
    def setUp(self):
        self.validate = Validations()
        self.instructor = PersonalInfo.objects.create(myName="Instructor", officeLocation="EMS", officeNumber=659, phoneNumber="244-568-7934",
                                                      email="instructor@uwm.edu", day="Monday, Thursday", timeFrom='8:00 AM', timeTo='10:00 AM')
        self.TA = PersonalInfo.objects.create(myName="TA", officeLocation="EMS", officeNumber=218, phoneNumber="4148337064",
                                                      email="ta@uwm.edu", day="Monday, Wednesday", timeFrom='9:00 AM', timeTo='11:00 AM')

    #checking checkPersonalInfoPost method validates valid Personal Info object
    def test_validPersonalInfo(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             str(self.instructor.officeNumber), self.instructor.phoneNumber,
                                                             self.instructor.email), [])

    #test invalid name
    def test_invalid_name(self):
        self.assertEqual(self.validate.checkPersonalInfoPost("14567", self.instructor.officeLocation,
                                                             str(self.instructor.officeNumber), self.instructor.phoneNumber,
                                                             self.instructor.email), ["Name should not include numbers or any characters"])

    #test invalid officeLocation
    def test_invalid_officeLocation(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, "1345",
                                                             str(self.instructor.officeNumber), self.instructor.phoneNumber,
                                                             self.instructor.email), ["Office Location is invalid"])

    #test invalid office Number with characters
    def test_invalid_char_officeNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             "8G56A", self.instructor.phoneNumber,
                                                             self.instructor.email), ["Office Number should be an Integer and be between 3 to 5 numbers"])

    #test invalid office Number over 5 numbers
    def test_outOfBounds_officeNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             "3556789876", self.instructor.phoneNumber,
                                                             self.instructor.email), ["Office Number should be an Integer and be between 3 to 5 numbers"])

    # test invalid office Number under 3 numbers
    def test_underBounds_officeNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             "3", self.instructor.phoneNumber,
                                                             self.instructor.email), ["Office Number should be an Integer and be between 3 to 5 numbers"])

    # test negative office Number
    def test_neg_officeNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             "-345", self.instructor.phoneNumber,
                                                             self.instructor.email), ["Office Number must be a positive integer"])

    #test phoneNumber with character
    def test_invalid_char_phoneNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             str(self.instructor.officeNumber), "3G3-444-6789",
                                                             self.instructor.email), ["Invalid Phone Number"])

    # test phoneNumber with less digits
    def test_less_digits_phoneNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             str(self.instructor.officeNumber), "383444",
                                                             self.instructor.email), ["Invalid Phone Number"])

    #test negative phoneNumber
    def test_neg_phoneNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.instructor.myName, self.instructor.officeLocation,
                                                             str(self.instructor.officeNumber), "-383-444-6432",
                                                             self.instructor.email), ["Invalid Phone Number"])

    #test email without @ character
    def test_invalid_phoneNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.TA.myName, self.TA.officeLocation,
                                                             str(self.TA.officeNumber), self.TA.phoneNumber,
                                                             "adriangmail.com"), ["email is invalid"])

    #test email by beggining with @-. chars
    def test_invalidBeginning_phoneNumber(self):
        self.assertEqual(self.validate.checkPersonalInfoPost(self.TA.myName, self.TA.officeLocation,
                                                             str(self.TA.officeNumber), self.TA.phoneNumber,
                                                             "@.-prof.uwm.edu"), ["email is invalid"])

    # check whether models checks personalInfo name max_length
    def test_invalid_maxLength_Name(self):
        self.invalid_info_name = PersonalInfo.objects.create(myName= ("Prof"*50), officeLocation="EMS", officeNumber=659, phoneNumber="244-568-7934",
                                                      email="prof@uwm.edu", day="Monday, Thursday", timeFrom='8:00 AM', timeTo='10:00 AM')
        try:
            self.invalid_info_name.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks personalInfo office location max_length
    def test_invalid_maxLength_officeLocation(self):
        self.invalid_info_loc = PersonalInfo.objects.create(myName=self.TA.myName, officeLocation= ("EMS"*25), officeNumber=659,
                                                        phoneNumber="244-568-7934",
                                                        email="ta@uwm.edu", day="Monday, Wednesday",
                                                        timeFrom='8:00 AM', timeTo='10:00 AM')
        try:
            self.invalid_info_loc.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))


    # check whether models checks personalInfo phoneNumber max_length
    def test_invalid_maxLength_phoneNumber(self):
        self.invalid_info_pNum = PersonalInfo.objects.create(myName=self.TA.myName, officeLocation= self.TA.officeLocation, officeNumber=659,
                                                        phoneNumber=("244-568-7934" * 45),
                                                        email="ta@uwm.edu", day="Monday, Wednesday",
                                                        timeFrom='8:00 AM', timeTo='10:00 AM')
        try:
            self.invalid_info_pNum.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks personalInfo email max_length
    def test_invalid_maxLength_email(self):
        self.invalid_info_e = PersonalInfo.objects.create(myName=self.TA.myName,
                                                             officeLocation=self.TA.officeLocation, officeNumber=659,
                                                             phoneNumber=self.TA.phoneNumber,
                                                             email=("ta@uwm.edu"*40), day="Monday, Wednesday",
                                                             timeFrom='8:00 AM', timeTo='10:00 AM')
        try:
            self.invalid_info_e.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))


    # check whether models checks personalInfo day max_length
    def test_invalid_maxLength_day(self):
        self.invalid_info_d = PersonalInfo.objects.create(myName=self.TA.myName,
                                                             officeLocation=self.TA.officeLocation, officeNumber=659,
                                                             phoneNumber=self.TA.phoneNumber,
                                                             email=self.TA.email, day=("Monday, Wednesday"*65),
                                                             timeFrom='8:00 AM', timeTo='10:00 AM')
        try:
            self.invalid_info_d.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks invalid timeFrom
    def test_invalid_timeFrom(self):
        try:
            self.invalid_info_t = PersonalInfo.objects.create(myName=self.TA.myName,
                                                              officeLocation=self.TA.officeLocation, officeNumber=659,
                                                              phoneNumber=self.TA.phoneNumber,
                                                              email=self.TA.email, day="Monday",
                                                              timeFrom='8', timeTo='10:00 AM')
            self.invalid_info_t.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    # check whether models checks invalid timeTo
    def test_invalid_timeTo(self):
        try:
            self.invalid_info_t1 = PersonalInfo.objects.create(myName=self.TA.myName,
                                                              officeLocation=self.TA.officeLocation, officeNumber=659,
                                                              phoneNumber=self.TA.phoneNumber,
                                                              email=self.TA.email, day="Monday",
                                                              timeFrom='8:00 AM', timeTo='10.54')
            self.invalid_info_t1.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

# if __name__ == '__main__':
#     unittest.main()
