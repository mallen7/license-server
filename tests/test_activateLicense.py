import unittest
from lambda_functions.activateLicense.activateLicense import activateLicense

class TestActivateLicense(unittest.TestCase):

    def test_valid_input(self):
        event = {'licenseKey': 'ABC123', 'productID': 1, 'userID': 1, 'deviceID': 'Device001'}
        response = activateLicense(event, None)
        self.assertEqual(response['statusCode'], 200)

    def test_invalid_input(self):
        event = {'licenseKey': '', 'productID': 0, 'userID': 0, 'deviceID': ''}
        response = activateLicense(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_activation_logic(self):
        event = {'licenseKey': 'XYZ789', 'productID': 2, 'userID': 2, 'deviceID': 'Device002'}
        response = activateLicense(event, None)
        # Assuming the license XYZ789 should be activated successfully
        self.assertIn('License Activated Successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
