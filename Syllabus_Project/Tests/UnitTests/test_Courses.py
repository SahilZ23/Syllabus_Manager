from django.test import TestCase
from django.core.exceptions import ValidationError
from Syllabus_Project.models import Courses
from Syllabus_Project.Validations import *

class TestCourses(TestCase):
    def setUp(self):
        self.validator = Validations()
        self.course1 = Courses.objects.create(courseName= "Intro to Java", courseNumber=200, semester="Fall", year=2020)
        self.course2 = Courses.objects.create(courseName="System Programming", courseNumber=337, semester="Spring", year=2021)

    # check if the duplicate course method detects that our course exists already in the database
    def test_check_if_duplicate_course(self):
        self.assertEqual(self.validator.checkDuplicateCourse(
            self.course1.courseName,
            self.course1.courseNumber,
            self.course1.year,
            self.course1.semester), True)

    # check if the duplicate course method correctly returns False if a course does not exist already
    def test_check_new_course(self):
        self.assertEqual(self.validator.checkDuplicateCourse('Java Programming', 251, 2021, 'Spring'), False)

    # check that the duplicate course method considers courses different based on semester
    def test_check_duplicate_course_different_semester(self):
        self.assertEqual(self.validator.checkDuplicateCourse(
            self.course1.courseName,
            self.course1.courseNumber,
            self.course1.year,
            self.course1.semester + ' SPECIAL'), False)

    # check that the duplicate course method considers courses different based on year
    def test_check_duplicate_course_different_year(self):
        self.assertEqual(self.validator.checkDuplicateCourse(
            self.course1.courseName,
            self.course1.courseNumber,
            self.course1.year + 1,
            self.course1.semester), False)

    # check that the duplicate course method considers courses different based on name alone
    def test_check_duplicate_course_different_name(self):
        self.assertEqual(self.validator.checkDuplicateCourse(
            self.course1.courseName + ' Graduate Students Only',
            self.course1.courseNumber,
            self.course1.year,
            self.course1.semester), False)

    # check that the duplicate course method considers courses different based on course number alone
    def test_check_duplicate_course_different_number(self):
        self.assertEqual(self.validator.checkDuplicateCourse(
            self.course1.courseName,
            self.course1.courseNumber + 500,
            self.course1.year,
            self.course1.semester), False)

    # check whether long course names can be added
    def test_reallyLong_course_names_courseName(self):
        self.invalid_course = Courses.objects.create(courseName= ("Program" * 101),
                                                courseNumber=458, semester="fall", year=2020)
        try:
            self.invalid_course.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    def test_reallyLong_courseSem(self):
        self.invalid_course_sem = Courses.objects.create(courseName= self.course1.courseName ,
                                                courseNumber=458, semester= ("fall" * 45), year=2020)
        try:
            self.invalid_course_sem.full_clean()
        except ValidationError as exp:
            self.fail(print(exp))

    def test_check_course_post_valid(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        self.course2.semester), [])  # zero errors

    # check that a fully numeric course name does not validate
    def test_check_course_post_numeric_name(self):
        self.assertEqual(self.validator.checkCoursePost('23947239874',
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        self.course2.semester),
                                                        ["Course name should start as alphabetic"])  # specific error

    # check that a fully numeric course name does not validate
    def test_check_course_post_numeric_name_start(self):
        self.assertEqual(self.validator.checkCoursePost('2 Programming Courses',
                                                        str(self.course1.courseNumber),
                                                        str(self.course1.year),
                                                        self.course1.semester),
                                                        ["Course name should start as alphabetic"])  # specific errors

    # check that a course name with a digit after does validate
    def test_check_course_post_name_allow_digits(self):
        self.assertEqual(self.validator.checkCoursePost('Web Programming 2',
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        self.course2.semester), [])  # zero errors
    # check that a course name with underscores does validate
    def test_check_course_post_name_allow_underscores(self):
        self.assertEqual(self.validator.checkCoursePost('Web_Programming_Adv',
                                                        str(self.course1.courseNumber),
                                                        str(self.course1.year),
                                                        self.course1.semester), [])  # zero errors

    # check that a course name with underscores and digits does validate
    def test_check_course_post_name_allow_underscores_digits(self):
        self.assertEqual(self.validator.checkCoursePost('Web_Programming_200',
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        self.course2.semester), [])  # zero errors

     # check that a course name with hyphens does validate
    def test_check_course_post_name_allow_hyphens(self):
        self.assertEqual(self.validator.checkCoursePost('Web-Programming---',
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        self.course2.semester), [])  # zero errors

    # check that a course name with hyphens does validate
    def test_check_course_post_name_allow_hyphens_and_digits(self):
        self.assertEqual(self.validator.checkCoursePost('Web-Programming-200',
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        self.course2.semester), [])  # zero errors

    # check that a course semester must start alphabetical
    def test_check_course_post_semester_numeric(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        '20 FALL'), ["Course semester should start as alphabetic"])  # check error

    # check that a course semester cannot be all numbers
    def test_check_course_post_semester_all_numeric(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        '20213'),
                                                        ["Course semester should start as alphabetic"])  # check error

    # check that a course semester can have digits
    def test_check_course_post_semester_has_numeric(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        str(self.course2.year),
                                                        'FALL 21'), [])  # zero errors

    # check that a course number must be a number
    def test_check_course_post_course_number_is_number(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        '503G',
                                                        str(self.course2.year),
                                                        self.course2.semester),
                                                        ["Course number must be a positive integer"])  # check error

    # check that a course number must be an integer
    def test_check_course_post_course_number_is_integer(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        '503324.34',
                                                        str(self.course2.year),
                                                        self.course2.semester),
                                                        ["Course number must be a positive integer"])  # check error

     # check that a course number does not contain spaces
    def test_check_course_post_course_number_spaces(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        '503324 ',
                                                        str(self.course2.year),
                                                        self.course2.semester),
                                                        ["Course number must be a positive integer"])  # check error

     # check course number not zero
    def test_check_course_post_course_number_not_zero(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        '0',
                                                        str(self.course2.year),
                                                        self.course2.semester),
                                                        ["Course number must be a positive integer"])  # check error

     # check course number not negative
    def test_check_course_post_course_number_not_negative(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        '-251',
                                                        str(self.course2.year),
                                                        self.course2.semester),
                                                        ["Course number must be a positive integer"])  # check error

    # check that a course year must be a number
    def test_check_course_post_course_year_is_number(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        '2021G',
                                                        self.course2.semester),
                                                        ["Course year must be a positive integer"])  # check error

    # check that a course year must be an integer
    def test_check_course_post_course_year_is_integer(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        '2021.1',
                                                        self.course2.semester),
                                                        ["Course year must be a positive integer"])  # check error

    # check that a course year does not contain spaces
    def test_check_course_post_course_year_spaces(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        '2021 ',
                                                        self.course2.semester),
                                                        ["Course year must be a positive integer"])  # check error

    # check course year not zero
    def test_check_course_post_course_year_not_zero(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        '0',
                                                        self.course2.semester),
                                                        ["Course year must be a positive integer"])  # check error

    # check course year not negative
    def test_check_course_post_course_year_not_negative(self):
        self.assertEqual(self.validator.checkCoursePost(self.course2.courseName,
                                                        str(self.course2.courseNumber),
                                                        '-2021',
                                                        self.course2.semester),
                                                        ["Course year must be a positive integer"])  # check error

# if __name__ == '__main__':
#     unittest.main()
