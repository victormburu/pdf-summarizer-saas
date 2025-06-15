import unittest

class Room:
    def __init__(self):
        self.register = []

    def add_student(self, student_name):
        self.register.append(student_name)

    def has_student(self, student_name):
        return student_name in self.register

class TestRoom(unittest.TestCase):
    def test_adding_student_to_room(self):
        room  =Room()
        new_student = "Victor mburu"

        room.add_student(new_student)

        self.assertTrue(room.has_student(new_student))

room_test_output =unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestRoom))
print(room_test_output)
