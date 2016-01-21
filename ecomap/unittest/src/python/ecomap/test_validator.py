"""Module which contains Test of Validator functions. """

import unittest2
from ecomap import validator


# input data
REGISTRATION_DATA = {'email': 'admin@gmail.com',
                     'first_name': 'admin',
                     'last_name': 'admin',
                     'password': 'db51903d292a412e4ef2079add791eae',
                     'pass_confirm': 'db51903d292a412e4ef2079add791eae'}

LOGIN_DATA = {'email': 'admin@gmail.com',
              'password': 'db51903d292a412e4ef2079add791eae'}

VALID_STATUS = {'status': True, 'error': []}

TEST_DATA_PUT = {'resource_name': '/res_name1', 'resource_id': '1234567'}

TEST_DATA_PERMISSION_POST = {'resource_id': '1234567',
                             'action': 'PUT',
                             'modifier': 'Own',
                             'description': 'user'}

TEST_DATA_PERMISSION_PUT = {'permission_id': '1234567',
                            'action': 'PUT',
                            'modifier': 'Own',
                            'description': 'user'}

TEST_DATA_POST_COMMENT = {'content': 'comment', 'problem_id': 77}

TEST_DATA_RESOURCE_DELETE = {'resource_id': 1111}

TEST_DATA_USER_ROLE_PUT = {'role_id': 3, 'user_id': 4}

ROLES_DATA = {'user': (2L, ), 'admin': (1L, )}

RESOURCE_DATA = {'/api/roles': (18L,), '/api/login': (17L,)}

ROLE_PUT = {'role_name': "new_name", 'role_id': 5}

ROLE_PERMISSION_DATA = {'permission_id': 3, 'role_id': 1}

ROLE_PERMISSION_POST = {'permission_id': 5, 'role_id': 4}

PROBLEM_POST = {'title': 'problem with rivers',
                'content': 'some text',
                'latitude': '49.8256101',
                'longitude': '24.0600542',
                'type' : 2}

VALIDATOR_DATA_ROLE_AND_RESOURCE = {'resource_name': '/name',
                                    'role_id': 5,
                                    'user_id': 5}

EMAIL_DATA = {"admin.mail@gmail.com": (1L,
                                       u'admin',
                                       u'admin',
                                       u'admin.mail@gmail.com',
                                       u'db51903d292a412e4ef2079add791eae',
                                       None)}

HASH_DATA = 'f10551c61d8f9d264125e1314287933df10551c61d8f9d264125e1314287933d'

ROLE_POST_DATA = {'role_name':'user'}

PERMISSION_DELETE_DATA = {'permission_id': 5}

CHANGE_PASS_DATA = {'id':'6', 'old_pass':'oldpasswd', 'password':'newpasswd'}

ERROR_MSG = {'has_key': 'not contain %s key.',
             'check_minimum_length': '%s value is too short.',
             'check_maximum_length': '%s value is too long.',
             'check_string': '%s value is not string.',
             'check_email': '%s value does not look like email.',
             'check_empty': '%s value is empty.',
             'check_enum_value': 'invalid %s value.',
             'check_email_exist': 'email allready exists.',
             'name_exists': '"%s" name allready exists.',
             'check_coordinates': '%s is not coordinates.',
             'check_coordinates_length': '%s is out of range.'}


class DBUtilMock(object):

    """Class mock for db.util """

    def check_hash_in_db(self, data):
        """Mock for db.check_hash_in_db() function."""
        return True

    def check_hash_in_db_mock(self, data):
        """Mock for db.check_hash_in_db() function to return False."""
        return False

def resource_name_exists_mock(resource_name):
    """Mock of resource_name_exists function."""
    return RESOURCE_DATA.get(resource_name)

def check_email_exist_mock(email):
    """Mock of email_exists function."""
    return EMAIL_DATA.get(email)

def role_name_exists_mock(role_name):
    """Mock of role_name_exists function."""
    return ROLES_DATA.get(role_name)


class TestValidator(unittest2.TestCase):

    """Class for test validator.py."""

    def setUp(self):
        """Setting up for the test."""
<<<<<<< HEAD
=======

        self.data_registration = REGISTRATION_DATA
        self.data_check_post_comment = TEST_DATA_POST_COMMENT
        self.data_resource_put = TEST_DATA_PUT
        self.data_resource_delete = TEST_DATA_RESOURCE_DELETE
        self.data_permission_post = TEST_DATA_PERMISSION_POST
        self.data_permission_put = TEST_DATA_PERMISSION_PUT
        self.data_user_role_put = TEST_DATA_USER_ROLE_PUT
        self.data = VALIDATOR_DATA_ROLE_AND_RESOURCE
        self.data_login = LOGIN_DATA
        self.role_permission_post = ROLE_PERMISSION_POST
        self.problem_post = PROBLEM_POST
        self.role_put = ROLE_PUT

        self.valid_status = VALID_STATUS

