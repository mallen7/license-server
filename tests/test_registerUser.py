import unittest
from lambda_functions.registerUser.registerUser import registerUser

class TestRegisterUser(unittest.TestCase):

    def test_valid_input(self):
        event = {'name': 'NewUser', 'email': 'new.user@example.com', 'company': 'NewCompany'}
        response = registerUser(event, None)
        self.assertEqual(response['statusCode'], 201)

    def test_invalid_input(self):
        event = {'name': '', 'email': '', 'company': ''}
        response = registerUser(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_registration_logic(self):
        event = {'name': 'AnotherUser', 'email': 'another.user@example.com', 'company': 'AnotherCompany'}
        response = registerUser(event, None)
        # Assuming the user should be registered successfully
        self.assertIn('User Registered Successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
