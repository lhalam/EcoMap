app.controller('DetailedProblemCtrl', ['$scope', '$rootScope', '$state', '$http', 'toaster', 'msg',
  function($scope, $rootScope, $state, $http, toaster, msg) {
    $scope.photos = [];
    $scope.maxSeverity = [1, 2, 3, 4, 5];
    $scope.comments = [];
    $scope.msg = msg;
    $http({
      "method": "GET",
      "url": "/api/problem_detailed_info/" + $state.params['id']
    }).then(function successCallback(response) {
      $scope.selectProblem = response.data[0][0];
      $scope.photos = response.data[2];
      $scope.comments = response.data[3]
      $rootScope.mapCenter = {
        lat: $scope.selectProblem['latitude'],
        lng: $scope.selectProblem['longitude']
      },
       $rootScope.zoomMap = 9
    }, function errorCallback(error) {
      $state.go('error404');
    });

    $scope.close = function() {
      $state.go('map')
    };

    $scope.getStatus = function(status) {
      var statuses = {
        'Unsolved': 'Не вирішено',
        'Solved': 'Вирішено'
      };
      return statuses[status];
    }
    $scope.getProblemType = function(type_id) {
      var types = {
        1: 'Проблеми лісів',
        2: 'Сміттєзвалища',
        3: 'Незаконна забудова',
        4: 'Проблеми водойм',
        5: 'Загрози біорізноманіттю',
        6: 'Браконьєрство',
        7: 'Інші проблеми'
      };
      return types[type_id];
    };
    $scope.post_comment = function(comment) {
      if (comment.text) {
        $http({
          method: 'POST',
          url: '/api/problem/add_comment',
          data: {
            content: comment.text,
            problem_id: $state.params['id']
          }
        }).then(function successCallback() {
          $scope.msg.addCommentSuccess('коммента');
          $http({
            method: 'GET',
            url: '/api/problem_comments/' + $state.params['id']
          }).then(function successCallback(response) {
            $scope.comments = response.data;
            comment.text = '';
          })
        }, function errorCallback() {
          $scope.msg.addCommentError('коммента');
        });
      } else {
        return;
      }
    }
  }
  ]);