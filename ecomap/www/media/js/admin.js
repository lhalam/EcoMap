var admin = angular.module("admin", [])

admin.controller("mainCtrl", function ($scope, $http) {
    $scope.resourceShow = false
    $scope.permisShow = false
    $scope.acceptedData
    $scope.tablesData = {
        'news': {
            'PUT': {
                'Admin': {'perm': 'None', 'role_id': 1},
                'Moderator': {'perm': 'None', 'role_id': 2}
            }, 'POST': {
                'Admin': {'perm': 'None', 'role_id': 1},
                'Moderator': {'perm': 'None', 'role_id': 2}
            }, 'GET': {
                'Admin': {'perm': 'None', 'role_id': 1},
                'Moderator': {'perm': 'None', 'role_id': 2}
            }, 'DELETE': {
                'Admin': {'perm': 'None', 'role_id': 1},
                'Moderator': {'perm': 'None', 'role_id': 2}
            }, 'resource_id': 1
        },
        'problem': {
            'PUT': {
                'Moderator': {'perm': 'None', 'role_id': 2},
                'Admin': {'perm': 'None', 'role_id': 1}
            },
            'POST': {'Admin': {'perm': 'None', 'role_id': 1}, 'Moderator': {'perm': 'None', 'role_id': 2}},
            'GET': {'Moderator': {'perm': 'None', 'role_id': 2}, 'Admin': {'perm': 'None', 'role_id': 1}},
            'DELETE': {'Admin': {'perm': 'None', 'role_id': 1}, 'Moderator': {'perm': 'None', 'role_id': 2}},
            'resource_id': 2
        },
        'cabinet': {
            'PUT': {'Moderator': {'perm': 'None', 'role_id': 2}, 'Admin': {'perm': 'None', 'role_id': 1}},
            'POST': {'Admin': {'perm': 'None', 'role_id': 1}, 'Moderator': {'perm': 'None', 'role_id': 2}},
            'GET': {'Moderator': {'perm': 'None', 'role_id': 2}, 'Admin': {'perm': 'None', 'role_id': 1}},
            'DELETE': {'Admin': {'perm': 'None', 'role_id': 1}, 'Moderator': {'perm': 'None', 'role_id': 2}},
            'resource_id': 3
        }
    }
    $scope.loadRes = function () {
        $scope.resourceShow = !$scope.resourceShow
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.acceptedData = data.data
            console.log($scope.acceptedData)
        }, function errorCallback(response) {
            console.log(response)
        });
    }
    $scope.addRes = function (newName) {
        $http({
            method: "POST",
            url: "/api/resources",
            data: {
                'resource_name': newName
            }
        }).then(function successCallback(data) {
            var addedobject = data.data['added_resource']

            $scope.tablesData[addedobject] = {}
        }, function errorCallback(response) {
            console.log(response)
        });
    }
    var tableIter = 0;
    $scope.loadPermis = function () {
        $scope.permisShow = !$scope.permisShow
        $scope.DataGenerator = function (id) {
            $http({
                method: "GET",
                url: '/api/permissions',
                params: {
                    'resource_id': id
                }
            }).then(function successCallback(data) {
                console.log(data.data)
            }, function errorCallback(response) {
                console.log(response)
            })

        }
        for (res in $scope.acceptedData) {
            console.log(res)
            var id = $scope.acceptedData[res]
            $scope.DataGenerator(id)
        }

    }
})
