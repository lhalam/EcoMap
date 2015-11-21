from pprint import pprint

sql_tuple = [['user', '/', 'GET', 'any'],
             ['admin', '/', 'GET', 'any'],
             ['admin', '/', 'PUT', 'any'],
             ['admin', '/api', 'GET', 'any'],
             ['admin', '/api', 'PUT', 'any'],
             ['admin', '/api', 'POST', 'any'],
             ['admin', '/api', 'DELETE', 'any'],
             ['moder', '/api', 'DELETE', 'any'],
             ['user', '/api', 'DELETE', 'None'],
             ['user', '/api', 'PUT', 'Own'],
             ['moder', '/new', 'DELETE', 'any'],
             ['moder', '/', 'GET', 'any'],
             ['moder', '/api', 'PUT', 'any'],
             ['user', '/api', 'GET', 'any']]


def make_json(sql_list):
    dct = {}
    for (role, resource, method, perm) in sql_list:
        if role not in dct:
            dct[role] = {}
        if resource not in dct[role]:
            dct[role][resource] = {}
        if method not in dct[role][resource]:
            dct[role][resource].update({method: perm})
    return dct


def get_id_problem_owner(problem_id):
    """
    returns id of problem owner
    :param problem_id - problem id
    :return: id of problem owner
    """
    print 'input problem_id %s' % problem_id
    print 'DO STUFF'
    print 'current user in request %s' % current_user_uid
    result = 5
    return result


def get_current_user_id(user_id):
    """
    returns id of current user
    :param user_id - user id to check
    :return: id of problem owner
    """
    print user_id
    print current_user_uid
    return current_user_uid if int(user_id) == int(current_user_uid) else False


def get_id_photo_owner(photo_id):
    """
    returns id of photo owner
    :param photo_id - photo id
    :return: id_user
    """
    pass

current_user_uid = 5

d = {':idUser': get_current_user_id,
     ':idProblem': get_id_problem_owner
     }

TESTJSON = {'admin': {'/api/roles/': {'PUT': 'Own', 'POST': 'Any', 'GET': 'Any', 'DELETE': 'None'},
                      '/': {'GET': 'Any'},
                      '/api/user_detailed_info/:idUser': {'GET': 'Any', 'PUT': 'Own', 'DELETE': 'None'},
                      '/api/problem/:idProblem': {'PUT': 'Own', 'POST': 'Any', 'GET': 'Any', 'DELETE': 'Any'}},
            'user': {'/api/roles': {'POST': 'Any'},
                     '/api/user_detailed_info/:idUser': {'GET': 'Own', 'PUT': 'Own', 'DELETE': 'None'},
                     '/': {'GET': 'Any', 'PUT': 'None'}}}

ROLE = 'user'
REQUEST_RESOURCE = '/api/user_detailed_info/5'
REQUEST_METHOD = 'GET'


# def run_dynamic_check(pattern, query_arg, url_rules, perm_dct, role, method):
#     if pattern in url_rules:
#                         if ":idUser" == pattern:
#                             pass
#
#                         if ":idProblem" == pattern:
#                             id = get_id_problem_owner(query_arg)
#                             if perm_dct[role][permission_res][method] == 'Any':
#                                 permission['status'] = 'ok any'
#                                 # return True
#                             if perm_dct[role][permission_res][method] == 'Own':
#                                 # print id
#                                 if current_user_uid == id:
#                                     permission['status'] = 'ok own'
#                                     # return True
#                                 else:
#                                     permission['error'] = 'YOU HAVE ACCESS ONLY TO OWN'
#                                     # return permission['error']
#

def check3(role, resource, method, dct):
    permission = {'status': None, 'error': None}
    if role in dct:
        xpath = dct[role]
        for permission_res in xpath:
            if resource in dct[role]:
                for perms in dct[role][resource]:
                    if method in dct[role][resource]:
                        if dct[role][resource][method] == 'Any':
                            permission['status'] = 'ok'
                        elif dct[role][resource][method] == 'Own':
                            permission['warning'] = 'you have an error in admin'
                        elif dct[role][resource][method] == 'None':
                            permission['error'] = 'METHOD FORBIDDEN BY ADMIN, 403'
                    else:
                        permission['error'] = 'METHOD FORBIDDEN'
            else:
                if ':' in permission_res:  # checking dynamic path
                    # print permission_res
                    # print 80 * '*'

                    dynamic_res_pattern = permission_res.split('/')[-1]
                    dynamic_res_host = '/'.join(permission_res.split('/')[:-1])
                    dynamic_res = dynamic_res_host + dynamic_res_pattern

                    # print dynamic_res_host
                    # print dynamic_res_pattern  # id:problem
                    # print dynamic_res

                    request_res_arg = resource.split('/')[-1]
                    request_res_host = '/'.join(resource.split('/')[:-1])  # /api/problem
                    request_res = resource

                    # print 80 * '-'
                    # print request_res_host
                    # print request_res_arg
                    # print request_res
                    # print 80 * '*'

                    if request_res_host == dynamic_res_host:
                        print 'MATCH %s = %s' % (request_res_host, dynamic_res_host)
                        print dynamic_res_pattern
                        if dynamic_res_pattern in d:
                                owner_id = d[dynamic_res_pattern](request_res_arg)
                                if dct[role][permission_res][method] == 'Any':
                                    permission['status'] = 'ok any'
                                    return True
                                if dct[role][permission_res][method] == 'Own':
                                    # print owner_id
                                    if current_user_uid == owner_id:
                                        permission['status'] = 'ok own'
                                        return True
                                    else:
                                        permission['error'] = 'YOU HAVE ACCESS ONLY TO YOUR OWN %s' % request_res_host
                                        return permission['error']
                else:
                    permission['error'] = 'NO SUCH RESOURCE FOR ROLE'
    else:
        permission['error'] = 'NOT ALLOWED FOR THIS ROLE'

    print permission
    if not permission['error']:
        return True
    else:
        return permission['error']

print 80*'*'
print check3(ROLE, REQUEST_RESOURCE, REQUEST_METHOD, TESTJSON)


pprint(make_json(sql_tuple))
# route = '/api/user_detailed_info/<int:user_id>'
# if '<int' in route:
#     route = route.split('<')[0] + '3'
#     print route

TESTJSON = {'admin': {'/api/roles/': {'PUT': 'Own', 'POST': 'Any', 'GET': 'Any', 'DELETE': 'None'},
                      '/': {'GET': 'Any'},
                      '/api/user_detailed_info/:idUser': {'GET': 'Any', 'PUT': 'Own', 'DELETE': 'None'},
                      '/api/problem/:idProblem': {'PUT': 'Own', 'POST': 'Any', 'GET': 'Any', 'DELETE': 'Any'}},
            'user': {'/api/roles': {'POST': 'Any'},
                     '/api/user_detailed_info/:idUser': {'GET': 'Own', 'PUT': 'Own', 'DELETE': 'None'},
                     '/': {'GET': 'Any', 'PUT': 'None'}}}

#
# def parse_json(js):
#     res_list = []
#     for roles in js:
#         res_list.append([roles])
#         for role in res_list:
#             print role
#         # for res in js[roles]:
#             # print res
#             # for role_list in res_list:
#             #     role_list.append(res[0])
#     return res_list
#
# # def parse_json(js):
# #     res_list = []
# #     res_list.append([js])
# #     return res_list
#
# print parse_json(TESTJSON)