"""Module which contains Test of Validator functions. """

import unittest2

from ecomap import validator


# input data
REGISTRATION_DATA = {'email': 'admin@gmail.com',\
                     'first_name': 'admin',\
                     'last_name': 'admin',\
                     'password': 'db51903d292a412e4ef2079add791eae',\
                     'pass_confirm': 'db51903d292a412e4ef2079add791eae'}

VALID_STATUS = {'status': True, 'error': []}

TEST_DATA_PUT = {'resource_name': '/res_name1', 'resource_id': '1234567'}

TEST_DATA_PERMISSION = {'permission_id': '1234567',\
                         'action': 'PUT',\
                         'modifier': 'Own',\
                         'description': 'user'}

TEST_DATA_POST_COMMENT = {'content': 'comment', 'problem_id': '77'}

TEST_DATA_RESOURCE_DELETE = {'resource_id': 1111}

TEST_DATA_USER_ROLE_PUT = {'role_id': 3, 'user_id': 4}

ROLES_DATA = {'user': (2L, ), 'admin': (1L, )}

RESOURCE_DATA = {'/api/roles': (18L,), '/api/login': (17L,)}


def resource_name_exists_mock(resource_name):
    """Mock of resource_name_exists function"""
    if resource_name in RESOURCE_DATA:
        return RESOURCE_DATA[resource_name]
    else:
        return None

def role_name_exists_mock(role_name):
    """Mock of role_name_exists function"""
    if role_name in ROLES_DATA:
        return ROLES_DATA[role_name]
    else:
        return None

