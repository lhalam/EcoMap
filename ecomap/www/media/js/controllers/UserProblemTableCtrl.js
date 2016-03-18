app.controller('UserProblemTableCtrl', ['$scope', '$http', '$state', '$cookies', '$window', 'toaster',
  function($scope, $http, $state, $cookies, $window, toaster) {
    $scope.showTable = ($cookies.get('role')=='user')?false:true;
    $scope.nickname = ($cookies.get('role')=='user')?false:true;
    $scope.user_id = $cookies.get('id');
    $scope.selectCountObj = {
      '1': '5',
      '2': '10',
      '3': '15',
      '4': '20',
      '5': '50',
      '6': '100'
    }
    $scope.selectCount = {
      'selected': '5'
    }
    $scope.getStatus = function(status) {
      var statuses = {
        'Unsolved': 'Не вирішено',
        'Solved': 'Вирішено'
      };
      return statuses[status];
    };
    $scope.filterTable = {
      'param': '',
      'order': 1
    }
    if ($cookies.get('role')=='user' && $cookies.get('id')!=2) {
      $http({
        url: '/api/user_detailed_info/' + $cookies.get('id'),
        method: 'GET'
      }).success(function(response) {
        $scope.old_nick = response.nickname;
        $scope.searchNick = $scope.old_nick;
        $scope.loadProblems();
      });
    }
    $scope.searchNick = ($cookies.get('role')=='user')?$scope.old_nick:null;
    $scope.sortFilter = function(filtr){
          $scope.filterTable.param = filtr;
          var par = "order_"+$scope.filterTable.param;
          $scope.filterTable[par] = $scope.filterTable[par]?0:1;
          $scope.loadProblems();
    }

    $scope.loadProblems = function() {
      $scope.msg = msg;
      $scope.fromPage = 1;
      $scope.bigCurrentPage = 1;
      $scope.problemsLength = $scope.selectCount['selected'];
      $scope.bigTotalItems = $scope.problemsLength / $scope.selectCount['selected'] * 10;
      $scope.$watch('bigCurrentPage', function(newValue, oldValue) {
        var stepCount = $scope.selectCount['selected']
        if ($scope.searchNick){
            $scope.showTable = ($cookies.get('role')!=='user');
            $scope.nickname = true;
            $http({
              method: 'GET',
              url: '/api/search_usersProblem',
              params: {
                nickname: $scope.searchNick, 
                filtr: $scope.filterTable.param || undefined,
                order: $scope.filterTable["order_"+$scope.filterTable.param] || 0,
                per_page: $scope.selectCount['selected'],
                offset: $scope.selectCount['selected'] * newValue - stepCount
              }
            }).then(function successCallback(response) {
             $scope.problems = response.data[0];
             $scope.problemsLength = response.data[1][0]['total_problem_count'];
             $scope.count = response.data[1][0]['total_problem_count'];
             $scope.bigTotalItems = $scope.problemsLength / $scope.selectCount['selected'] * 10;
           })
        } else {
          $http({
            method: 'GET',
            url: 'api/all_usersProblem',
            params: {
              filtr: $scope.filterTable.param || undefined,
              order: $scope.filterTable["order_"+$scope.filterTable.param] || 0,
              per_page: $scope.selectCount['selected'],
              offset: $scope.selectCount['selected'] * newValue - stepCount
            }
          }).then(function successCallback(response) {
            $scope.problems = response.data[0];
            $scope.problemsLength = response.data[1][0]['total_problem_count'];
            $scope.count = response.data[1][0]['total_problem_count'];
            $scope.bigTotalItems = $scope.problemsLength / $scope.selectCount['selected'] * 10;
          })
        }
        // } else{
        //   $scope.nickname = false;
        //   $http({
        //     method: 'GET',
        //     url: 'api/usersProblem/' + $scope.user_id,
        //     params: {
        //       filtr: $scope.filterTable.param || undefined,
        //       order: $scope.filterTable["order_"+$scope.filterTable.param] || 0,
        //       per_page: $scope.selectCount['selected'],
        //       offset: $scope.selectCount['selected'] * newValue - stepCount,
        //     }
        //   }).then(function successCallback(response) {
        //    $scope.problems = response.data[0];
        //    $scope.problemsLength = response.data[1][0]['total_problem_count'];
        //    $scope.count = response.data[1][0]['total_problem_count'];
        //    $scope.bigTotalItems = $scope.problemsLength / $scope.selectCount['selected'] * 10;
        //  })
        // }
      })
    };
    $scope.idProblem = 0;
    $scope.deleteProblem = function(id, title, user_id) {
      $scope.idProblem = id;
      if($cookies.get('role')=='admin' || $cookies.get('role')=='moderator'){
        $http({
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
          url: '/api/problem_delete',
          data: {
            'problem_id': id, 
            'problem_title': title,
            'user_id': user_id
          }
        }).then(function successCallback(data) {
          $scope.loadProblems();
          $scope.idProblem = 0;
          $scope.msg.deleteSuccess('проблема');
        }, function errorCallback(response) {
          $scope.idProblem = 0;
          $scope.msg.deleteError('проблема', arguments[0]['data']['msg']);
        })
      }
      else{
        $http({
        url: '/api/problem_delete',
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        data: {
          'problem_id': id, 
          'problem_title': title,
          'user_id': user_id
        }
        }).then(function successCallback(data){
          $scope.loadProblems();
          $scope.idProblem = 0;
          toaster.pop('success','проблема', 'Проблема успішно перенесена на анонімного користувача.');
        }, function errorCallback(response) {
          $scope.idProblem = 0;
          $scope.msg.deleteError('проблема', arguments[0]['data']['msg']);
        })
        }
      };

    $scope.loadProblems();
    
    $scope.triggerDetailModal = function(problem_id) {
      var url = '/#/detailedProblem/' + problem_id;
      window.open(url, '_blank');
    }
    $scope.triggerEditModal = function(problem_id) {
      if($cookies.get('role')=='user'){
        $scope.linkEditProblem = '/#/editProblem/' + problem_id;
      } else if($cookies.get('role')=='admin' || $cookies.get('role')=='moderator'){
        $scope.linkEditProblem = '/#/detailedProblem/' + problem_id;
      }     
    };

  }
]);