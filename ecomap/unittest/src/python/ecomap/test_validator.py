"""Module which contains Test of Validator functions. """

import unittest2
from ecomap import validator


REGISTRATION_DATA = {'email': 'admin@gmail.com',
                     'first_name': 'admin',
                     'last_name': 'admin',
                     'nickname': 'super_nick',
                     'password': 'db51903d292a412e4ef2079add791eae',
                     'pass_confirm': 'db51903d292a412e4ef2079add791eae'}

LOGIN_DATA = {'email': 'admin@gmail.com',
              'password': 'db51903d292a412e4ef2079add791eae'}

TEST_DATA = {'resource_name': '/res_name1',
             'resource_id': 1234567,
             'role_id': 5,
             'user_id': 5}

TEST_DATA_PUT = {'resource_name': '/res_name1',
                 'resource_id': 1234567}

TEST_DATA_PERMISSION = {'resource_id': 121,
                        'permission_id': 1234567,
                        'action': 'PUT',
                        'modifier': 'Own',
                        'description': 'user'}

TEST_DATA_POST_COMNT = {'content': 'comment',
                        'parent_id': "0",
                        'problem_id': 77}

ROLE_PERMISSION = {'role_id': 3,
                   'user_id': 4,
                   'permission_id': 3}

ROLES_DATA = {'user': (2L,),
              'admin': (1L,),
              'role_name': 'user'}

RESOURCE_DATA = {'/api/roles': (18L,),
                 '/api/login': (17L,)}

ROLE_PUT = {'role_name': 'new_name',
            'role_id': 5}

PROBLEM_POST = {'title': 'problem with rivers',
                'content': 'some text',
                'latitude': '49.8256101',
                'longitude': '24.0600542',
                'type': 2}

PROBLEM_PUT = {'problem_id': 2,
               'title': 'problem with rivers',
               'content': 'some text',
               'latitude': '49.8256101',
               'longitude': '24.0600542',
               'type': 2}

EMAIL_DATA = {'admin.mail@gmail.com': (1L,
                                       u'admin',
                                       u'admin',
                                       u'admin.mail@gmail.com',
                                       u'db51903d292a412e4ef2079add791eae',
                                       None)}

NICKNAME_DATA = {'admin': 'admin'}

PROBLEM_TYPE_DATA = {'problem_type_id': 3,
                     'problem_type_name': 'name',
                     'problem_type_radius': 10}

HASH_DATA = 'f10551c61d8f9d264125e1314287933df10551c61d8f9d264125e1314287933d'

HASH_DATA_DIC = {HASH_DATA: 1L}

CHANGE_PASS_DATA = {'id': 6,
                    'old_pass': 'oldpasswd',
                    'password': 'newpasswd'}

CHANGE_NICK_DATA = {'id': 5,
                    'nickname':'admin'}

VALID_STATUS = {'status': True,
                'error': []}

ERROR_DATA = {'status': False,
              'error': []}

ERROR_MSG = {'has_key': 'not contain %s key.',
             'check_minimum_length': '%s value is too short.',
             'check_maximum_length': '%s value is too long.',
             'check_string': '%s value is not string.',
             'check_email': '%s value does not look like email.',
             'check_empty': '%s value is empty.',
             'check_enum_value': 'invalid %s value.',
             'check_email_exist': 'email allready exists.',
             'check_nickname_exist': 'nickname already exists.',
             'name_exists': '"%s" name allready exists.',
             'check_coordinates': '%s is not coordinates.',
             'check_coordinates_length': '%s is out of range.',
             'check_hash_sum': '%s has wrong length.',
             'check_hash_db': '%s does not exist.'}

def check_hash_in_db_mock(data):
    """Mock for db.check_hash_in_db() function to return False."""
    return bool(HASH_DATA_DIC.get(data))

def resource_name_exists_mock(resource_name):
    """Mock of resource_name_exists function."""
    return bool(RESOURCE_DATA.get(resource_name))

def check_email_exist_mock(email):
    """Mock of email_exists function."""
    return bool(EMAIL_DATA.get(email))

def check_nickname_exist_mock(nickname):
    """Mock of check_nickname_exist function"""
    return bool(NICKNAME_DATA.get(nickname))

def role_name_exists_mock(role_name):
    """Mock of role_name_exists function."""
    return bool(ROLES_DATA.get(role_name))