class TestValidator(unittest2.TestCase):
    """ Class for test validator.py"""

    def setUp(self):
        """ Setting up for the test """
        self.data_registration = REGISTRATION_DATA
        self.data_check_post_comment = TEST_DATA_POST_COMMENT
        self.data_resource_put = TEST_DATA_PUT
        self.data_resource_delete = TEST_DATA_RESOURCE_DELETE
        self.data_permission_post = TEST_DATA_PERMISSION
        self.data_user_role_put = TEST_DATA_USER_ROLE_PUT

        self.valid_status = VALID_STATUS

        self.original_role_name_exists = validator.role_name_exists
        validator.role_name_exists = role_name_exists_mock
        self.original_resource_name_exists = validator.resource_name_exists
        validator.resource_name_exists = resource_name_exists_mock

    def tearDown(self):
        """Cleaning up after the test"""
        validator.role_name_exists = self.original_role_name_exists
        validator.resource_name_exists = self.original_resource_name_exists


    # user_registration tests
    def test_registr_return_dictionary(self):
        """ testing if user_registration return
        a dictionary in user_registration function.
        """
        return_data = validator.user_registration(self.data_registration)
        self.assertIsInstance(return_data, dict)

    def test_registr_correct_status(self):
        """testing status with correct
        user_registration in user_registration function.
        """
        return_data = validator.user_registration(self.data_registration)
        expected = self.valid_status
        self.assertTrue(return_data, expected)

    def test_registr_has_key(self):
        """testing if data has all keys
        in user_registration function.
        """
        del self.data_registration['first_name']
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'first_name': 'not contain first_name key.'}]}
        self.data_registration['first_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registr_not_empty_data(self):
        """testing if value is not empty in
         user_registration function.
         """
        self.data_registration['last_name'] = ""
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'last_name': 'last_name value is empty.'}]}
        self.data_registration['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registr_maximum_length(self):
        """testing if value of data is not too long
        in user_registration function.
        """
        self.data_registration['last_name'] = 'a'*260
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'last_name': 'last_name value is too long.'}]}
        self.data_registration['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registr_minimum_length(self):
        """testing if value of data is not too short
        in user_registration function.
        """
        self.data_registration['last_name'] = 'a'
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'last_name': 'last_name value is too short.'}]}
        self.data_registration['last_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registr_check_string(self):
        """testing invalid type in data
        in user_registration function.
        """
        self.data_registration['first_name'] = 125698
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'first_name': 'first_name value is not string.'}]}
        self.data_registration['first_name'] = 'admin'
        self.assertEqual(return_data, expected)

    def test_registr_incorrect_email(self):
        """testing invalid email in data
        in user_registration function.
        """
        self.data_registration['email'] = "admin@gmail"
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'email': 'email value does not look like email.'}]}
        self.data_registration['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)

    def test_registr_check_email_exist(self):
        """testing invalid email in data
        in user_registration function.
        """
        self.data_registration['email'] = "admin.mail@gmail.com"
        return_data = validator.user_registration(self.data_registration)
        expected = {'status': False, 'error': [{'email': 'email allready exists.'}]}
        self.data_registration['email'] = 'admin@gmail.com'
        self.assertEqual(return_data, expected)


    # check_post_comment tests
    def test_post_comment_return_type(self):
        """ Testing if check_post_comment returns
        a dictionary in permission_post function.
        """
        self.assertIsInstance(validator.check_post_comment(self.data_check_post_comment), dict)

    def test_post_comment_correct_status(self):
        """ Check if status is correct. """
        expected = validator.check_post_comment(self.data_check_post_comment)
        actual = self.valid_status
        self.assertDictEqual(expected, actual)

    def test_post_comment_has_key(self):
        """ Testing if data has all keys
        in check_post_comment function.
        """
        invalid_data = {'content': 'comment'}
        actual = {'status': False, 'error': [{'problem_id': 'not contain problem_id key.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_not_empty_data(self):
        """ Testing if return value is not empty in
         check_post_comment function.
         """
        invalid_data = {'content': 'comment', 'problem_id': None}
        actual = {'status': False, 'error': [{'problem_id': 'problem_id value is empty.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_check_string(self):
        """ Testing invalid type in data
        in check_post_comment function.
        """
        invalid_data = {'content': [1, 2, 3], 'problem_id': '77'}
        actual = {'status': False, 'error': [{'content': 'content value is not string.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_minimum_length(self):
        """ Testing if content is not too short
        in check_post_comment function.
        """
        invalid_data = {'content': 'q', 'problem_id': '77'}
        actual = {'status': False, 'error': [{'content': 'content value is too short.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)

    def test_post_comment_check_maximum_length(self):
        """ Testing if content is not too long
        in check_post_comment function.
        """
        invalid_data = {'content': 'q' * 256, 'problem_id': '77'}
        actual = {'status': False, 'error': [{'content': 'content value is too long.'}]}
        self.assertDictEqual(validator.check_post_comment(invalid_data), actual)


    # resource_put tests
    def test_res_put_return_dictionary(self):
        """ testing if resource_put return a dictionary in resource_put dunction"""
        return_data = validator.resource_put(self.data_resource_put)
        self.assertIsInstance(return_data, dict)

    def test_res_put_correct_status(self):
        """testing status with correct resource_putin resource_put dunction."""
        return_data = validator.resource_put(self.data_resource_put)
        expected = self.valid_status
        self.assertTrue(return_data, expected)

    def test_res_put_not_empty_data(self):
        """testing invalid email in data in resource_put dunction."""
        test_data = {'resource_name': '', 'resource_id': ''}
        return_data = validator.resource_put(test_data)
        expected = {'status': False, 'error': [{'resource_name': 'resource_name value is empty.'},\
                                                {'resource_id': 'resource_id value is empty.'}]}
        self.assertEqual(return_data, expected)

    def test_res_put_has_key(self):
        """testing if data has all keys in resource_put dunction."""
        del self.data_resource_put['resource_id']
        return_data = validator.resource_put(self.data_resource_put)
        expected = {'status': False, 'error': [{'resource_id': 'not contain resource_id key.'}]}
        self.data_resource_put['resource_id'] = '12345'
        self.assertEqual(return_data, expected)

    def test_res_put_name_is_string(self):
        """testing if resouce_name is string in resource_put dunction."""
        self.data_resource_put['resource_name'] = 123
        return_data = validator.resource_put(self.data_resource_put)
        expected = {'status': False, 'error': [{'resource_name': \
                                                'resource_name value is not string.'}]}
        self.data_resource_put['rresource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_res_put_minimum_length(self):
        """testing if resouce_name is not too short in resource_put dunction."""
        self.data_resource_put['resource_name'] = "a"
        return_data = validator.resource_put(self.data_resource_put)
        expected = {'status': False, 'error': [{'resource_name': \
                                                'resource_name value is too short.'}]}
        self.data_resource_put['resource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_res_put_maximum_length(self):
        """testing if resouce_name is not too long in resource_put dunction."""
        self.data_resource_put['resource_name'] = "a"*256
        return_data = validator.resource_put(self.data_resource_put)
        expected = {'status': False, 'error': [{'resource_name': \
                                                'resource_name value is too long.'}]}
        self.data_resource_put['resource_name'] = '/res_name1'
        self.assertEqual(return_data, expected)

    def test_res_put_name_exist(self):
        """testing if resouce_name is already exist in resource_put dunction."""
        self.data_resource_put['resource_name'] = '/api/roles'
        return_data = validator.resource_put(self.data_resource_put)
        expected = {'status': False, 'error': [{'resource_name': \
                                                '"/api/roles" name allready exists.'}]}
        self.assertEqual(return_data, expected)


    # resource_delete tests
    def test_res_delete_return_type(self):
        """ Testing if resource_delete returns
        a dictionary in permission_post function.
        """
        self.assertIsInstance(validator.resource_delete(self.data_resource_delete), dict)

    def test_res_delete_correct_status(self):
        """ Testing if status is correct. """
        expected = validator.resource_delete(self.data_resource_delete)
        actual = self.valid_status
        self.assertDictEqual(expected, actual)

    def test_res_delete_not_empty_data(self):
        """ Testing if return data is not empty
        in resource_delete function.
        """
        invalid_data = {'resource_id': None}
        actual = {'status': False, 'error': [{'resource_id': 'resource_id value is empty.'}]}
        self.assertDictEqual(validator.resource_delete(invalid_data), actual)

    def test_res_delete_has_key(self):
        """ Testing if data has all keys
        in resource_delete function.
        """
        invalid_data = {'test': 1}
        actual = {'status': False, 'error': [{'resource_id': 'not contain resource_id key.'}]}
        self.assertDictEqual(validator.resource_delete(invalid_data), actual)


    # permission_post tests
    def test_perm_post_is_dictionary(self):
        """ testing if resource_put return
        a dictionary in permission_post function.
        """
        return_data = validator.permission_put(self.data_permission_post)
        self.assertIsInstance(return_data, dict)

    def test_perm_post_correct_status(self):
        """testing status with correct
        resource_put in permission_post function.
        """
        return_data = validator.permission_put(self.data_permission_post)
        expected = self.valid_status
        self.assertTrue(return_data, expected)

    def test_perm_post_has_key(self):
        """testing if data has all keys
        in permission_post function.
        """
        del self.data_permission_post['action']
        return_data = validator.permission_put(self.data_permission_post)
        expected = {'status': False, 'error': [{'action': 'not contain action key.'}]}
        self.data_permission_post['action'] = 'PUT'
        self.assertEqual(return_data, expected)

    def test_perm_post_empty_data(self):
        """testing if data dont have empty value
        in permission_post function.
        """
        self.data_permission_post['action'] = ""
        return_data = validator.permission_put(self.data_permission_post)
        expected = {'status': False, 'error': [{'action': 'action value is empty.'}]}
        self.data_permission_post['action'] = 'PUT'
        self.assertEqual(return_data, expected)

    def test_perm_post_minimum_length(self):
        """testing if description is not too short
        in permission_post function.
        """
        self.data_permission_post['description'] = "a"
        return_data = validator.permission_put(self.data_permission_post)
        expected = {'status': False, 'error': [{'description': 'description value is too short.'}]}
        self.data_permission_post['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_perm_post_maximum_length(self):
        """testing if description is not too long
        in permission_post function.
        """
        self.data_permission_post['description'] = "a"*256
        return_data = validator.permission_put(self.data_permission_post)
        expected = {'status': False, 'error': [{'description': 'description value is too long.'}]}
        self.data_permission_post['description'] = 'user'
        self.assertEqual(return_data, expected)

    def test_perm_post_is_string(self):
        """testing if description is string
        in permission_post function.
        """
        self.data_permission_post['description'] = 123
        return_data = validator.permission_put(self.data_permission_post)
        expected = {'status': False, 'error': [{'description': 'description value is not string.'}]}
        self.data_permission_post['description'] = 'user'
        self.assertEqual(return_data, expected)


    # user_role_put tests
    def test_user_role_put_return_type(self):
        """ Testing if user_role_put returns
        a dictionary in permission_post function.
        """
        self.assertIsInstance(validator.user_role_put(self.data_user_role_put), dict)

    def test_user_role_put_correct_status(self):
        """ Testing if status is correct. """
        expected = validator.user_role_put(self.data_user_role_put)
        actual = self.valid_status
        self.assertDictEqual(expected, actual)

    def  test_return_error_empty_dict(self):
        """ Testing if return data is not empty
        in user_role_put function.
        """
        invalid_data = {'role_id': None, 'user_id': 2}
        actual = {'status': False, 'error': [{'role_id': 'role_id value is empty.'}]}
        self.assertDictEqual(validator.user_role_put(invalid_data), actual)

    def test_return_error_has_key(self):
        """ Testing if return dictionary is correct. """
        invalid_data = {'test': 1, 'user_id': 3}
        actual = {'status': False, 'error': [{'role_id': 'not contain role_id key.'}]}
        self.assertDictEqual(validator.user_role_put(invalid_data), actual)


    # role_name_exists tests
    def test_role_name_exist_correct_data(self):
        """ Testing with input data when role_name exists. """
        input_role_name = 'admin'
        self.assertTupleEqual(validator.role_name_exists(input_role_name), (1L,))

    def test_role_name_exist_incorrect_data(self):
        """ Testing with input data when role_name doesn't exists. """
        input_role_name = 'test'
        self.assertEqual(validator.role_name_exists(input_role_name), None)



    #def test_perm_post_is_enum(self):
    #    """testing if modifier or action is ENUM
    #    in permission_post function.
    #    """
    #   self.data_permission_post['modifier'] = 'user'
    #    return_data = validator.permission_put(self.data_permission_post)
    #    expected = {'status': False, 'error': [{'modifier': 'invalid modifier value.'}]}
    #    self.data_permission_post['modifier'] = 'Own'
    #    self.assertEqual(return_data, expected)
    #
    # !!!!! 'check_enum_value': 'invalid %s value.' In str.434
    # we have ERROR_MSG['is_in_enum']. Not such value in ERROR_MSG

if __name__ == '__main__':
    unittest2.main()
