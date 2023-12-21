import unittest
from lambda_functions.validateLicense.validateLicense import validateLicense

class TestValidateLicense(unittest.TestCase):

    def test_valid_input(self):
        event = {'licenseKey': 'ABC123', 'productID': 1, 'deviceID': 'Device001'}
        response = validateLicense(event, None)
        self.assertEqual(response['statusCode'], 200)

    def test_invalid_input(self):
        event = {'licenseKey': '', 'productID': 0, 'deviceID': ''}
        response = validateLicense(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_validation_logic(self):
        event = {'licenseKey': 'XYZ789', 'productID': 2, 'deviceID': 'Device002'}
        response = validateLicense(event, None)
        # Assuming the license XYZ789 should be valid
        self.assertIn('License Validated Successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