class TestValidator(unittest2.TestCase):
    """Class for test validator.py."""
    def setUp(self):
        """Setting up for the test."""
        self.original_role_name_exists = validator.role_name_exists
        validator.role_name_exists = role_name_exists_mock
        self.original_resource_name_exists = validator.resource_name_exists
        validator.resource_name_exists = resource_name_exists_mock
        self.original_check_email_exist = validator.check_email_exist
        validator.check_email_exist = check_email_exist_mock
        self.orifinal_validator_db = validator.db.check_hash_in_db
        validator.db.check_hash_in_db = check_hash_in_db_mock
        self.original_check_nickname_exist = validator.check_nickname_exist
        validator.check_nickname_exist = check_nickname_exist_mock

    def tearDown(self):
        """Cleaning up after the test."""
        validator.role_name_exists = self.original_role_name_exists
        validator.resource_name_exists = self.original_resource_name_exists
        validator.check_email_exist = self.original_check_email_exist
        validator.db.check_hash_in_db = self.orifinal_validator_db
        validator.check_nickname_exist = self.original_check_nickname_exist

    def test_registr_return_dict(self):
        """Testing user_registration function if it returns dictionary."""
        self.assertIsInstance(validator.user_registration(REGISTRATION_DATA),
                              dict)

    def test_registr_correct_stat(self):
        """Testing user_registration function if status is correct."""
        self.assertDictEqual(validator.user_registration(REGISTRATION_DATA),
                             VALID_STATUS)

    def test_registr_has_key(self):
        """Testing user_registration function if data has all keys."""
        del REGISTRATION_DATA['first_name']
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'first_name': ERROR_MSG['has_key']
                                              %'first_name'}]
        REGISTRATION_DATA['first_name'] = 'admin'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_check_empty(self):
        """Testing user_registration function if value is not empty."""
        REGISTRATION_DATA['last_name'] = ''
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'last_name': ERROR_MSG['check_empty']
                                             %'last_name'}]
        REGISTRATION_DATA['last_name'] = 'admin'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_check_str(self):
        """Testing user_registration function if type is invalid."""
        REGISTRATION_DATA['first_name'] = 125698
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'first_name': ERROR_MSG['check_string']
                                              % 'first_name'}]
        REGISTRATION_DATA['first_name'] = 'admin'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_min_length(self):
        """Testing user_registration function if value is not too short."""
        REGISTRATION_DATA['last_name'] = 'a'
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'last_name': ERROR_MSG['check_minimum_length']
                                             % 'last_name'}]
        REGISTRATION_DATA['last_name'] = 'admin'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_max_length(self):
        """Testing user_registration function if value is not too long."""
        REGISTRATION_DATA['last_name'] = 'a' * 260
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'last_name': ERROR_MSG['check_maximum_length']
                                             % 'last_name'}]
        REGISTRATION_DATA['last_name'] = 'admin'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_incorrect_value(self):
        """Testing user_registration function if email is invalid."""
        REGISTRATION_DATA['email'] = "admin@gmail"
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'email': ERROR_MSG['check_email']
                                         % 'email'}]
        REGISTRATION_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_check_email_exist(self):
        """Testing user_registration function if email exists."""
        REGISTRATION_DATA['email'] = 'admin.mail@gmail.com'
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'email': ERROR_MSG['check_email_exist']}]
        REGISTRATION_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, ERROR_DATA)

    def test_registr_check_nickname_exist(self):
        """Testing user_registration function if nickname exists."""
        REGISTRATION_DATA['nickname'] = 'admin'
        return_data = validator.user_registration(REGISTRATION_DATA)
        ERROR_DATA['error'] = [{'nickname': ERROR_MSG['check_nickname_exist']}]
        REGISTRATION_DATA['nickname'] = 'super_nick'
        self.assertEqual(return_data, ERROR_DATA)

    def test_post_com_return_dict(self):
        """Testing check_post_comment function if it returns dictionary."""
        self.assertIsInstance(validator.check_post_comment(TEST_DATA_POST_COMNT),
                              dict)

    def test_post_com_correct_stat(self):
        """Testing check_post_comment function if status is correct."""
        self.assertDictEqual(validator.check_post_comment(TEST_DATA_POST_COMNT),
                             VALID_STATUS)

    def test_post_com_has_key(self):
        """Testing check_post_comment function if data has all keys."""
        invalid_data = {'content': 'comment', 'parent_id': 12}
        ERROR_DATA['error'] = [{'problem_id': ERROR_MSG['has_key']
                                              % 'problem_id'}]
        self.assertDictEqual(validator.check_post_comment(invalid_data),
                             ERROR_DATA)

    def test_post_com_check_empty(self):
        """Testing check_post_comment function if value is not empty."""
        invalid_data = {'content': 'comment',
                        'problem_id': None,
                        'parent_id': 12}
        ERROR_DATA['error'] = [{'problem_id': ERROR_MSG['check_empty']
                                              % 'problem_id'}]
        self.assertDictEqual(validator.check_post_comment(invalid_data),
                             ERROR_DATA)

    def test_post_com_check_str(self):
        """Testing check_post_comment function if type is invalid."""
        invalid_data = {'content': [1, 2, 3],
                        'problem_id': 77,
                        'parent_id': 12}
        ERROR_DATA['error'] = [{'content': ERROR_MSG['check_string']
                                           % 'content'}]
        self.assertDictEqual(validator.check_post_comment(invalid_data),
                             ERROR_DATA)


    def test_post_com_check_max_length(self):
        """Testing check_post_comment function if value is not too long."""
        invalid_data = {'content': 'q' * 256,
                        'problem_id': 77,
                        'parent_id': 12}
        ERROR_DATA['error'] = [{'content': ERROR_MSG['check_maximum_length']
                                           % 'content'}]
        self.assertDictEqual(validator.check_post_comment(invalid_data),
                             ERROR_DATA)

    def test_hash_check_return_dict(self):
        """Testing hash_check function if it returns dictionary."""
        self.assertIsInstance(validator.hash_check(HASH_DATA), dict)

    def test_hash_check_correct_stat(self):
        """Testing hash_check function if status is correct."""
        self.assertDictEqual(validator.hash_check(HASH_DATA), VALID_STATUS)

    def test_hash_check_hash_length(self):
        """Testing hash_check function if length is incorrect."""
        bad_hash = HASH_DATA[:50]
        ERROR_DATA['error'] = [{'hash_sum': ERROR_MSG['check_hash_sum']
                                            % 'hash sum'}]
        self.assertDictEqual(validator.hash_check(bad_hash), ERROR_DATA)

    def test_hash_check_not_exist(self):
        """Testing hash_check function if hash does not exist."""
        ERROR_DATA['error'] = [{'hash_sum': ERROR_MSG['check_hash_db']
                                            % 'hash'}]
        self.assertDictEqual(validator.hash_check('1' * 64), ERROR_DATA)

    def test_login_return_dict(self):
        """Testing user_login function if it returns dictionary."""
        self.assertIsInstance(validator.user_login(LOGIN_DATA), dict)

    def test_login_correct_stat(self):
        """Testing user_login function if is correct."""
        self.assertDictEqual(validator.user_login(LOGIN_DATA), VALID_STATUS)

    def test_login_has_key(self):
        """Testing user_login function if data has all keys."""
        del LOGIN_DATA['email']
        return_data = validator.user_login(LOGIN_DATA)
        ERROR_DATA['error'] = [{'email': ERROR_MSG['has_key']
                                         % 'email'}]
        LOGIN_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, ERROR_DATA)

    def test_login_check_empty(self):
        """Testing user_login function if value is not empty."""
        LOGIN_DATA['password'] = ""
        return_data = validator.user_login(LOGIN_DATA)
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_empty']
                                            % 'password'}]
        LOGIN_DATA['password'] = 'db51903d292a412e4ef2079add791eae'
        self.assertEqual(return_data, ERROR_DATA)

    def test_login_check_str(self):
        """Testing user_login function if type is invalid."""
        LOGIN_DATA['email'] = 125698
        return_data = validator.user_login(LOGIN_DATA)
        ERROR_DATA['error'] = [{'email': ERROR_MSG['check_string']
                                         % 'email'}]
        LOGIN_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, ERROR_DATA)

    def test_login_min_length(self):
        """Testing user_login function if value is not too short."""
        LOGIN_DATA['password'] = 'a'
        return_data = validator.user_login(LOGIN_DATA)
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_minimum_length']
                                            % 'password'}]
        LOGIN_DATA['password'] = 'db51903d292a412e4ef2079add791eae'
        self.assertEqual(return_data, ERROR_DATA)

    def test_login_max_length(self):
        """Testing user_login function if value is not too long."""
        LOGIN_DATA['password'] = 'a' * 101
        return_data = validator.user_login(LOGIN_DATA)
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_maximum_length']
                                            % 'password'}]
        LOGIN_DATA['password'] = 'db51903d292a412e4ef2079add791eae'
        self.assertEqual(return_data, ERROR_DATA)

    def test_login_incorrect_value(self):
        """Testing user_login function if email is invalid."""
        LOGIN_DATA['email'] = "admin"
        return_data = validator.user_login(LOGIN_DATA)
        ERROR_DATA['error'] = [{'email': ERROR_MSG['check_email'] % 'email'}]
        LOGIN_DATA['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, ERROR_DATA)

    def test_res_post_return_dict(self):
        """Testing resource_post function if it returns dictionary."""
        self.assertIsInstance(validator.resource_post(TEST_DATA), dict)

    def test_res_post_correct_stat(self):
        """Testing resource_post function if status is correct."""
        self.assertDictEqual(validator.resource_post(TEST_DATA_PUT),
                             VALID_STATUS)

    def test_res_post_has_key(self):
        """Testing resource_post function if data has all keys."""
        invalid_data = {'wrong_key': '/res_name1'}
        ERROR_DATA['error'] = [{'resource_name': ERROR_MSG['has_key']
                                                 % 'resource_name'}]
        self.assertEqual(validator.resource_post(invalid_data), ERROR_DATA)

    def test_res_post_check_empty(self):
        """Testing resource_post function if value is not empty."""
        invalid_data = {'resource_name': None}
        ERROR_DATA['error'] = [{'resource_name': ERROR_MSG['check_empty']
                                                 % 'resource_name'}]
        self.assertEqual(validator.resource_post(invalid_data), ERROR_DATA)

    def test_res_post_check_str(self):
        """Testing resource_post function if type is invalid."""
        invalid_data = {'resource_name': 1}
        ERROR_DATA['error'] = [{'resource_name': ERROR_MSG['check_string']
                                                 % 'resource_name'}]
        self.assertEqual(validator.resource_post(invalid_data), ERROR_DATA)

    def test_res_post_min_length(self):
        """Testing resource_post function if value is not too short."""
        invalid_data = {'resource_name': 'a'}
        error_msg = ERROR_MSG['check_minimum_length'] % 'resource_name'
        ERROR_DATA['error'] = [{'resource_name': error_msg}]
        self.assertEqual(validator.resource_post(invalid_data), ERROR_DATA)

    def test_res_post_max_length(self):
        """Testing resource_post function if value is not too long."""
        test_data = {'resource_name': 'a' * 101}
        error_msg = ERROR_MSG['check_maximum_length'] % 'resource_name'
        ERROR_DATA['error'] = [{'resource_name': error_msg}]
        self.assertEqual(validator.resource_post(test_data), ERROR_DATA)

    def test_res_put_return_dict(self):
        """Testing resource_put function if it returns dictionary."""
        self.assertIsInstance(validator.resource_put(TEST_DATA), dict)

    def test_res_put_correct_stat(self):
        """Testing resource_put function if status is correct."""
        self.assertDictEqual(validator.resource_put(TEST_DATA), VALID_STATUS)

    def test_res_put_has_key(self):
        """Testing resource_put function if data has all keys."""
        del TEST_DATA['resource_id']
        return_data = validator.resource_put(TEST_DATA)
        ERROR_DATA['error'] = [{'resource_id': ERROR_MSG['has_key']
                                               % 'resource_id'}]
        TEST_DATA['resource_id'] = 12345
        self.assertEqual(return_data, ERROR_DATA)

    def test_res_put_check_empty(self):
        """Testing resource_put function if value is not empty."""
        invalid_data = {'resource_name': 'resource', 'resource_id': None}
        ERROR_DATA['error'] = [{'resource_id': ERROR_MSG['check_empty']
                                               % 'resource_id'}]
        self.assertEqual(validator.resource_put(invalid_data), ERROR_DATA)

    def test_res_put_check_str(self):
        """Testing resouce_put function if value is not too short."""
        TEST_DATA['resource_name'] = 123
        return_data = validator.resource_put(TEST_DATA)
        ERROR_DATA['error'] = [{'resource_name': ERROR_MSG['check_string']
                                                 % 'resource_name'}]
        TEST_DATA['resource_name'] = '/res_name1'
        self.assertEqual(return_data, ERROR_DATA)

    def test_res_put_min_length(self):
        """Testing resource_put function if it is not too short in ."""
        TEST_DATA['resource_name'] = 'a'
        return_data = validator.resource_put(TEST_DATA)
        error_msg = ERROR_MSG['check_minimum_length'] % 'resource_name'
        ERROR_DATA['error'] = [{'resource_name': error_msg}]
        TEST_DATA['resource_name'] = '/res_name1'
        self.assertEqual(return_data, ERROR_DATA)

    def test_res_put_max_length(self):
        """Testing resource_put function if value is not too long."""
        TEST_DATA['resource_name'] = 'a' * 256
        return_data = validator.resource_put(TEST_DATA)
        error_msg = ERROR_MSG['check_maximum_length'] % 'resource_name'
        ERROR_DATA['error'] = [{'resource_name':error_msg}]
        TEST_DATA['resource_name'] = '/res_name1'
        self.assertEqual(return_data, ERROR_DATA)

    def test_res_put_name_exist(self):
        """Testing resource_put function if name already exists."""
        TEST_DATA['resource_name'] = '/api/roles'
        return_data = validator.resource_put(TEST_DATA)
        ERROR_DATA['error'] = [{'resource_name': ERROR_MSG['name_exists']
                                                 % TEST_DATA['resource_name']}]
        TEST_DATA['resource_name'] = '/res_name1'
        self.assertEqual(return_data, ERROR_DATA)

    def test_res_delete_return_dict(self):
        """Testing resource_delete function if it returns dictionary."""
        self.assertIsInstance(validator.resource_delete(TEST_DATA_PERMISSION),
                              dict)

    def test_res_delete_correct_stat(self):
        """Testing resource_delete function if status is correct."""
        self.assertDictEqual(validator.resource_delete(TEST_DATA_PERMISSION),
                             VALID_STATUS)

    def test_res_delete_has_key(self):
        """Testing resource_delete function if data has all keys."""
        invalid_data = {'test': 1}
        ERROR_DATA['error'] = [{'resource_id': ERROR_MSG['has_key']
                                               % 'resource_id'}]
        self.assertDictEqual(validator.resource_delete(invalid_data),
                             ERROR_DATA)

    def test_res_delete_check_empty(self):
        """Testing resource_delete function if value is not empty."""
        invalid_data = {'resource_id': None}
        ERROR_DATA['error'] = [{'resource_id': ERROR_MSG['check_empty']
                                               % 'resource_id'}]
        self.assertDictEqual(validator.resource_delete(invalid_data),
                             ERROR_DATA)

    def test_role_post_return_dict(self):
        """Testing role_post function if it returns dictionary."""
        self.assertIsInstance(validator.role_post(ROLES_DATA), dict)

    def test_role_post_has_key(self):
        """Testing role_post function if data has all keys."""
        post_data = {}
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['has_key']
                                             % 'role_name'}]
        self.assertDictEqual(validator.role_post(post_data), ERROR_DATA)

    def test_role_post_check_empty(self):
        """Testing role_post function if value is not empty."""
        invalid_data = {'role_name': ''}
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_empty']
                                             % 'role_name'}]
        self.assertDictEqual(validator.role_post(invalid_data), ERROR_DATA)

    def test_role_post_check_str(self):
        """Testing role_post function if type is invalid."""
        invalid_data = {'role_name': 123123}
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_string']
                                             % 'role_name'}]
        self.assertDictEqual(validator.role_post(invalid_data), ERROR_DATA)

    def test_role_post_min_length(self):
        """Testing role_post function if value is not too short."""
        post_data = {'role_name': 'a'}
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_minimum_length']
                                             % 'role_name'}]
        self.assertDictEqual(validator.role_post(post_data), ERROR_DATA)

    def test_role_post_max_length(self):
        """Testing role_post function if value is not too long."""
        post_data = {'role_name': 'a' * 256}
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_maximum_length']
                                             % 'role_name'}]
        self.assertDictEqual(validator.role_post(post_data), ERROR_DATA)

    def test_role_post_name_exists(self):
        """Testing role_post function if name already exists."""
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['name_exists'] % 'user'}]
        self.assertDictEqual(validator.role_post(ROLES_DATA), ERROR_DATA)

    def test_role_put_return_dict(self):
        """Testing role_put function if it returns dictionary."""
        self.assertIsInstance(validator.role_put(ROLE_PUT), dict)

    def test_role_put_correct_stat(self):
        """Testing user_login function if status is correct."""
        self.assertDictEqual(validator.role_put(ROLE_PUT), VALID_STATUS)

    def test_role_put_has_key(self):
        """Testing role_put function if data has all keys."""
        del ROLE_PUT['role_name']
        return_data = validator.role_put(ROLE_PUT)
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['has_key']
                                             % 'role_name'}]
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, ERROR_DATA)

    def test_role_put_check_empty(self):
        """Testing role_put function if value is not empty."""
        ROLE_PUT['role_id'] = ""
        return_data = validator.role_put(ROLE_PUT)
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['check_empty']
                                           % 'role_id'}]
        ROLE_PUT['role_id'] = 4
        self.assertEqual(return_data, ERROR_DATA)

    def test_role_put_check_str(self):
        """Testing role_put function if type is invalid."""
        ROLE_PUT['role_name'] = 125698
        return_data = validator.role_put(ROLE_PUT)
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_string']
                                             % 'role_name'}]
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, ERROR_DATA)

    def test_role_put_min_length(self):
        """Testing role_put function if value is not too short."""
        ROLE_PUT['role_name'] = 'a'
        return_data = validator.role_put(ROLE_PUT)
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_minimum_length']
                                             % 'role_name'}]
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, ERROR_DATA)

    def test_role_put_max_length(self):
        """Testing role_put function if value is not too long."""
        ROLE_PUT['role_name'] = 'a' * 260
        return_data = validator.role_put(ROLE_PUT)
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['check_maximum_length']
                                             % 'role_name'}]
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, ERROR_DATA)

    def test_role_put_name_exists(self):
        """Testing role_put function if name already exists"""
        ROLE_PUT['role_name'] = 'user'
        return_data = validator.role_put(ROLE_PUT)
        ERROR_DATA['error'] = [{'role_name': ERROR_MSG['name_exists'] % 'user'}]
        ROLE_PUT['role_name'] = 'new_name'
        self.assertEqual(return_data, ERROR_DATA)

    def test_role_del_return_dict(self):
        """Testing role_del function if it returns dictionary."""
        self.assertIsInstance(validator.role_delete(TEST_DATA), dict)

    def test_role_del_correct_stat(self):
        """Testing role_del function if status is correct."""
        self.assertDictEqual(validator.role_delete(TEST_DATA), VALID_STATUS)

    def test_role_del_has_key(self):
        """Testing role_del function if data has all keys."""
        invalid_data = {'wrong_key': 3}
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['has_key'] % 'role_id'}]
        self.assertEqual(validator.role_delete(invalid_data), ERROR_DATA)

    def test_role_del_check_empty(self):
        """Testing role_del function if value is not empty."""
        invalid_data = {'role_id': None}
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['check_empty']
                                           % 'role_id'}]
        self.assertEqual(validator.role_delete(invalid_data), ERROR_DATA)

    def test_perm_post_return_dict(self):
        """Testing permission_post function if it returns dictionary."""
        self.assertIsInstance(validator.permission_post(TEST_DATA_PERMISSION),
                              dict)

    def test_perm_post_correct_stat(self):
        """Testing permission_post function if status is correct."""
        self.assertDictEqual(validator.permission_post(TEST_DATA_PERMISSION),
                             VALID_STATUS)

    def test_perm_post_has_key(self):
        """Testing permission_post function if data has all keys."""
        del TEST_DATA_PERMISSION['action']
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'action': ERROR_MSG['has_key'] % 'action'}]
        TEST_DATA_PERMISSION['action'] = 'PUT'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_post_check_empty(self):
        """Testing permission_post function if value is not empty."""
        TEST_DATA_PERMISSION['action'] = ''
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'action': ERROR_MSG['check_empty'] % 'action'}]
        TEST_DATA_PERMISSION['action'] = 'PUT'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_post_check_enum(self):
        """Testing permission_post function if modifier or action is enum."""
        TEST_DATA_PERMISSION['modifier'] = 'user'
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'modifier': ERROR_MSG['check_enum_value']
                                            % 'modifier'}]
        TEST_DATA_PERMISSION['modifier'] = 'Own'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_post_check_str(self):
        """Testing permission_post function if type is invalid."""
        TEST_DATA_PERMISSION['description'] = 123
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'description': ERROR_MSG['check_string']
                                               % 'description'}]
        TEST_DATA_PERMISSION['description'] = 'user'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_post_min_length(self):
        """Testing permission_post function if value is not too short."""
        TEST_DATA_PERMISSION['description'] = 'a'
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'description': ERROR_MSG['check_minimum_length']
                                               % 'description'}]
        TEST_DATA_PERMISSION['description'] = 'user'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_post_max_length(self):
        """Testing permission_post function if value is not too long."""
        TEST_DATA_PERMISSION['description'] = 'a' * 256
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'description': ERROR_MSG['check_maximum_length']
                                               % 'description'}]
        TEST_DATA_PERMISSION['description'] = 'user'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_put_return_dict(self):
        """Testing permission_put function if it returns dictionary."""
        self.assertIsInstance(validator.permission_put(TEST_DATA_PERMISSION),
                              dict)

    def test_perm_put_correct_stat(self):
        """Testing permission_put function if status is correct."""
        self.assertDictEqual(validator.permission_put(TEST_DATA_PERMISSION),
                             VALID_STATUS)

    def test_perm_put_has_key(self):
        """Testing permission_put function if data has all keys."""
        del TEST_DATA_PERMISSION['action']
        return_data = validator.permission_put(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'action': ERROR_MSG['has_key'] % 'action'}]
        TEST_DATA_PERMISSION['action'] = 'PUT'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_put_check_empty(self):
        """Testing permission_put function if value is not empty."""
        TEST_DATA_PERMISSION['action'] = ''
        return_data = validator.permission_put(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'action': ERROR_MSG['check_empty'] % 'action'}]
        TEST_DATA_PERMISSION['action'] = 'PUT'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_put_check_enum(self):
        """Testing permission_post function if modifier or action is enum."""
        TEST_DATA_PERMISSION['modifier'] = 'user'
        return_data = validator.permission_post(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'modifier': ERROR_MSG['check_enum_value']
                                            % 'modifier'}]
        TEST_DATA_PERMISSION['modifier'] = 'Own'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_put_check_str(self):
        """Testing permission_put function if type is invalid."""
        TEST_DATA_PERMISSION['description'] = 123
        return_data = validator.permission_put(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'description': ERROR_MSG['check_string']
                                               % 'description'}]
        TEST_DATA_PERMISSION['description'] = 'user'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_put_min_length(self):
        """Testing permission_put function if value is not too short."""
        TEST_DATA_PERMISSION['description'] = 'a'
        return_data = validator.permission_put(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'description': ERROR_MSG['check_minimum_length']
                                               % 'description'}]
        TEST_DATA_PERMISSION['description'] = 'user'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_put_max_length(self):
        """Testing permission_put function if value is not too long."""
        TEST_DATA_PERMISSION['description'] = 'a' * 256
        return_data = validator.permission_put(TEST_DATA_PERMISSION)
        ERROR_DATA['error'] = [{'description': ERROR_MSG['check_maximum_length']
                                               % 'description'}]
        TEST_DATA_PERMISSION['description'] = 'user'
        self.assertEqual(return_data, ERROR_DATA)

    def test_perm_delete_return_dict(self):
        """Testing permission_delete function if it returns dictionary."""
        self.assertIsInstance(validator.permission_delete(TEST_DATA), dict)

    def test_perm_delete_has_key(self):
        """Testing permission_delete function if data has all keys."""
        permission_data = {}
        ERROR_DATA['error'] = [{'permission_id': ERROR_MSG['has_key']
                                                 % 'permission_id'}]
        self.assertDictEqual(validator.permission_delete(permission_data),
                             ERROR_DATA)

    def test_perm_delete_check_empty(self):
        """Testing permission_delete function if value is not empty."""
        invalid_data = {'permission_id': ''}
        ERROR_DATA['error'] = [{'permission_id': ERROR_MSG['check_empty']
                                                 % 'permission_id'}]
        self.assertDictEqual(validator.permission_delete(invalid_data),
                             ERROR_DATA)

    def test_role_perm_post_return_dict(self):
        """Testing role_permission_post function if it returns dictionary."""
        self.assertIsInstance(validator.role_permission_post(ROLE_PERMISSION),
                              dict)

    def test_role_perm_post_correct(self):
        """Testing role_permission_post function if status is correct."""
        self.assertDictEqual(validator.role_permission_post(ROLE_PERMISSION),
                             VALID_STATUS)

    def test_role_perm_post_has_key(self):
        """Testing role_permission_post function if data has all keys."""
        del ROLE_PERMISSION['role_id']
        return_data = validator.role_permission_post(ROLE_PERMISSION)
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['has_key'] % 'role_id'}]
        ROLE_PERMISSION['role_id'] = 4
        self.assertEqual(return_data, ERROR_DATA)

    def  test_role_perm_post_check_empty(self):
        """Testing role_permission_post if value is not empty."""
        ROLE_PERMISSION['role_id'] = None
        return_data = validator.role_permission_post(ROLE_PERMISSION)
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['check_empty']
                                           % 'role_id'}]
        ROLE_PERMISSION['role_id'] = 3
        self.assertDictEqual(return_data, ERROR_DATA)

    def test_perm_del_return_dict(self):
        """Testing permission_delete if it returns dictionary."""
        self.assertIsInstance(validator.role_permission_delete(TEST_DATA), dict)

    def test_perm_del_correct_stat(self):
        """Testing permission_delete function if status is correct."""
        self.assertDictEqual(validator.role_permission_delete(TEST_DATA),
                             VALID_STATUS)

    def test_perm_del_has_key(self):
        """Testing permission_delete function if data has all keys."""
        invalid_data = {'wrong_key':3}
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['has_key'] % 'role_id'}]
        self.assertEqual(validator.role_permission_delete(invalid_data),
                         ERROR_DATA)

    def test_perm_del_check_empty(self):
        """Testing permission_delete function if value is not empty."""
        invalid_data = {'role_id': None}
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['check_empty'] % 'role_id'}]
        self.assertEqual(validator.role_permission_delete(invalid_data),
                         ERROR_DATA)

    def test_user_role_put_return_dict(self):
        """Testing user_role_put function if it returns dictionary."""
        self.assertIsInstance(validator.user_role_put(ROLE_PERMISSION), dict)

    def test_user_role_put_correct_stat(self):
        """Testing user_role_put function if status is correct."""
        self.assertDictEqual(validator.user_role_put(ROLE_PERMISSION),
                             VALID_STATUS)

    def test_return_error_has_key(self):
        """Testing user_role_put function if data has all keys."""
        invalid_data = {'test': 1, 'user_id': 3}
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['has_key'] % 'role_id'}]
        self.assertDictEqual(validator.user_role_put(invalid_data), ERROR_DATA)

    def  test_user_role_put_check_empty(self):
        """Testing user_role_put function if value is not empty."""
        invalid_data = {'role_id': None, 'user_id': 2}
        ERROR_DATA['error'] = [{'role_id': ERROR_MSG['check_empty'] % 'role_id'}]
        self.assertDictEqual(validator.user_role_put(invalid_data), ERROR_DATA)

    def test_change_pass_return_dict(self):
        """Testing change_password function if it returns dictionary."""
        self.assertIsInstance(validator.change_password(CHANGE_PASS_DATA), dict)

    def test_change_pass_has_key(self):
        """Testing change_password function if data has all keys."""
        permission_data = {}
        ERROR_DATA['error'] = [{'password': ERROR_MSG['has_key'] % 'password'}]
        self.assertDictEqual(validator.change_password(permission_data),
                             ERROR_DATA)

    def test_change_pass_check_empty(self):
        """Testing change_password function if value is not empty."""
        invalid_data = {'password': ''}
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_empty']
                                            % 'password'}]
        self.assertDictEqual(validator.change_password(invalid_data),
                             ERROR_DATA)

    def test_change_pass_check_str(self):
        """Testing change_password function if type is invalid."""
        invalid_data = {'password': 1321521}
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_string']
                                            % 'password'}]
        self.assertDictEqual(validator.change_password(invalid_data),
                             ERROR_DATA)

    def test_change_pass_min_length(self):
        """Testing change_password function if value is not too short."""
        post_data = {'password': '1'}
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_minimum_length']
                                            % 'password'}]
        self.assertDictEqual(validator.change_password(post_data), ERROR_DATA)

    def test_change_pass_max_length(self):
        """Testing change_password function if value is not too long."""
        post_data = {'password': '1' * 256}
        ERROR_DATA['error'] = [{'password': ERROR_MSG['check_maximum_length']
                                            % 'password'}]
        self.assertDictEqual(validator.change_password(post_data), ERROR_DATA)

    def test_change_nick_return_dict(self):
        """Testing change_nickname function if it returns dictionary."""
        self.assertIsInstance(validator.change_nickname(CHANGE_NICK_DATA), dict)

    def test_change_nick_has_key(self):
        """Testing change_nickname function if data has all keys."""
        permission_data = {}
        ERROR_DATA['error'] = [{'nickname': ERROR_MSG['has_key'] % 'nickname'}]
        self.assertDictEqual(validator.change_nickname(permission_data),
                             ERROR_DATA)

    def test_change_nick_check_empty(self):
        """Testing change_nickname function if value is not empty."""
        invalid_data = {'nickname': ''}
        ERROR_DATA['error'] = [{'nickname': ERROR_MSG['check_empty']
                                            % 'nickname'}]
        self.assertDictEqual(validator.change_nickname(invalid_data),
                             ERROR_DATA)

    def test_change_nick_check_str(self):
        """Testing change_nickname function if type is invalid."""
        invalid_data = {'nickname': 1321521}
        ERROR_DATA['error'] = [{'nickname': ERROR_MSG['check_string']
                                            % 'nickname'}]
        self.assertDictEqual(validator.change_nickname(invalid_data),
                             ERROR_DATA)

    def test_change_nick_max_length(self):
        """Testing change_nickname function if value is not too long."""
        post_data = {'nickname': '1' * 256}
        ERROR_DATA['error'] = [{'nickname': ERROR_MSG['check_maximum_length']
                                            % 'nickname'}]
        self.assertDictEqual(validator.change_nickname(post_data), ERROR_DATA)

    def test_change_nick_nickname_exist(self):
        """Testing change_nickname function if nickname exists."""
        return_data = validator.change_nickname(CHANGE_NICK_DATA)
        ERROR_DATA['error'] = [{'nickname': ERROR_MSG['check_nickname_exist']}]
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_post_return_dict(self):
        """Testing problem_post function if it returns dictionary."""
        self.assertIsInstance(validator.problem_post(PROBLEM_POST), dict)

    def test_probl_post_correct_stat(self):
        """Testing problem_post function if status is correct."""
        self.assertDictEqual(validator.problem_post(PROBLEM_POST), VALID_STATUS)

    def test_probl_post_has_key(self):
        """Testing problem_post function if data has all keys."""
        del PROBLEM_POST['title']
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['has_key'] % 'title'}]
        PROBLEM_POST['title'] = 'title'
        self.assertEqual(return_data, ERROR_DATA)

    def  test_probl_check_empty(self):
        """Testing problem_post function if value is not empty."""
        PROBLEM_POST['title'] = None
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['check_empty'] % 'title'}]
        PROBLEM_POST['title'] = 'problem with rivers'
        self.assertDictEqual(return_data, ERROR_DATA)

    def test_probl_post_check_str(self):
        """Testing problem_post function if type is invalid."""
        PROBLEM_POST['content'] = 125698
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [{'content': ERROR_MSG['check_string']
                                           % 'content'}]
        PROBLEM_POST['content'] = 'some text'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_post_min_length(self):
        """Testing problem_post function if value is not too short."""
        PROBLEM_POST['title'] = 'a'
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['check_minimum_length']
                                         % 'title'}]
        PROBLEM_POST['title'] = 'problem with rivers'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_post_max_length(self):
        """Testing problem_post function if value is not too long."""
        PROBLEM_POST['title'] = 'a' * 260
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['check_maximum_length']
                                         % 'title'}]
        PROBLEM_POST['title'] = 'problem with rivers'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_post_check_coord(self):
        """Testing problem_post function if values are coordinates"""
        PROBLEM_POST['latitude'] = '49'
        PROBLEM_POST['longitude'] = '24'
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [
            {'latitude': ERROR_MSG['check_coordinates'] % '49'},
            {'longitude': ERROR_MSG['check_coordinates'] % '24'}
        ]
        PROBLEM_POST['latitude'] = '49.08256101'
        PROBLEM_POST['longitude'] = '24.0600542'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_post_crd_length(self):
        """Testing problem_post function if coordinates are not too long"""
        PROBLEM_POST['latitude'] = '91.1'
        PROBLEM_POST['longitude'] = '181.1'
        return_data = validator.problem_post(PROBLEM_POST)
        ERROR_DATA['error'] = [
            {'latitude': ERROR_MSG['check_coordinates_length'] % '91.1'},
            {'longitude': ERROR_MSG['check_coordinates_length'] % '181.1'}
        ]
        PROBLEM_POST['latitude'] = '49.08256101'
        PROBLEM_POST['longitude'] = '24.0600542'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_put_return_dict(self):
        """Testing problem_post function if it returns dictionary."""
        self.assertIsInstance(validator.problem_put(PROBLEM_PUT), dict)

    def test_probl_put_correct_stat(self):
        """Testing problem_post function if status is correct."""
        self.assertDictEqual(validator.problem_put(PROBLEM_PUT), VALID_STATUS)

    def test_probl_put_has_key(self):
        """Testing problem_post function if data has all keys."""
        del PROBLEM_PUT['title']
        return_data = validator.problem_put(PROBLEM_PUT)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['has_key'] % 'title'}]
        PROBLEM_PUT['title'] = 'title'
        self.assertEqual(return_data, ERROR_DATA)

    def  test_probl_put_check_empty(self):
        """Testing problem_post function if value is not empty."""
        PROBLEM_PUT['title'] = None
        return_data = validator.problem_put(PROBLEM_PUT)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['check_empty'] % 'title'}]
        PROBLEM_PUT['title'] = 'problem with rivers'
        self.assertDictEqual(return_data, ERROR_DATA)

    def test_probl_put_check_str(self):
        """Testing problem_post function if type is invalid."""
        PROBLEM_PUT['content'] = 125698
        return_data = validator.problem_put(PROBLEM_PUT)
        ERROR_DATA['error'] = [{'content': ERROR_MSG['check_string']
                                           % 'content'}]
        PROBLEM_PUT['content'] = 'some text'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_put_min_length(self):
        """Testing problem_post function if value is not too short."""
        PROBLEM_PUT['title'] = 'a'
        return_data = validator.problem_put(PROBLEM_PUT)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['check_minimum_length']
                                         % 'title'}]
        PROBLEM_PUT['title'] = 'problem with rivers'
        self.assertEqual(return_data, ERROR_DATA)

    def test_probl_put_max_length(self):
        """Testing problem_post function if value is not too long."""
        PROBLEM_PUT['title'] = 'a' * 260
        return_data = validator.problem_put(PROBLEM_PUT)
        ERROR_DATA['error'] = [{'title': ERROR_MSG['check_maximum_length']
                                         % 'title'}]
        PROBLEM_PUT['title'] = 'problem with rivers'
        self.assertEqual(return_data, ERROR_DATA)

    def test_prob_del_return_dict(self):
        """Testing problem_type if it returns dictionary."""
        problem_data = {'problem_id': 2}
        self.assertIsInstance(validator.problem_delete(problem_data),
                              dict)

    def test_prob_del_correct_stat(self):
        """Testing problem_type function if status is correct."""
        problem_data = {'problem_id': 2}
        self.assertDictEqual(validator.problem_delete(problem_data),
                             VALID_STATUS)

    def test_prob_del_has_key(self):
        """Testing problem_type function if data has all keys."""
        invalid_data = {'wrong_key': 3}
        ERROR_DATA['error'] = [{'problem_id': ERROR_MSG['has_key']
                                % 'problem_id'}]
        self.assertEqual(validator.problem_delete(invalid_data),
                         ERROR_DATA)

    def test_prob_del_check_empty(self):
        """Testing problem_type function if value is not empty."""
        invalid_data = {'problem_id': None}
        ERROR_DATA['error'] = [{'problem_id': ERROR_MSG['check_empty']
                                % 'problem_id'}]
        self.assertEqual(validator.problem_delete(invalid_data),
                         ERROR_DATA)

    def test_role_name_exists_incorrect(self):
        """Testing role_name function if role_name is invalid."""
        input_role_name = 'test'
        self.assertFalse(validator.role_name_exists(input_role_name))

    def test_role_name_check_name_exist(self):
        """Testing role_name function if role_name already exists."""
        input_role_name = 'admin'
        self.assertTrue(validator.role_name_exists(input_role_name))

    def test_user_photo_del_return_dict(self):
        """Testing user_photo_deletion function if it returns dictionary."""
        self.assertIsInstance(validator.user_photo_deletion(TEST_DATA), dict)

    def test_user_photo_del_correct(self):
        """Test user_photo_deletion function if status is correct."""
        self.assertDictEqual(validator.user_photo_deletion(TEST_DATA),
                             VALID_STATUS)

    def test_prob_type_del_return_dict(self):
        """Testing problem_type if it returns dictionary."""
        self.assertIsInstance(validator.problem_type_delete(PROBLEM_TYPE_DATA),
                              dict)

    def test_prob_type_del_correct_stat(self):
        """Testing problem_type function if status is correct."""
        self.assertDictEqual(validator.problem_type_delete(PROBLEM_TYPE_DATA),
                             VALID_STATUS)

    def test_prob_type_del_has_key(self):
        """Testing problem_type function if data has all keys."""
        invalid_data = {'wrong_key': 3}
        ERROR_DATA['error'] = [{'problem_type_id': ERROR_MSG['has_key']
                                % 'problem_type_id'}]
        self.assertEqual(validator.problem_type_delete(invalid_data),
                         ERROR_DATA)

    def test_prob_type_del_check_empty(self):
        """Testing problem_type function if value is not empty."""
        invalid_data = {'problem_type_id': None}
        ERROR_DATA['error'] = [{'problem_type_id': ERROR_MSG['check_empty']
                                % 'problem_type_id'}]
        self.assertEqual(validator.problem_type_delete(invalid_data),
                         ERROR_DATA)

    def test_post_prob_type_return_dict(self):
        """Testing problem_type_post function if it returns dictionary."""
        self.assertIsInstance(validator.problem_type_post(PROBLEM_TYPE_DATA),
                              dict)

    def test_post_prob_type_correct_stat(self):
        """Testing problem_type_post function if status is correct."""
        self.assertDictEqual(validator.problem_type_post(PROBLEM_TYPE_DATA),
                             VALID_STATUS)

    def test_post_prob_type_has_key(self):
        """Testing problem_type_post function if data has all keys."""
        invalid_data = {'wrong_key': 'name', 'problem_type_radius': 12}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['has_key']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_post(invalid_data),
                             ERROR_DATA)

    def test_post_prob_type_check_empty(self):
        """Testing problem_type_post function if value is not empty."""
        invalid_data = {'problem_type_name': None,
                        'problem_type_radius': 73}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_empty']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_post(invalid_data),
                             ERROR_DATA)

    def test_post_prob_type_check_str(self):
        """Testing problem_type_post function if type is invalid."""
        invalid_data = {'problem_type_name': [1, 2, 3],
                        'problem_type_radius': 10}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_string']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_post(invalid_data),
                             ERROR_DATA)

    def test_post_prob_type_min_length(self):
        """Testing problem_type_post function if value is not too short."""
        invalid_data = {'problem_type_name': 'q',
                        'problem_type_radius': 10}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_minimum_length']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_post(invalid_data),
                             ERROR_DATA)

    def test_post_prob_type_check_max_length(self):
        """Testing problem_type_post function if value is not too long."""
        invalid_data = {'problem_type_name': 'q' * 256,
                        'problem_type_radius': 10}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_maximum_length']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_post(invalid_data),
                             ERROR_DATA)

    def test_put_prob_type_return_dict(self):
        """Testing problem_type_put function if it returns dictionary."""
        self.assertIsInstance(validator.problem_type_put(PROBLEM_TYPE_DATA),
                              dict)

    def test_put_prob_type_correct_stat(self):
        """Testing problem_type_put function if status is correct."""
        self.assertDictEqual(validator.problem_type_put(PROBLEM_TYPE_DATA),
                             VALID_STATUS)

    def test_put_prob_type_has_key(self):
        """Testing problem_type_put function if data has all keys."""
        invalid_data = {'problem_type_name': 'name', 'problem_type_radius': 12,
                        'wrong_key': 2}
        ERROR_DATA['error'] = [{'problem_type_id': ERROR_MSG['has_key']
                                % 'problem_type_id'}]
        self.assertDictEqual(validator.problem_type_put(invalid_data),
                             ERROR_DATA)

    def test_put_prob_type_check_empty(self):
        """Testing problem_type_put function if value is not empty."""
        invalid_data = {'problem_type_name': 'name',
                        'problem_type_radius': None,
                        'problem_type_id': 2}
        ERROR_DATA['error'] = [{'problem_type_radius': ERROR_MSG['check_empty']
                                % 'problem_type_radius'}]
        self.assertDictEqual(validator.problem_type_put(invalid_data),
                             ERROR_DATA)

    def test_put_prob_type_check_str(self):
        """Testing problem_type_put function if type is invalid."""
        invalid_data = {'problem_type_name': [1, 2, 3],
                        'problem_type_radius': 10,
                        'problem_type_id': 2}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_string']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_put(invalid_data),
                             ERROR_DATA)

    def test_put_prob_type_min_length(self):
        """Testing problem_type_put function if value is not too short."""
        invalid_data = {'problem_type_name': 'q',
                        'problem_type_radius': 10,
                        'problem_type_id': 2}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_minimum_length']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_put(invalid_data),
                             ERROR_DATA)

    def test_put_prob_type_check_max_length(self):
        """Testing problem_type_put function if value is not too long."""
        invalid_data = {'problem_type_name': 'q' * 256,
                        'problem_type_radius': 10,
                        'problem_type_id': 2}
        ERROR_DATA['error'] = [{'problem_type_name': ERROR_MSG['check_maximum_length']
                                % 'problem_type_name'}]
        self.assertDictEqual(validator.problem_type_put(invalid_data),
                             ERROR_DATA)

    def test_user_photo_del_has_key(self):
        """Testing user_photo_deletion function if data has all keys."""
        invalid_data = {'wrong_key': '3'}
        ERROR_DATA['error'] = [{'user_id': ERROR_MSG['has_key'] % 'user_id'}]
        self.assertEqual(validator.user_photo_deletion(invalid_data),
                         ERROR_DATA)

    def test_user_photo_del_check_empty(self):
        """Testing user_photo_deletion function if type is invalid.."""
        invalid_data = {'user_id': None}
        ERROR_DATA['error'] = [{'user_id': ERROR_MSG['check_empty']
                                           % 'user_id'}]
        self.assertEqual(validator.user_photo_deletion(invalid_data),
                         ERROR_DATA)


if __name__ == '__main__':
    unittest2.main()
