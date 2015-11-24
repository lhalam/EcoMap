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
        $scope.user.data.avatar = $scope.user.data.avatar || 'http://placehold.it/150x150';
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


    // User Change Avatar
    $scope.reloadImg = function (imgUrl) {
        $scope.user.data.avatar = imgUrl + '?=new_' + new Date().getTime();
        return $scope.user.data.avatar;
    };

    $scope.photo = false;
    $scope.result = '';
    $scope.showModalPhoto = function(){
          $scope.photo = true
    };

    $scope.showStatus = true;
    $scope.uploadButtuon = false;
    $scope.deleteButtuon = true;

    $scope.cancelImg = function(picFile){
        $scope.photo = false;
        $scope.showStatus = false;
        $scope.uploadButtuon = false;
        $scope.result = '';
        picFile = null;
        $scope.picFile = null;
        return $scope.picFile = null;
      };

    $scope.showUploadButton = function(){
        $scope.uploadButtuon = true;
        $scope.deleteButtuon = false;
    };

    $scope.showCanvas = function(formFile){

        $scope.showStatus = true;
        $scope.uploadButtuon = true;
        //alert($scope.uploadPhoto.file.$error.maxSize)
        var uploadForm = angular.element(document.getElementsByName('uploadPhoto'))[0];
        //console.log(uploadForm.file.error)

        if (formFile.$error.maxSize){
            //alert(formFile)
            //console.log(formFile)
            console.log(formFile.$error);
            toaster.pop('error', 'Фото профілю', 'Розмір фото перевищує максимально допустимий!');
            //console.log(formFile.$error.maxSize)
            //alert(formFile.$error.maxSize)
        }

        //alert(uploadPhoto.file.$error)
        //console.log(uploadPhoto.file.$error)
        //console.log(uploadPhoto.file.$error.maxSize)
        //alert(uploadForm.file.error)

};



        $scope.setDefaultPhoto = function () {
            $scope.user.data.avatar = 'http://placehold.it/150x150';
            $scope.deletePhoto($scope.user.id);
        return $scope.user.data.avatar;
        };

  $scope.clearCanvas = function(picFile){
     var cnv = angular.element(document.getElementsByTagName('canvas'));
      var uploadForm = angular.element(document.getElementsByName('uploadPhoto'))[0];
      var cnv2 = cnv[0];
      var ctx = cnv2.getContext('2d');
      ctx.clearRect(0, 0, cnv2.width, cnv2.height);
      $scope.showStatus = false;
      $scope.uploadButtuon = false;
      $scope.result = '';
      console.log(picFile);
      uploadForm.file = null;
      picFile = null;
      return ctx.clearRect(0, 0, cnv2.width, cnv2.height);

  };

 $scope.upload = function (dataUrl, picFile) {
        Upload.upload({
            url: '/api/user_avatar',
            method:"POST",
            cache: false,
            headers: { 'Cache-Control' : 'no-cache' } ,
            data: {
                file: Upload.dataUrltoBlob(dataUrl), name: picFile.name
            }
        }).then(function (response, picFile) {
            $timeout(function () {
                $scope.result = response.data;
                $scope.reloadImg($scope.result.added_file);
                $scope.photo = false;
                $scope.file = false;
                var cnv = angular.element(document.getElementsByTagName('canvas'));
                var cnv2 = cnv[0];
                var ctx = cnv2.getContext('2d');
                ctx.clearRect(0, 0, cnv2.width, cnv2.height);
                $scope.cancelImg(picFile);
                $scope.clearCanvas(picFile);
                picFile = null;
                toaster.pop('success', 'Фото профілю', 'Фото було успішно змінено!');
            });
        }, function (response) {
            if (response.status > 0) $scope.errorMsg = response.status
                + ': ' + response.data.error;
            toaster.pop('error', 'Фото профілю', 'Виникла помилка при завантаженні фото');
            if (response.status == 403){
                toaster.pop('error', 'Немає доступу', 'Дія заборонена адміністратором!');
            }
        }, function (evt) {
            $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
        });
    };


    $scope.deletePhoto = function(id){
        $http({
          method:"DELETE",
          headers: {"Content-Type": "application/json;charset=utf-8"},
          url:"/api/user_avatar",
          data:{
            "user_id":id
          }
        }).then(function successCallback(data) {
            if(data){
                toaster.pop('info', 'Фото', 'Фото профілю видалено!');
                }
            else { toaster.pop('error', 'Фото', 'Виникла помилка!');
                }
        }, function errorCallback(response) {
            console.log(response)
        })
   	};



}]);