>>>>>>> 61536d1a2aecfc40725878f0897359a94af170ce
        self.original_role_name_exists = validator.role_name_exists
        validator.role_name_exists = role_name_exists_mock
        self.original_resource_name_exists = validator.resource_name_exists
        validator.resource_name_exists = resource_name_exists_mock
        self.original_check_email_exist = validator.check_email_exist
        validator.check_email_exist = check_email_exist_mock


    def tearDown(self):
        """Cleaning up after the test."""
        validator.role_name_exists = self.original_role_name_exists
        validator.resource_name_exists = self.original_resource_name_exists
        validator.check_email_exist = self.original_check_email_exist


    # user_registration tests
    def test_registration_return_dictionary(self):
        """Testing if user_registration return
        a dictionary in user_registration function.
        """
        return_data = validator.user_registration(REGISTRATION_DATA)
        self.assertIsInstance(return_data, dict)

    def test_registration_correct_status(self):
        """Testing status with correct
        user_registration in user_registration function.
        """
        return_data = validator.user_registration(REGISTRATION_DATA)
        self.assertTrue(return_data, VALID_STATUS)

    def test_registration_has_key(self):
        """Testing if data has all keys
        in user_registration function.
        """
        del REGISTRATION_DATA['first_name']
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error':[{'first_name': 'not contain first_name key.'}]}
        REGISTRATION_DATA['first_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registration_not_empty_data(self):
        """Testing if value is not empty in
         user_registration function.
         """
        REGISTRATION_DATA['last_name'] = ''
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error':[{'last_name': 'last_name value is empty.'}]}
        REGISTRATION_DATA['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registration_maximum_length(self):
        """Testing if value of data is not too long
        in user_registration function.
        """
        REGISTRATION_DATA['last_name'] = 'a' * 260
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error': [{'last_name': 'last_name value is too long.'}]}
        REGISTRATION_DATA['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registration_minimum_length(self):
        """Testing if value of data is not too short
        in user_registration function.
        """
        REGISTRATION_DATA['last_name'] = 'a'
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error': [{'last_name': 'last_name value is too short.'}]}
        REGISTRATION_DATA['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registration_check_string(self):
        """Testing invalid type in data
        in user_registration function.
        """
        REGISTRATION_DATA['first_name'] = 125698
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error': [{'first_name': 'first_name value is not string.'}]}
        REGISTRATION_DATA['first_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registration_incorrect_email(self):
        """Testing invalid email in data
        in user_registration function.
        """
        REGISTRATION_DATA['email'] = "admin@gmail"
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error': [{'email': 'email value does not look like email.'}]}
        REGISTRATION_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)

    def test_registration_check_email_exist(self):
        """Testing if email exist in db
        in user_registration function.
        """
        REGISTRATION_DATA['email'] = 'admin.mail@gmail.com'
        return_data = validator.user_registration(REGISTRATION_DATA)
        expected = {'status': False,
                    'error': [{'email': 'email allready exists.'}]}
        REGISTRATION_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)


    # check_post_comment tests
    def test_post_comment_return_type(self):
        """Testing if check_post_comment returns
        a dictionary in check_post_comment function."""
        return_data = validator.check_post_comment(TEST_DATA_POST_COMMENT)
        self.assertIsInstance(return_data, dict)

    def test_post_comment_correct_status(self):
        """Check if status is correct."""
        expected = validator.check_post_comment(TEST_DATA_POST_COMMENT)
        self.assertDictEqual(expected, VALID_STATUS)

    def test_post_comment_has_key(self):
        """Testing if data has all keys
        in check_post_comment function.
        """
        invalid_data = {'content': 'comment'}
        actual = {'status': False,
                  'error': [{'problem_id': 'not contain problem_id key.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_not_empty_data(self):
        """Testing if return value is not empty in
         check_post_comment function.
         """
        invalid_data = {'content': 'comment', 'problem_id': None}
        actual = {'status': False,
                  'error': [{'problem_id': 'problem_id value is empty.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_check_string(self):
        """Testing invalid type in data
        in check_post_comment function.
        """
        invalid_data = {'content': [1, 2, 3], 'problem_id': 77}
        actual = {'status': False,
                  'error': [{'content': 'content value is not string.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_minimum_length(self):
        """Testing if content is not too short
        in check_post_comment function.
        """
        invalid_data = {'content': 'q', 'problem_id': 77}
        actual = {'status': False,
                  'error': [{'content': 'content value is too short.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_check_maximum_length(self):
        """Testing if content is not too long
        in check_post_comment function.
        """
        invalid_data = {'content': 'q' * 256, 'problem_id': 77}
        actual = {'status': False,
                  'error': [{'content': 'content value is too long.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)


    #hash_chek
    def test_hash_check_returned_type(self):
        """Test hash_check returned type of hash_check."""
        returned_data = validator.hash_check(HASH_DATA)
        self.assertIsInstance(returned_data, dict)

    def test_hash_check_dict_bad_hash(self):
        """Test hash_check dictionary when length of hash is bad."""
        bad_hash = HASH_DATA[:50]
        bad_hash_dict = validator.hash_check(bad_hash)
        correct_hash_dict = {'status': False,
                             'error': [{'hash_sum': 'hash sum has wrong length.'}]}
        self.assertDictEqual(bad_hash_dict, correct_hash_dict)

    def test_hash_check_wrong_hash_db(self):
        """Test hash_check dictionary when there is no such hash in db."""
        bad_hash_dict = validator.hash_check(HASH_DATA)
        correct_db_dict = {'status': False, 'error': [{'hash_sum': 'hash does not exist.'}]}
        self.assertDictEqual(bad_hash_dict, correct_db_dict)

    def test_hash_check_hash_in_db_ok(self):
        """Test hash_check if there is no error and hash is valid."""
        original_val_db = validator.db
        validator.db = DBUtilMock()
        returned_data = validator.hash_check(HASH_DATA)
        correct_db_dict = {'status': True, 'error': []}
        self.assertDictEqual(returned_data, correct_db_dict)
        validator.db = original_val_db


    #user_login
    def test_login_return_dictionary(self):
        """Testing user_login function whether it returns dictionary."""
        return_data = validator.user_login(LOGIN_DATA)
        self.assertIsInstance(return_data, dict)

    def test_login_correct_status(self):
        """Testing user_login function whether status is correct."""
        return_data = validator.user_login(LOGIN_DATA)
        self.assertTrue(return_data, VALID_STATUS)

    def test_login_has_key(self):
        """Testing user_login function if data has all keys."""
        del LOGIN_DATA['email']
        return_data = validator.user_login(LOGIN_DATA)
        expected = {'status': False,
                    'error': [{'email': 'not contain email key.'}]}
        LOGIN_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)

    def test_login_not_empty_data(self):
        """Testing user_login function if value is not empty."""
        LOGIN_DATA['password'] = ""
        return_data = validator.user_login(LOGIN_DATA)
        expected = {'status': False,
                    'error': [{'password': 'password value is empty.'}]}
        LOGIN_DATA['password'] = 'db51903d292a412e4ef2079add791eae'
        self.assertEqual(return_data, expected)

    def test_login_maximum_length(self):
        """Testing user_login function if value of data is not too long."""
        LOGIN_DATA['password'] = 'a' * 101
        return_data = validator.user_login(LOGIN_DATA)
        expected = {'status': False,
                    'error': [{'password': 'password value is too long.'}]}
        LOGIN_DATA['password'] = 'db51903d292a412e4ef2079add791eae'
        self.assertEqual(return_data, expected)

    def test_login_minimum_length(self):
        """Testing user_login function if value of data is not too short."""
        LOGIN_DATA['password'] = 'a'
        return_data = validator.user_login(LOGIN_DATA)
        expected = {'status': False,
                    'error': [{'password': 'password value is too short.'}]}
        LOGIN_DATA['password'] = 'db51903d292a412e4ef2079add791eae'
        self.assertEqual(return_data, expected)

    def test_login_check_string(self):
        """Testing user_login function if it is invalid type in data."""
        LOGIN_DATA['email'] = 125698
        return_data = validator.user_login(LOGIN_DATA)
        expected = {'status': False,
                    'error': [{'email': 'email value is not string.'}]}
        LOGIN_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)

    def test_login_incorrect_email(self):
        """Testing user_login function if email is correct in data."""
        LOGIN_DATA['email'] = "admin"
        return_data = validator.user_login(LOGIN_DATA)
        expected = {'status': False,
                    'error': [{'email': 'email value does not look like email.'}]}
        LOGIN_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)


    #resource_post
    def test_resource_post_return_dictionary(self):
        """Test if function returns dictionary."""
        return_data = validator.resource_post(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertIsInstance(return_data, dict)

    def test_resource_post_return_true(self):
        """Test if function returns true."""
        return_data = validator.resource_post(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertTrue(return_data['status'])

    def test_resource_post_has_key(self):
        """Test if function has errror has_key."""
        invalid_data = {'':'/res_name1'}
        return_data = validator.resource_post(invalid_data)
        expected_data = {'status': False,
                         'error':[{'resource_name': 'not contain resource_name key.'}]}
        self.assertEqual(return_data, expected_data)

    def test_resource_post_empty(self):
        """Test if function has errror error_empty."""
        invalid_data = {'resource_name': ''}
        return_data = validator.resource_post(invalid_data)
        expected_data = {'status': False,
                         'error':[{'resource_name': 'resource_name value is empty.'}]}
        self.assertEqual(return_data, expected_data)

    def test_resource_post_str(self):
        """Test if function has errror is_str."""
        invalid_data = {'resource_name': 1}
        return_data = validator.resource_post(invalid_data)
        expected_data = {'status': False,
                         'error':[{'resource_name': 'resource_name value is not string.'}]}
        self.assertEqual(return_data, expected_data)

    def test_resource_post_min_len(self):
        """Test if function has errror min_len."""
        invalid_data = {'resource_name': 'a'}
        return_data = validator.resource_post(invalid_data)
        expected_data = {'status': False,
                         'error':[{'resource_name': 'resource_name value is too short.'}]}
        self.assertEqual(return_data, expected_data)

    def test_resource_post_max_len(self):
        """Test if function has errror max_len."""
        invalid_data = {'resource_name': 'a' * 101}
        return_data = validator.resource_post(invalid_data)
        expected_data = {'status': False,
                         'error':[{'resource_name': 'resource_name value is too long.'}]}
        self.assertEqual(return_data, expected_data)


    # resource_put tests
    def test_res_put_return_dictionary(self):
        """Testing if resource_put return a dictionary in function."""
        return_data = validator.resource_put(TEST_DATA_PUT)
        self.assertIsInstance(return_data, dict)

    def test_res_put_correct_status(self):
        """Testing status with correct resource_putin resource_put dunction."""
        return_data = validator.resource_put(TEST_DATA_PUT)
        self.assertTrue(return_data, VALID_STATUS)

    def test_res_put_not_empty_data(self):
        """Testing invalid email in data in resource_put dunction."""
        test_data = {'resource_name': '', 'resource_id': ''}
        return_data = validator.resource_put(test_data)
        expected = {'status': False,
                    'error': [{'resource_name': 'resource_name value is empty.'},
                              {'resource_id': 'resource_id value is empty.'}]}
        self.assertEqual(return_data, expected)

    def test_res_put_has_key(self):
        """Testing if data has all keys in resource_put dunction."""
        del TEST_DATA_PUT['resource_id']
        return_data = validator.resource_put(TEST_DATA_PUT)
        expected = {'status': False,
                    'error': [{'resource_id': 'not contain resource_id key.'}]}
        TEST_DATA_PUT['resource_id'] = '12345'
        self.assertEqual(return_data, expected)

    def test_res_put_name_is_string(self):
        """Testing if resouce_name is string in resource_put dunction."""
        TEST_DATA_PUT['resource_name'] = 123
        return_data = validator.resource_put(TEST_DATA_PUT)
        expected = {'status': False,
                    'error': [{'resource_name': 'resource_name value is not string.'}]}
        TEST_DATA_PUT['rresource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_res_put_minimum_length(self):
        """Testing if resouce_name is not too short in resource_put dunction."""
        TEST_DATA_PUT['resource_name'] = "a"
        return_data = validator.resource_put(TEST_DATA_PUT)
        expected = {'status': False,
                    'error': [{'resource_name': 'resource_name value is too short.'}]}
        TEST_DATA_PUT['resource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_res_put_maximum_length(self):
        """Testing if resouce_name is not too long in resource_put dunction."""
        TEST_DATA_PUT['resource_name'] = "a"*256
        return_data = validator.resource_put(TEST_DATA_PUT)
        expected = {'status': False,
                    'error': [{'resource_name': 'resource_name value is too long.'}]}
        TEST_DATA_PUT['resource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_res_put_name_exist(self):
        """Testing if resouce_name is already exist in resource_put dunction."""
        TEST_DATA_PUT['resource_name'] = '/api/roles'
        return_data = validator.resource_put(TEST_DATA_PUT)
        expected = {'status': False,
                    'error': [{'resource_name': '"/api/roles" name allready exists.'}]}
        self.assertEqual(return_data, expected)


    # resource_delete tests
    def test_res_delete_return_type(self):
        """Testing if resource_delete returns
        a dictionary in resource_delete function."""
        return_data = validator.resource_delete(TEST_DATA_RESOURCE_DELETE)
        self.assertIsInstance(return_data, dict)

    def test_res_delete_correct_status(self):
        """Testing if status is correct."""
        expected = validator.resource_delete(TEST_DATA_RESOURCE_DELETE)
        self.assertDictEqual(expected, VALID_STATUS)

    def test_res_delete_not_empty_data(self):
        """Testing if return data is not empty
        in resource_delete function.
        """
        invalid_data = {'resource_id': None}
        actual = {'status': False,
                  'error': [{'resource_id': 'resource_id value is empty.'}]}
        self.assertDictEqual(validator.resource_delete(invalid_data), actual)

    def test_res_delete_has_key(self):
        """Testing if data has all keys
        in resource_delete function.
        """
        invalid_data = {'test': 1}
        actual = {'status': False,
                  'error': [{'resource_id': 'not contain resource_id key.'}]}
        self.assertDictEqual(validator.resource_delete(invalid_data), actual)


    #role_post
    def test_role_post_returned_type(self):
        """Test if function return dictionary."""
        returned_data = validator.role_post(ROLE_POST_DATA)
        self.assertIsInstance(returned_data, dict)

    def test_role_post_has_key(self):
        """Test if data has all keys."""
        post_data = {}
        returned_data = validator.role_post(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': 'not contain role_name key.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_role_post_empty_data(self):
        """Test if data isnt empty."""
        post_data = {'role_name':''}
        returned_data = validator.role_post(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': 'role_name value is empty.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_role_post_key_has_value(self):
        """Test if value of key isnt empty."""
        post_data = {'role_name':''}
        returned_data = validator.role_post(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': 'role_name value is empty.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_role_post_check_string(self):
        """Test if value is instance of string."""
        post_data = {'role_name':123123}
        returned_data = validator.role_post(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': 'role_name value is not string.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_role_post_minimum_length(self):
        """Test if value has minimum length."""
        post_data = {'role_name':'a'}
        returned_data = validator.role_post(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': 'role_name value is too short.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_role_post_maximum_length(self):
        """Test if value has maximim length."""
        post_data = {'role_name':'a'*256}
        returned_data = validator.role_post(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': 'role_name value is too long.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_role_post_role_name_exists(self):
        """Test if in database is role with such name."""
        returned_data = validator.role_post(ROLE_POST_DATA)
        correct_post_dict = {'status': False, 'error':
                             [{'role_name': '"user" name allready exists.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)


    #role_put
    def test_role_put_return_dictionary(self):
        """Testing role_put function whether it returns dictionary."""
        return_data = validator.role_put(ROLE_PUT)
        self.assertIsInstance(return_data, dict)

    def test_role_put_correct_status(self):
        """Testing user_login function whether status is correct."""
        return_data = validator.user_login(ROLE_PUT)
        self.assertTrue(return_data, VALID_STATUS)

    def test_role_put_has_key(self):
        """Testing role_put function if data has all keys."""
        del ROLE_PUT['role_name']
        return_data = validator.role_put(ROLE_PUT)
        expected = {'status': False,
                    'error': [{'role_name': 'not contain role_name key.'}]}
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, expected)

    def test_role_put_not_empty_data(self):
        """Testing role_put function if value is not empty."""
        ROLE_PUT['role_id'] = ""
        return_data = validator.role_put(ROLE_PUT)
        expected = {'status': False,
                    'error': [{'role_id': 'role_id value is empty.'}]}
        ROLE_PUT['role_id'] = 4
        self.assertEqual(return_data, expected)

    def test_role_put_maximum_length(self):
        """Testing role_put function if value of data is not too long."""
        ROLE_PUT['role_name'] = 'a' * 260
        return_data = validator.role_put(ROLE_PUT)
        expected = {'status': False,
                    'error': [{'role_name': 'role_name value is too long.'}]}
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, expected)

    def test_role_put_minimum_length(self):
        """Testing role_put function if value of data is not too short."""
        ROLE_PUT['role_name'] = 'a'
        return_data = validator.role_put(ROLE_PUT)
        expected = {'status': False,
                    'error': [{'role_name': 'role_name value is too short.'}]}
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, expected)

    def test_role_put_check_string(self):
        """Testing role_put function if it is invalid type in data."""
        ROLE_PUT['role_name'] = 125698
        return_data = validator.role_put(ROLE_PUT)
        expected = {'status': False,
                    'error': [{'role_name': 'role_name value is not string.'}]}
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, expected)

    def test_role_put_name_exists(self):
        """Testing role_put function if it is role with such name in db"""
        ROLE_PUT['role_name'] = 'user'
        return_data = validator.role_put(ROLE_PUT)
        expected = {'status': False,
                    'error': [{'role_name': '"user" name allready exists.'}]}
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, expected)


    #role_delete
    def test_role_del_retutn_dictionary(self):
        """Test if function returns deictionary."""
        return_data = validator.role_delete(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertIsInstance(return_data, dict)

    def test_role_del_return_true(self):
        """Test if function returns true."""
        return_data = validator.role_delete(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertTrue(return_data['status'])

    def test_role_del_has_key(self):
        """Test if function has errror has_key."""
        invalid_data = {'': 3}
        return_data = validator.role_delete(invalid_data)
        expected_data = {'status': False,
                         'error': [{'role_id': 'not contain role_id key.'}]}
        self.assertEqual(return_data, expected_data)

    def test_role_del_empty(self):
        """Test if function has errror error_empty."""
        invalid_data = {'role_id': ''}
        return_data = validator.role_delete(invalid_data)
        expected_data = {'status': False,
                         'error': [{'role_id': 'role_id value is empty.'}]}
        self.assertEqual(return_data, expected_data)


    # permission_post tests
    def test_perm_post_is_dictionary(self):
        """Testing if resource_put return
        a dictionary in permission_post function.
        """
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        self.assertIsInstance(return_data, dict)

    def test_perm_post_correct_status(self):
        """Testing status with correct
        resource_put in permission_post function.
        """
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        self.assertTrue(return_data, VALID_STATUS)

    def test_perm_post_has_key(self):
        """Testing if data has all keys
        in permission_post function.
        """
        del TEST_DATA_PERMISSION_POST['action']
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'action': 'not contain action key.'}]}
        TEST_DATA_PERMISSION_POST['action'] = 'PUT'
        self.assertEqual(return_data, expected)

    def test_perm_post_empty_data(self):
        """testing if data dont have empty value
        in permission_post function.
        """
        TEST_DATA_PERMISSION_POST['action'] = ''
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'action': 'action value is empty.'}]}
        TEST_DATA_PERMISSION_POST['action'] = 'PUT'
        self.assertEqual(return_data, expected)

    def test_perm_post_minimum_length(self):
        """testing if description is not too short
        in permission_post function.
        """
        TEST_DATA_PERMISSION_POST['description'] = 'a'
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'description': 'description value is too short.'}]}
        TEST_DATA_PERMISSION_POST['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_perm_post_maximum_length(self):
        """testing if description is not too long
        in permission_post function.
        """
        TEST_DATA_PERMISSION_POST['description'] = 'a' * 256
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'description': 'description value is too long.'}]}
        TEST_DATA_PERMISSION_POST['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_perm_post_is_string(self):
        """testing if description is string
        in permission_post function.
        """
        TEST_DATA_PERMISSION_POST['description'] = 123
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,\
                    'error': [{'description': 'description value is not string.'}]}
        TEST_DATA_PERMISSION_POST['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_permission_post_is_enum(self):
        """testing if modifier or action is ENUM
        in permission_post function.
        """
        TEST_DATA_PERMISSION_POST['modifier'] = 'user'
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,\
                    'error': [{'modifier': 'invalid modifier value.'}]}
        TEST_DATA_PERMISSION_POST['modifier'] = 'Own'
        self.assertEqual(return_data, expected)


    #permission_put tests
    def test_perm_put_is_dictionary(self):
        """ testing if resource_put return
        a dictionary in permission_put function."""
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        self.assertIsInstance(return_data, dict)

    def test_perm_put_correct_status(self):
        """testing status with correct
        resource_put in permission_put function."""
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        self.assertTrue(return_data, VALID_STATUS)

    def test_perm_put_has_key(self):
        """testing if data has all keys
        in permission_put function."""
        del TEST_DATA_PERMISSION_PUT['action']
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        expected = {'status': False,
                    'error': [{'action': 'not contain action key.'}]}
        TEST_DATA_PERMISSION_PUT['action'] = 'PUT'
        self.assertEqual(return_data, expected)

    def test_perm_put_empty_data(self):
        """testing if data dont have empty value
        in permission_put function.
        """
        TEST_DATA_PERMISSION_PUT['action'] = ''
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        expected = {'status': False,
                    'error': [{'action': 'action value is empty.'}]}
        TEST_DATA_PERMISSION_PUT['action'] = 'PUT'
        self.assertEqual(return_data, expected)

    def test_perm_put_minimum_length(self):
        """testing if description is not too short
        in permission_put function.
        """
        TEST_DATA_PERMISSION_PUT['description'] = 'a'
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        expected = {'status': False,
                    'error': [{'description': 'description value is too short.'}]}
        TEST_DATA_PERMISSION_PUT['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_perm_put_maximum_length(self):
        """testing if description is not too long
        in permission_put function.
        """
        TEST_DATA_PERMISSION_PUT['description'] = 'a' * 256
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        expected = {'status': False,
                    'error': [{'description': 'description value is too long.'}]}
        TEST_DATA_PERMISSION_PUT['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_perm_put_is_string(self):
        """testing if description is string
        in permission_put function.
        """
        TEST_DATA_PERMISSION_PUT['description'] = 123
        return_data = validator.permission_put(TEST_DATA_PERMISSION_PUT)
        expected = {'status': False,
                    'error': [{'description': 'description value is not string.'}]}
        TEST_DATA_PERMISSION_PUT['description'] = 'user'
        self.assertEqual(return_data, expected)

    # !!!!! 'check_enum_value': 'invalid %s value.' In str.434
    # we have ERROR_MSG['is_in_enum']. Not such value in ERROR_MSG
    def test_permission_put_is_enum(self):
        """testing if modifier or action is ENUM
        in permission_post function."""
        TEST_DATA_PERMISSION_POST['modifier'] = 'user'
        return_data = validator.permission_post(TEST_DATA_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'modifier': 'invalid modifier value.'}]}
        TEST_DATA_PERMISSION_POST['modifier'] = 'Own'
        self.assertEqual(return_data, expected)


    # permission_delete tests
    def test_permission_delete_returned_type(self):
        """Test if function return dictionary."""
        returned_data = validator.permission_delete\
                        (VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertIsInstance(returned_data, dict)

    def test_permission_delete_has_key(self):
        """Test if data has all keys."""
        permission_data = {}
        returned_data = validator.permission_delete(permission_data)
        correct_post_dict = {'status': False,
                             'error':[{'permission_id': 'not contain permission_id key.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_permission_delete_key_has_value(self):
        """Test if value of key isnt empty."""
        permission_data = {'permission_id':''}
        returned_data = validator.permission_delete(permission_data)
        correct_post_dict = {'status': False, 'error':
                             [{'permission_id':
                               'permission_id value is empty.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)


    # role_permission_post tests
    def test_role_permission_post_return_dictionary(self):
        """Testing role_permission_post function
        whether it returns dictionary."""
        return_data = validator.role_permission_post(ROLE_PERMISSION_POST)
        self.assertIsInstance(return_data, dict)

    def test_role_permission_post_correct_status(self):
        """testing role_permission_post function whether status is correct."""
        return_data = validator.role_permission_post(ROLE_PERMISSION_POST)
        self.assertTrue(return_data, VALID_STATUS)

    def test_role_permission_post_has_key(self):
        """testing role_permission_post function if data has all keys."""
        del ROLE_PERMISSION_POST['role_id']
        return_data = validator.role_permission_post(ROLE_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'role_id': 'not contain role_id key.'}]}
        ROLE_PERMISSION_POST['role_id'] = 4
        self.assertEqual(return_data, expected)

    def  test_role_permission_post_empty_dict(self):
        """ testing role_permission_post if data is not empty."""
        ROLE_PERMISSION_POST['role_id'] = None
        return_data = validator.role_permission_post(ROLE_PERMISSION_POST)
        expected = {'status': False,
                    'error': [{'role_id': 'role_id value is empty.'}]}
        self.assertDictEqual(return_data, expected)


    #role_permission_delete
    def test_permission_del_return_dictionary(self):
        """Test does function return dictionary."""
        return_data = validator.role_permission_delete(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertIsInstance(return_data, dict)

    def test_permission_del_return_true(self):
        """Testinf something."""
        return_data = validator.role_permission_delete(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertTrue(return_data['status'])

    def test_permission_del_has_key(self):
        """Test does function have errror has_key."""
        invalid_data = {'':3}
        return_data = validator.role_permission_delete(invalid_data)
        expected_data = {'status': False,
                         'error':[{'role_id': 'not contain role_id key.'}]}
        self.assertEqual(return_data, expected_data)

    def test_permission_del_empty(self):
        """Test does function have errror error_empty."""
        invalid_data = {'role_id': ''}
        return_data = validator.role_permission_delete(invalid_data)
        expected_data = {'status': False,
                         'error':[{'role_id': 'role_id value is empty.'}]}
        self.assertEqual(return_data, expected_data)


    # user_role_put tests
    def test_user_role_put_return_type(self):
        """Testing if user_role_put returns
        a dictionary in permission_post function.
        """
        return_data = validator.user_role_put(TEST_DATA_USER_ROLE_PUT)
        self.assertIsInstance(return_data, dict)

    def test_user_role_put_correct_status(self):
        """Testing if status is correct."""
        expected = validator.user_role_put(TEST_DATA_USER_ROLE_PUT)
        self.assertDictEqual(expected, VALID_STATUS)

    def  test_return_error_empty_dict(self):
        """Testing if return data is not empty
        in user_role_put function.
        """
        invalid_data = {'role_id': None, 'user_id': 2}
        actual = {'status': False,
                  'error': [{'role_id': 'role_id value is empty.'}]}
        self.assertDictEqual(validator.user_role_put(invalid_data), actual)

    def test_return_error_has_key(self):
        """Testing if return dictionary is correct."""
        invalid_data = {'test': 1, 'user_id': 3}
        actual = {'status': False,
                  'error': [{'role_id': 'not contain role_id key.'}]}
        self.assertDictEqual(validator.user_role_put(invalid_data), actual)


    # change_password tests
    def test_change_pass_returned_type(self):
        """Test if function return dictionary."""
        returned_data = validator.change_password\
                        (CHANGE_PASS_DATA)
        self.assertIsInstance(returned_data, dict)

    def test_change_pass_has_key(self):
        """Test if data has all keys."""
        permission_data = {}
        returned_data = validator.change_password(permission_data)
        correct_post_dict = {'status': False, 'error':
                             [{'password': 'not contain password key.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_change_pass_key_has_value(self):
        """Test if value of key isnt empty."""
        permission_data = {'password':''}
        returned_data = validator.change_password(permission_data)
        correct_post_dict = {'status': False, 'error':
                             [{'password': 'password value is empty.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_change_pass_check_string(self):
        """Test if value is instance of string."""
        post_data = {'password':1321521}
        returned_data = validator.change_password(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'password': 'password value is not string.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_change_pass_minimum_length(self):
        """Test if value has minimum length."""
        post_data = {'password':'1'}
        returned_data = validator.change_password(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'password': 'password value is too short.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)

    def test_change_pass_maximum_length(self):
        """Test if value has maximim length."""
        post_data = {'password':'1'*256}
        returned_data = validator.change_password(post_data)
        correct_post_dict = {'status': False, 'error':
                             [{'password': 'password value is too long.'}]}
        self.assertDictEqual(returned_data, correct_post_dict)


    # problem_post tests
    def test_problem_post_return_dictionary(self):
        """Testing problem_post function whether it returns dictionary."""
        return_data = validator.problem_post(PROBLEM_POST)
        self.assertIsInstance(return_data, dict)

    def test_problem_post_correct_status(self):
        """Testing problem_post function whether status is correct."""
        return_data = validator.problem_post(PROBLEM_POST)
        self.assertTrue(return_data, VALID_STATUS)

    def test_problem_post_has_key(self):
        """Testing problem_post function if data has all keys."""
        del PROBLEM_POST['title']
        return_data = validator.problem_post(PROBLEM_POST)
        expected = {'status': False,
                    'error': [{'title': 'not contain title key.'}]}
        PROBLEM_POST['title'] = 'title'
        self.assertEqual(return_data, expected)

    def  test_problem_post_empty_dict(self):
        """Testing problem_post if data is not empty."""
        PROBLEM_POST['title'] = None
        return_data = validator.problem_post(PROBLEM_POST)
        expected = {'status': False,
                    'error': [{'title': 'title value is empty.'}]}
        self.assertDictEqual(return_data, expected)

    def test_problem_post_check_string(self):
        """Testing problem_post function if it is invalid type in data."""
        PROBLEM_POST['content'] = 125698
        return_data = validator.problem_post(PROBLEM_POST)
        expected = {'status': False,
                    'error': [{'content': 'content value is not string.'}]}
        PROBLEM_POST['content'] = '49.8256101'
        self.assertEqual(return_data, expected)

    def test_problem_post_maximum_length(self):
        """Testing problem_post function if value of data is not too long."""
        PROBLEM_POST['title'] = 'a' * 260
        return_data = validator.problem_post(PROBLEM_POST)
        expected = {'status': False,
                    'error': [{'title': 'title value is too long.'}]}
        PROBLEM_POST['title'] = 'problem with rivers'
        self.assertEqual(return_data, expected)

    def test_problem_post_minimum_length(self):
        """Testing problem_post function if value of data is not too short."""
        PROBLEM_POST['title'] = 'a'
        return_data = validator.problem_post(PROBLEM_POST)
        expected = {'status': False,
                    'error': [{'title': 'title value is too short.'}]}
        PROBLEM_POST['title'] = 'problem with rivers'
        self.assertEqual(return_data, expected)


    # role_name_exists tests
    def test_role_name_exist_correct_data(self):
        """Testing with input data when role_name exists."""
        input_role_name = 'admin'
        return_data = validator.role_name_exists(input_role_name)
        self.assertTupleEqual(return_data, (1L,))

    def test_role_name_exist_incorrect_data(self):
        """Testing with input data when role_name doesn't exists."""
        input_role_name = 'test'
        self.assertEqual(validator.role_name_exists(input_role_name), None)


    #user_photo_deletion
    def test_user_photo_del_dictionary(self):
        """Test does function return dictionary."""
        return_data = validator.user_photo_deletion(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertIsInstance(return_data, dict)

    def test_user_photo_del_true(self):
        """Test does function return true."""
        return_data = validator.user_photo_deletion(VALIDATOR_DATA_ROLE_AND_RESOURCE)
        self.assertTrue(return_data['status'])

    def test_user_photo_del_has_key(self):
        """Test does function have errror has_key."""
        invalid_data = {'':'3'}
        return_data = validator.user_photo_deletion(invalid_data)
        expected_data = {'status': False,
                         'error':[{'user_id': 'not contain user_id key.'}]}
        self.assertEqual(return_data, expected_data)

    def test_user_photo_del_empty(self):
        """Test does function have errror error_empty."""
        invalid_data = {'user_id': ''}
        return_data = validator.user_photo_deletion(invalid_data)
        expected_data = {'status': False,
                         'error':[{'user_id': 'user_id value is empty.'}]}
        self.assertEqual(return_data, expected_data)


if __name__ == '__main__':
    unittest2.main()
