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
import pprint

req = [['resource', 'post', 'any', 'user'], ['resource', 'del', 'any', 'user'], ['resource', 'put', 'any', 'user']]
dic = {}
for x in req:
    dic[x[0]] = x[0]
print dic
# req = ['resource', 'del', 'own', 'user']
# req = ['problem', 'post', 'any', 'admin']
# req = ['resource', 'post', 'any', 'user']


js3 = {

    'res_name': (
        ({
            'put': {
                'admin': 'any',
                'user': 'own'
            }
        },
        {
            'post': {
                'admin': 'any',
                'user': 'own'
            }
        })
    ),
    'problem': (
        {
            'get': {
                'admin': 'any',
                'user': 'own'
            }
        },
        {
            'post': {
                'admin': 'any',
                'user': 'own'
            }
        }
    )
}


# print [x for x in js2]
# j =json.dumps(js3)
from pprint import pprint
pprint(js3)