app.controller('UserProfileCtrl', ['$scope', '$cookies', '$http', 'toaster', 'Upload', '$timeout',
    function($scope, $cookies, $http, toaster, Upload, $timeout){

  $scope.user = {};
  $scope.user.id = $cookies.get("id");

  $scope.body = angular.element(document.body);
  $scope.body.addClass("body-scroll-shown");

  if($scope.user.id){
      $http({
        url: '/api/user_detailed_info/' + $scope.user.id,
        method: 'GET'
      }).success(function(response){
        $scope.user.data = response;
      });
  }

  $scope.selectedTab = "userInfo";
  $scope.setTab = function(tabName){
    $scope.selectedTab = tabName;
  };
  $scope.isSelected = function(tabName){
    return $scope.selectedTab == tabName;
  };

  console.log($scope);
  $scope.changePassword = function(){
    var data = {};
    data.id = $cookies.get('id');
    data.old_pass = $scope.password.old_pass;
    data.new_pass = $scope.password.new_pass;
    console.log(data);
    $http({
        method: 'POST',
        url: '/api/change_password',
        data: data
    }).then(function successCallback(responce){
        $scope.password = {};
        toaster.pop('success', 'Пароль', 'Пароль було успішно змінено!');
        $scope.changePasswordForm.$setUntouched();
    },
      function errorCallback(responce){
        if(responce.status == 401){
          $scope.wrongOldPass = true;
        }
      });
  };

  $scope.wrongOldPass = false;
  $scope.getWrongPass = function(){
    return $scope.wrongOldPass;
  };
  $scope.changeWrongPass = function(){
    $scope.wrongOldPass = false;
  };

  $scope.alert = false;
  $scope.closeAlert = function() {
    $scope.alert = false;
  };
  $scope.showAlert = function(){
    return $scope.alert;
  };

  $scope.$on("$destroy", function handler() {
    $scope.body.removeClass("body-scroll-shown");
  });


      $scope.reloadImg = function (imgUrl) {
  $scope.user.data.avatar = imgUrl + '?=new_' + new Date().getTime();
      return $scope.user.data.avatar;
  //
  };

      $scope.photo = false;
      $scope.showModalPhoto = function(){
          $scope.photo = true
      };

 $scope.cancelImg = function(){
     $scope.photo = false;
     $scope.newImage = '';
     $scope.picFile = ''
      };


 $scope.upload = function (dataUrl, picFile) {
        Upload.upload({
            url: '/api/upload_avatar',
            cache: false,
            data: {
                file: Upload.dataUrltoBlob(dataUrl), name: picFile.name
            }
        }).then(function (response) {
            $timeout(function () {
                $scope.result = response.data;
                $scope.reloadImg($scope.result.added_file);
                $scope.photo = false
            });
        }, function (response) {
            if (response.status > 0) $scope.errorMsg = response.status
                + ': ' + response.data.error;
        }, function (evt) {
            $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
        });
    };

}]);




