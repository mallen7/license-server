import unittest
from lambda_functions.deactivateLicense.deactivateLicense import deactivateLicense

class TestDeactivateLicense(unittest.TestCase):

    def test_valid_input(self):
        event = {'licenseKey': 'ABC123', 'deviceID': 'Device001'}
        response = deactivateLicense(event, None)
        self.assertEqual(response['statusCode'], 200)

    def test_invalid_input(self):
        event = {'licenseKey': '', 'deviceID': ''}
        response = deactivateLicense(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_deactivation_logic(self):
        event = {'licenseKey': 'XYZ789', 'deviceID': 'Device002'}
        response = deactivateLicense(event, None)
        # Assuming the license XYZ789 should be deactivated successfully
        self.assertIn('License Deactivated Successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
