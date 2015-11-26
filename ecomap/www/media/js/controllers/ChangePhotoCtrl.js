app.controller('ChangePhotoCtrl', ['$scope', '$cookies', '$http', 'toaster', 'Upload', '$timeout',
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

    $scope.cancelImg = function(){
        $scope.photo = false;
        $scope.showStatus = false;
        $scope.uploadButtuon = false;
        $scope.result = '';
        return $scope.showStatus = false;
      };

    $scope.showUploadButton = function(){
    $scope.uploadButtuon = true
    };

    $scope.showCanvas = function(){
     $scope.showStatus = true;
        $scope.uploadButtuon = true;
      };

  $scope.clearCanvas = function(picFile){
     var cnv = angular.element(document.getElementsByTagName('canvas'));
      var cnv2 = cnv[0];
      var ctx = cnv2.getContext('2d');
      ctx.clearRect(0, 0, cnv2.width, cnv2.height);
      $scope.showStatus = false;
      $scope.uploadButtuon = false;
      $scope.result = '';
      console.log(picFile);
      return ctx.clearRect(0, 0, cnv2.width, cnv2.height);
  };



 $scope.upload = function (dataUrl, picFile) {
        Upload.upload({
            url: '/api/upload_avatar',
            cache: false,
            headers: { 'Cache-Control' : 'no-cache' } ,
            data: {
                file: Upload.dataUrltoBlob(dataUrl), name: picFile.name
            }
        }).then(function (response) {
            $timeout(function () {
                $scope.result = response.data;
                $scope.reloadImg($scope.result.added_file);
                $scope.photo = false;
                $scope.file = false;
                var cnv = angular.element(document.getElementsByTagName('canvas'));
                var cnv2 = cnv[0];
                var ctx = cnv2.getContext('2d');
                ctx.clearRect(0, 0, cnv2.width, cnv2.height);
            });
        }, function (response) {
            if (response.status > 0) $scope.errorMsg = response.status
                + ': ' + response.data.error;
        }, function (evt) {
            $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
        });
    };
  //$scope.photo = false;


}]);