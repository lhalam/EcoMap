app.controller('AddFaqCtrl', ['$scope', '$state', '$http', 'toaster', '$timeout', '$rootScope',
  function($scope, $state, $http, toaster, $timeout, $rootScope) {
    $rootScope.metadata = function(){
      metaTags = {
        'title': "Екологічні проблеми України",
        'description': 'Створення інструкції'
      }
      return metaTags;
    }
    $scope.page = {
      'description': '',
      'meta_keywords': '',
      'meta_description': ''
    };
    $scope.addPage = function(newPage, form) {
      $scope.submitted = true;
      if (form.$invalid) {
        return;
      }
      newPage['is_enabled'] = 1;
      $http({
        method: 'POST',
        url: '/api/addResource',
        data: newPage
      }).then(function successCallback(response) {
        toaster.pop('success', 'Інструкцію додано', 'Інструкцію було успішно додано!');
        $state.go('user_profile.faq');
      }, function errorCallback() {
        toaster.pop('error', 'Помилка при додаванні', 'При спробі створення нової інструкції виникла помилка!');
      })
    };
  }
]);
