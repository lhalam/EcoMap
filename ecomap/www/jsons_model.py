import json
from pprint import pprint
#
# json = {
#
#     "resource_name": {
#         [{'admin': {
#             'permissions':
#                 [{"put": 'own'},
#                 {'get': 'any'},
#                 {'post': 'none'}]
#
#                 }
#         },
#
#         {'user': {
#             'permissions':
#                 [{"put": 'own'},
#                 {'get': 'any'},
#                 {'post': 'none'}]
#
#                 }
#         },
#         ]
#     }
# }

sql_tuple = [['resource', 'post', 'any', 'user'],
       ['admin_page', 'del', 'own', 'user'],
       ['admin_page', 'del', 'any', 'admin'],
       ['admin_page', 'post', 'any', 'admin'],
       ['admin_page', 'post', 'None', 'user'],
       ['admin_page', 'put', 'own', 'user'],
       ['admin_page', 'put', 'none', 'guest'],
       ['admin_page', 'put', 'any', 'admin'],
       ['problems', 'post', 'any', 'admin'],
       ['problems', 'put', 'None', 'user'],
       ['problems', 'put', 'any', 'admin']]

# #unique res
# def fj(sql_tuple):
#     # dct = {}
#     for y in sql_tuple:
#         dct = {}
#         dct[y[0]] = [{}]
#         for x in sql_tuple:
#             # dct[y[0]] = {x[1]: []}
#             if x[0] in dct.iterkeys():
#                 dct[x[0]].append(x[1])
#         print dct
# print fj(sql_tuple)



def js_js2(sql_list):
    dct = {}
    for (resource, method, perm, role) in sql_list:
        if resource not in dct:
            dct[resource] = []
        if method not in dct[resource]:
            dct[resource].append({method: [{role: perm}]})
        # dct[resource][method] = {}
        # if role not in dct[resource][method]:
        #     # dct[resource][method][perm] = {}
        #     dct[resource][method][role] = []
        #     if role not in dct[resource][0]:
        #         try:
        #             dct[resource].append({role: perm})
        #         # print [{k:v} for k,v in dct[resource][method].items()]
        #         except:
        #             pass
    return dct


#         if resource not in dct:
#             dct[resource] = []
#         if method not in dct[resource]:
#             dct[resource].append({method: [{role: perm}]})
def js_js(sql_list):
    dct = {}
    for (resource, method, perm, role) in sql_list:
        if resource not in dct:
            dct[resource] = {}
        if method not in dct[resource]:
            dct[resource][method] = []
        # dct[resource][method] = {}
        # if role not in dct[resource][method]:
        #     # dct[resource][method][perm] = {}
        #     dct[resource][method][role] = []
        if role not in dct[resource][method]:
            dct[resource][method].append({role: perm})
            # print [{k:v} for k,v in dct[resource][method].items()]
    return dct





#
# def js_js(sql_list):
#     dct = {}
#     for (resource, method, perm, role) in sql_list:
#         if resource not in dct:
#             dct[resource] = []
#         if method not in dct[resource]:
#             dct[resource].append({method:{}})
#         if role not in dct[resource]:
#             for met in dct[resource]:
#                 for k,v in met.items():
#                     met[k].update({role:perm})
#
#                 print met.values()[0]
#             # print 'olo'
#             # dct[resource]({role: perm})
#     return dct
dd = (js_js(sql_tuple))
pprint(dd)
# print dd['problems']
# def fj(sql_tuple):
#     dct = {}
#     for x1 in sql_tuple:
#         # dct = {}
#         for x2 in sql_tuple:
#             dct[x1[0]] = {x2[1]: []}
#             # for x in sql_tuple:
#             #     dct[x[0]]
#         print dct


# for x in sql_tuple:
#             if x[0] in dic2.iterkeys():
#                 dic2[_res_name].append(x[1])
#         yield dic2



# print '****starst'
# dic = {}
# for x in sql_tuple:
#
#     dic[x[0]] = {x[1]:x[2]}
#     # dic[_res_name].append(x[1])
# print dic
# print 'endnednended'


def make_json(sql_tuple):
    # dic2 = {}
    for x in sql_tuple:
        dic2 = {}
        _res_name = x[0]
        # print _res_name
        dic2[_res_name] = []

        for x in sql_tuple:
            if x[0] in dic2.iterkeys():
                dic2[_res_name].append(x[1])
        yield dic2


# # print make_json(sql_tuple)
# for x in make_json(sql_tuple):
#     d3 = {}
#     print x

js3 = {

    'comment': (
        ({
            'put': ({'admin': 'any'},
                    {'user': 'own'})
        },
        {
            'post': ({'admin': 'any'},
                     {'user': 'own'})
            }
        )
    ),
    'problem': (
        ({
            'get': ({'admin': 'any'},
                    {'user': 'own'})
        },
        {
            'del': ({'admin': 'any'},
                     {'user': 'own'})
            }
        )
    ),
}
# j =json.dumps(js3)
# pprint(js3)
# print [x for x in js3]
# print "***"
# for x in js3['problem']:
#     print x
#
print "*******"
for res_name, resource in js3.items():
    # pprint ('<' + res_name + '>')
    # pprint(resource)
    for permissions in resource:
        # pprint(permissions)
        for methods in permissions:
            # pprint(methods)
            for role_perm in permissions[methods]:
                # pprint(role_perm)
                for role, perm in role_perm.iteritems():
                    r= role, perm


# pprint(js3)