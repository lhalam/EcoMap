"""Module which contains Test of Validator functions. """

import unittest2

import ecomap.validator

from ecomap.db import util as db

REGISTRATION_DATA = {'email': 'admin@gmail.com', 
                     'first_name': 'admin', 
                     'last_name': 'admin', 
                     'password': 'db51903d292a412e4ef2079add791eae', 
                     'pass_confirm': 'db51903d292a412e4ef2079add791eae'}

VALID_STATUS = {'status': True, 'error': []}

TEST_DATA = {'resource_name': '/res_name1', 'resource_id': '1234567'}

def get_resource_id_mock(resource_name):
    """Mock of resource_name_exists function"""
    return True

class TestUserRegistration(unittest2.TestCase):
    """ Class for test user_registration function"""

    def setUp(self):
        """ Setting up for the test """
        self.data = REGISTRATION_DATA
        self.valid_status = VALID_STATUS

    def tearDown(self):
        """Cleaning up after the test"""
        del self.data
        del self.valid_status

    def test_return_dictionary(self):
        """ testing if user_registration return a dictionary."""
        return_data = ecomap.validator.user_registration(self.data)
        self.assertIsInstance(return_data, dict)

    def test_return_correct_status(self):
        """testing status with correct user_registration."""
        return_data = ecomap.validator.user_registration(self.data)
        expected = self.valid_status
        self.assertTrue(return_data, expected)

    def test_has_key(self):
        """testing if data has all keys."""
        del self.data['first_name']
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'first_name': 'not contain first_name key.'}]}
        self.data['first_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_not_empty_data(self):
        """testing if value is not empty."""
        self.data['last_name'] = ""
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'last_name': 'last_name value is empty.'}]}
        self.data['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_check_maximum_length(self):
        """testing if value of data is not too long."""
        self.data['last_name'] = 'a'*260
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'last_name': 'last_name value is too long.'}]}
        self.data['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_check_minimum_length(self):
        """testing if value of data is not too short."""
        self.data['last_name'] = 'a'
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'last_name': 'last_name value is too short.'}]}
        self.data['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_check_string(self):
        """testing invalid type in data"""
        self.data['first_name'] = 125698
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'first_name': 'first_name value is not string.'}]}
        self.data['first_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_incorrect_email(self):
        """testing invalid email in data"""
        self.data['email'] = "admin@gmail"
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'email': 'email value does not look like email.'}]}
        self.data['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)

    def test_check_email_exist(self):
        """testing invalid email in data"""
        self.data['email'] = "admin.mail@gmail.com"
        return_data = ecomap.validator.user_registration(self.data)
        expected = {'status': False, 'error': [{'email': 'email allready exists.'}]}
        self.data['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)


class TestResourcePut(unittest2.TestCase):
    """ Class for test resource_put function"""

    def setUp(self):
        """ Setting up for the test """
        self.data = TEST_DATA
        self.valid_status = VALID_STATUS
        self.original_get_resource_id = db.get_resource_id
        db.get_resource_id = get_resource_id_mock


    def tearDown(self):
        """Cleaning up after the test"""
        del self.data, self.valid_status
        db.get_resource_id = self.original_get_resource_id

    def test_return_dictionary(self):
        """ testing if resource_put return a dictionary"""
        return_data = ecomap.validator.resource_put(self.data)
        self.assertIsInstance(return_data, dict)

    def test_return_correct_status(self):
        """testing status with correct resource_put"""
        return_data = ecomap.validator.resource_put(self.data)
        expected = self.valid_status
        self.assertTrue(return_data, expected)

    def test_not_empty_data(self):
        """testing invalid email in data"""
        test_data = {'resource_name': '', 'resource_id': ''}
        return_data = ecomap.validator.resource_put(test_data)
        expected = {'status': False, 'error': [{'resource_name': 'resource_name value is empty.'},\
                                                {'resource_id': 'resource_id value is empty.'}]}
        self.assertEqual(return_data, expected)

    def test_has_key(self):
        """testing if data has all keys."""
        del self.data['resource_id']
        db.get_resource_id = self.original_get_resource_id
        return_data = ecomap.validator.resource_put(self.data)
        expected = {'status': False, 'error': [{'resource_id': 'not contain resource_id key.'}]}
        self.data['resource_id'] = '12345'
        self.assertEqual(return_data, expected)

    def test_resouce_name_is_string(self):
        """testing if resouce_name is string."""
        self.assertIsInstance(self.data['resource_name'], basestring)

    def test_check_minimum_length(self):
        """testing if resouce_name is not too short."""
        self.data['resource_name'] = "a"
        return_data = ecomap.validator.resource_put(self.data)
        expected = {'status': False, 'error': [{'resource_name': \
                                                'resource_name value is too short.'}]}
        self.data['resource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_check_maximum_length(self):
        """testing if resouce_name is not too long."""
        self.data['resource_name'] = "a"*256
        return_data = ecomap.validator.resource_put(self.data)
        expected = {'status': False, 'error': [{'resource_name': \
                                                'resource_name value is too long.'}]}
        self.data['resource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

class TestPermissionPost(unittest2.TestCase):
    """ Class for test permission_put function"""
    def setUp(self):
        """ Setting up for the test """
        self.data = TEST_DATA
        self.valid_status = VALID_STATUS

    def tearDown(self):
        """Cleaning up after the test"""
        del self.data, self.valid_status

    def test_return_dictionary(self):
        """ testing if resource_put return a dictionary"""
        return_data = ecomap.validator.resource_put(self.data)
        self.assertIsInstance(return_data, dict)

    def test_return_correct_status(self):
        """testing status with correct resource_put"""
        return_data = ecomap.validator.resource_put(self.data)
        expected = self.valid_status
        self.assertTrue(return_data, expected) 

        
if __name__ == '__main__':
    unittest2.main()
