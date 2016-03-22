app.controller('DetailedFaqCtrl', ['$scope', '$stateParams', '$state', '$http', '$rootScope',
  function($scope, $stateParams, $state, $http, $rootScope) {
    $http({
      url: '/api/resources/' + $stateParams.faqAlias,
      method: 'GET'
    }).then(function successCallback(responce) {
      $scope.faqInfo = responce.data[0];
      $rootScope.metadata = function(){
      metaTags = {
        'title':  $scope.faqInfo.title,
        'description': $scope.faqInfo.description
      }
      return metaTags;
    }
    }, function errorCallback() {
      $state.go('error404');
    });
  }
]);