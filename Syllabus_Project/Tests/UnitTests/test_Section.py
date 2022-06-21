from django.test import TestCase
from Syllabus_Project.models import Users, PersonalInfo, Courses, Section
from Syllabus_Project.Validations import *


class TestSection(TestCase):
    def setUp(self):
        self.validate = Validations()
        self.compsci_1 = Courses.objects.create(courseName='Introduction to the calculator', courseNumber=150,
                                                semester='Spring', year=2021)
        self.instructor_info = PersonalInfo.objects.create(myName='Test Instructor', officeLocation='EMS FLOOR 5',
                                                           officeNumber=512, phoneNumber='414-555-5501',
                                                           email='csdept@example.com', day='Monday, Tuesday',
                                                           timeFrom='8:00 AM', timeTo='10:00 AM')
        self.instructor = Users.objects.create(role="Instructor", user_username='prof01',
                                               user_password='password', info=self.instructor_info)
        self.section1 = Section.objects.create(day="Thursday, Friday", timeFrom="2:00 PM", timeTo="3:45 PM",
                                               class_room="EMS 340", section_number=805,
                                               users=self.instructor, courses=self.compsci_1)

    def test_assigned_Users_to_Sections(self):
        self.assertEqual(self.validate.checkSectionPost(self.compsci_1, self.instructor), "Professor already assigned to this course")

    def test_24_hour_time(self):
        self.assertIn(Section.objects.create(day="Thursday, Friday", timeFrom="14:00", timeTo="3:45 PM",
                                               class_room="EMS 340", section_number=807,
                                               users=self.instructor, courses=self.compsci_1), Section.objects.all())

    def test_24_hour_time_2(self):
        self.assertIn(Section.objects.create(day="Thursday, Friday", timeFrom="14:00", timeTo="15:45",
                                             class_room="EMS 340", section_number=808,
                                             users=self.instructor, courses=self.compsci_1), Section.objects.all())

    def test_24_hour_time_3(self):
        self.assertIn(Section.objects.create(day="Thursday, Friday", timeFrom="12:00 PM", timeTo="14:00",
                                             class_room="EMS 340", section_number=808,
                                             users=self.instructor, courses=self.compsci_1), Section.objects.all())

# if __name__ == '__main__':
#     unittest.main()
