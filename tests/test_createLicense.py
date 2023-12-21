import unittest
from lambda_functions.createLicense.createLicense import createLicense

class TestCreateLicense(unittest.TestCase):

    def test_valid_input(self):
        event = {'productID': 1, 'userID': 1, 'expiryDate': '2025-12-31'}
        response = createLicense(event, None)
        self.assertEqual(response['statusCode'], 201)

    def test_invalid_input(self):
        event = {'productID': '', 'userID': '', 'expiryDate': ''}
        response = createLicense(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_creation_logic(self):
        event = {'productID': 2, 'userID': 2, 'expiryDate': '2026-12-31'}
        response = createLicense(event, None)
        # Assuming the license for product 2 and user 2 should be created successfully
        self.assertIn('License Created Successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
