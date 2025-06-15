import os
import unittest
import shutil

def simple_addition(a, b):
    return a + b

ORIGINAL_FILE_PATH = "original_test_file_txt"
COPIED_FILE_PATH = "copied_test_file_txt"

COUNTER = 0

# This method will be run once before any tests or test classes
def setUpModule():
    global COUNTER
    COUNTER = 0

with open(ORIGINAL_FILE_PATH, "w") as file:
    file.write("Test Result:\n")

# This method will be run once after all tests and test classes
def tearDownModule():
    shutil.copy2(ORIGINAL_FILE_PATH, COPIED_FILE_PATH)
    os.remove(ORIGINAL_FILE_PATH)

class TestSimpleAddition(unittest.TestCase):
    def setUp(self):
        global COUNTER
        COUNTER += 1

    def tearDown(self):
        with open(ORIGINAL_FILE_PATH, "a") as file:
            result = "PASSED" if self._outcome.success else "FAILED"
            file.write(f"Test {COUNTER}: {result}\n")

    def test_add_positive_numbers(self):
        self.assertEqual(simple_addition(3, 4), 7)
        
    def test_add_negative_numbers(self):
        self.assertEqual(simple_addition(-3, -4), -7)

# Running the tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestSimpleAddition)
runner = unittest.TextTestRunner()
runner.run(suite)

# Read the copied file to show the results
with open(COPIED_FILE_PATH, 'r') as result_file:
	test_results = result_file.read()

print(test_results)


        
        
