app.controller('DetailedProblemCtrl', ['$scope', '$cookies', '$rootScope', '$state', '$http', 'toaster', 'msg', 'MapFactory',
  function($scope, $cookies, $rootScope, $state, $http, toaster, msg, MapFactory) {
    $scope.photos = [];
    $scope.maxSeverity = [1, 2, 3, 4, 5];
    $scope.comments = [];
    $scope.msg = msg;
    $http({
      'method': 'GET',
      'url': '/api/problem_detailed_info/' + $state.params['id']
    }).then(function successCallback(response) {
      $scope.selectProblem = response.data[0][0];
      $scope.isSubscripted = response.data[0][0]['is_subscripted'];	
      $scope.photos = response.data[2];
      $scope.comments = response.data[3];
      MapFactory.setCenter(new google.maps.LatLng($scope.selectProblem.latitude, $scope.selectProblem.longitude), 15);
    	if($scope.isSubscripted === false) {
				$scope.cls_eye_subs = "fa fa-eye-slash";
			} else $scope.cls_eye_subs = "fa fa-eye";	
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
    };

    $scope.getMinPhoto = function(url){
      var parts = url.split('.');
      var min_url = parts[0] + '.min.' + parts[1];
      return min_url;
    };
    $scope.changeUser = false;
    
$scope.change = function(value){
          $scope.changeUser = value;
    $scope.post_comment = function(comment) {
      if (comment) {
          $http({
            method: 'POST',
            url: '/api/problem/add_comment',
            data: {
              content: comment.text,
              problem_id: $state.params['id'],
              parent_id: '0',
              anonim: $scope.changeUser
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
          }, function errorCallback(response) {
            if (response.status===405) {
              $scope.msg.addCommentAnonimError('коммента');
            } else {
              $scope.msg.addCommentError('коммента');
            }
          });
      } else {
        return;
      }
    }
  }

    $scope.post_subcomment = function(subcomment, comment) {
      if (subcomment) {
        $http({
          method: 'POST',
          url: '/api/problem/add_comment',
          data: {
            content: subcomment.text,
            problem_id: $state.params['id'],
            parent_id: comment.id
          }
        }).then(function successCallback() {
          $scope.msg.addCommentSuccess('коментаря ');
          $http({
            method: 'GET',
            url: '/api/problem_subcomments/' + comment.id
          }).then(function successCallback(response) {
            $scope.subcomments = response.data[0];
            subcomment.text = '';
            comment.sub_count = response.data[1];
          })
        }, function errorCallback(response) {
          if (response.status===405) {
            $scope.msg.addCommentAnonimError('коментаря ');
          } else {
            $scope.msg.addCommentError('коментаря ');
          }
        });
      } else {
        return;
      }
    }

    $scope.showSubComments = false;
    $scope.getSubComments = function (parent_id) {
      $http({
        method: 'GET',
        url: '/api/problem_subcomments/' + parent_id
      }).then(function successCallback(response) {
        $scope.subcomments = response.data[0];
      })
      if(!$scope.subcomment_parent || $scope.subcomment_parent === parent_id) {
        $scope.showSubComments = $scope.showSubComments ? false: true;
      }
      if($scope.showSubComments === false && $scope.subcomment_parent !== parent_id) {
        $scope.showSubComments = true;
      }
      $scope.subcomment_parent = parent_id;
    }
    
    $scope.colBs = 'col-lg-8';
    $scope.hideIconSubsc = true;
    if ($cookies.get('role')=='admin' || $cookies.get('role')=='user') {
      $scope.colBs = 'col-lg-4';
      $scope.hideIconSubsc = false;
    }
    
    $scope.cls_eye_subs = "fa fa-eye-slash";

    $scope.chgEyeSubsc = function(){
      if ($scope.cls_eye_subs === "fa fa-eye-slash"){
        $http({
          method: 'POST',
          url: '/api/subscription_post',
          data: {
            'problem_id': $state.params['id']
          }
        }).then(function successCallback(response) {
          $scope.cls_eye_subs = "fa fa-eye";
          $scope.msg.createSuccess('підписки');
        })        
      } else if ($scope.cls_eye_subs = "fa fa-eye") {
        $http({
          method: 'DELETE',
          url: '/api/subscription_delete',
          params: {
            problem_id: $state.params['id']
          }
        }).then(function successCallback(response) {
          $scope.cls_eye_subs = "fa fa-eye-slash";
          $scope.msg.deleteSuccess('підписки');
        })          
      }
    };
  }
]);








