import unittest
from lambda_functions.registerProduct.registerProduct import registerProduct

class TestRegisterProduct(unittest.TestCase):

    def test_valid_input(self):
        event = {'productName': 'NewProduct', 'description': 'New Product Description'}
        response = registerProduct(event, None)
        self.assertEqual(response['statusCode'], 201)

    def test_invalid_input(self):
        event = {'productName': '', 'description': ''}
        response = registerProduct(event, None)
        self.assertEqual(response['statusCode'], 400)

    def test_registration_logic(self):
        event = {'productName': 'AnotherProduct', 'description': 'Another Description'}
        response = registerProduct(event, None)
        # Assuming the product should be registered successfully
        self.assertIn('Product Registered Successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
