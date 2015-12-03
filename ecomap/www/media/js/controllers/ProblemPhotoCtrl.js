//
//app.controller('ProblemPhotoCtrl', ['$scope', '$cookies', '$http',
//    'toaster', 'Upload', '$timeout', 'uiGmapIsReady',
//function($scope, $cookies, $http, toaster, Upload, $timeout, uiGmapIsReady) {
//
//  //$scope.reloadImg = function(imgUrl) {
//  //  $scope.user.data.avatar = imgUrl + '?=new_' + new Date().getTime();
//  //  return $scope.user.data.avatar;
//  //};
//  //
//  //$scope.photo = false;
//  //$scope.result = '';
//  //$scope.showModalPhoto = function() {
//  //  $scope.photo = true
//  //};
//  //
//  //$scope.showStatus = true;
//  //$scope.uploadButton = false;
//  //$scope.deleteButton = true;
//  //$scope.cancelImg = function(picFile) {
//  //  $scope.photo = false;
//  //  $scope.showStatus = false;
//  //  $scope.uploadButton = false;
//  //  $scope.result = '';
//  //  picFile = null;
//  //  $scope.picFile = null;
//  //  return $scope.picFile = null;
//  //};
//  //
//  //$scope.showUploadButton = function() {
//  //  $scope.uploadButton = true;
//  //  $scope.deleteButton = false;
//  //};
//  //
//  //$scope.check = function(formFile) {
//  //  if (formFile.$error.maxSize) {
//  //    return toaster.pop('error', 'Фото профілю', 'Розмір фото перевищує максимально допустимий!');
//  //  } else if (formFile.$error.pattern) {
//  //    return toaster.pop('error', 'Фото профілю', 'Оберіть зображення в форматі .jpg або .png!');
//  //  } else {
//  //    return 'valid'
//  //  }
//  //};
//  //
//  //$scope.showCanvas = function(formFile) {
//  //  $scope.uploadButton = false;
//  //  $scope.showStatus = false;
//  //  if ($scope.check(formFile) == 'valid') {
//  //    $scope.uploadButton = true;
//  //    $scope.showStatus = true;
//  //  }
//  //};
//  //
//  //$scope.setDefaultPhoto = function() {
//  //  $scope.user.data.avatar = 'http://placehold.it/150x150';
//  //  $scope.deletePhoto($scope.user.id);
//  //  return $scope.user.data.avatar;
//  //};
//  //
//  //$scope.clearCanvas = function(picFile) {
//  //  var cnv = angular.element(document.getElementsByTagName('canvas'));
//  //  var uploadForm = angular.element(document.getElementsByName('uploadPhoto'))[0];
//  //  var cnv2 = cnv[0];
//  //  var ctx = cnv2.getContext('2d');
//  //  ctx.clearRect(0, 0, cnv2.width, cnv2.height);
//  //  $scope.showStatus = false;
//  //  $scope.uploadButton = false;
//  //  $scope.result = '';
//  //  console.log(picFile);
//  //  uploadForm.file = null;
//  //  picFile = null;
//  //  return ctx.clearRect(0, 0, cnv2.width, cnv2.height);
//  //};
//  //
//  //$scope.upload = function(dataUrl, picFile) {
//  //  Upload.upload({
//  //    url: '/api/user_avatar',
//  //    method: "POST",
//  //    cache: false,
//  //    headers: {
//  //      'Cache-Control': 'no-cache'
//  //    },
//  //    data: {
//  //      file: Upload.dataUrltoBlob(dataUrl),
//  //      name: picFile.name
//  //    }
//  //  }).then(function(response, picFile) {
//  //    $timeout(function() {
//  //      $scope.result = response.data;
//  //      $scope.reloadImg($scope.result.added_file);
//  //      $scope.photo = false;
//  //      $scope.file = false;
//  //      var cnv = angular.element(document.getElementsByTagName('canvas'));
//  //      var cnv2 = cnv[0];
//  //      var ctx = cnv2.getContext('2d');
//  //      ctx.clearRect(0, 0, cnv2.width, cnv2.height);
//  //      $scope.cancelImg(picFile);
//  //      $scope.clearCanvas(picFile);
//  //      picFile = null;
//  //      toaster.pop('success', 'Фото профілю', 'Фото було успішно змінено!');
//  //    });
//  //  }, function(response) {
//  //    if (response.status > 0) $scope.errorMsg = response.status + ': ' + response.data.error;
//  //    toaster.pop('error', 'Фото профілю', 'Виникла помилка при завантаженні фото');
//  //    if (response.status == 403) {
//  //      toaster.pop('error', 'Немає доступу', 'Дія заборонена адміністратором!');
//  //    }
//  //  }, function(evt) {
//  //    $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
//  //  });
//  //};
//  //
//  //$scope.deletePhoto = function(id) {
//  //  $http({
//  //    method: "DELETE",
//  //    headers: {
//  //      "Content-Type": "application/json;charset=utf-8"
//  //    },
//  //    url: "/api/user_avatar",
//  //    data: {
//  //      "user_id": id
//  //    }
//  //  }).then(function successCallback(data) {
//  //    if (data) {
//  //      toaster.pop('info', 'Фото', 'Фото профілю видалено!');
//  //    } else {
//  //      toaster.pop('error', 'Фото', 'Виникла помилка!');
//  //    }
//  //  }, function errorCallback(response) {
//  //    console.log(response)
//  //  })
//  //};
//
//  $scope.photos = [];
//  $scope.validationStatus = 0;
//  $scope.createdProblemId = 0;
//
//  $scope.check = function(formFile) {
//    $scope.validationStatus = 0;
//    //$scope.arrayValidation = {
//    //  'len':$scope.photos.length,
//    //  'totalSize':0
//    //};
//
//    if (formFile.$error.maxSize) {
//      return toaster.pop('error', 'Фото профілю', 'Розмір фото перевищує максимально допустимий!');
//    } else if (formFile.$error.pattern) {
//      return toaster.pop('error', 'Фото профілю', 'Оберіть зображення в форматі .jpg або .png!');
//    } else {
//      $scope.validationStatus = 1;
//      return 'valid'
//    }
//  };
//
//
//  $scope.removePhoto = function(photo){
//    var index = $scope.photos.indexOf(photo);
//    $scope.photos.splice(index, 1);
//    toaster.pop('warning', 'Фото', 'Фото видалено');
//  };
//
//  $scope.arrayUpload = function (photos) {
//  console.log(photos);
//    angular.forEach(photos, $scope.uploadPic);
//  console.log(photos)
//  };
//
//  //$scope.getCreatedProblemId = function() {
//  //  $http({
//  //    method: 'GET',
//  //    url: 'api/usersProblem/'
//  //  }).then(function successCallback(response) {
//  //    console.log(response);
//  //    $scope.createdProblemId = response.data.id;
//  //  });
//  //};
//
//  $scope.uploadPic = function(file) {
//    console.log(file);
//    console.log(file.description);
//    file.upload = Upload.upload({
//      url: '/api/user_avatar',
//      method: "POST",
//      cache: false,
//      headers: {
//        'Cache-Control': 'no-cache'
//      },
//      data: {
//        file: file,
//        name: file.name,
//        description: file.description
//      }
//    });
//
//    file.upload.then(function (response) {
//      $timeout(function () {
//        file.result = response.data;
//        console.log(response);
//        console.log(response.data);
//        console.log(response.data.last_id);
//        toaster.pop('success', 'Фото', 'Фото було успішно додано!');
//        //$http({
//        //method: "GET",
//        //url: "/api/permissions",
//        //data: {
//        //}
//        //}).then(function successCallback(data) {
//        //$scope.editPermModal = false;
//        //$scope.msg.editSuccess('права');
//        //$scope.loadPerm()
//        //}, function errorCallback(response) {
//        //$scope.msg.editError('права');
//        //})
//        //
//      });
//    }, function (response) {
//      if (response.status >= 400)
//        toaster.pop('error', 'помилка', 'помилка завантаження фото');
//        //$scope.errorMsg = response.status + ': ' + response.data;
//    }, function (evt) {
//      // Math.min is to fix IE which reports 200% sometimes
//      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
//    });
//    }
//
//}]);
