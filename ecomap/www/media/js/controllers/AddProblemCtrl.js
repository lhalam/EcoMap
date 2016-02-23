app.controller('AddProblemCtrl', ['$scope', '$state', '$http', 'toaster', 'Upload', '$timeout', 'uiGmapIsReady', '$rootScope', 'MapFactory',
  function($scope, $state, $http, toaster, Upload, $timeout, uiGmapIsReady, $rootScope, MapFactory) {
    $scope.pattern = {
      'coords': /^[-]{0,1}[0-9]{0,3}[.]{1}[0-9]{0,20}$/
    };
    MapFactory.getInst().addListener('click', function(event) {
        var lat = event.latLng.lat();
        var lon = event.latLng.lng();
        $scope.newProblem.latitude = lat;
        $scope.newProblem.longitude = lon;
        $scope.latlng = latlng;
        var latlng = new google.maps.LatLng(lat, lon);
        if (!$scope.marker) {
          $scope.createMarker()
        }
        $scope.marker.setPosition(latlng);
        $scope.$apply();
      })
    $scope.newProblem = {
      'title': '',
      'type': '',
      'latitude': '',
      'longitude': '',
      'content': '',
      'proposal': ''
    };
    $scope.problemTypes = [];
      $scope.loadProblemType = function() {
      $http({
        method: 'GET',
        url: '/api/problem_type',
      }).then(function successCallback(data) {
         for (var i = 0; i < data.data.length; i++){
          $scope.problemTypes.push(data.data[i]);
          $scope.problemTypes[i]['picture'] = '/image/markers/' + $scope.problemTypes[i]['picture'] ;
      }
      }, function errorCallback(response) {})
    };
    $scope.loadProblemType();
    $scope.validationStatus = 0;
    $scope.createdProblemId = 0;
    $scope.createMarker = function(position) {
      $scope.options = {
        scrollwheel: true
      };
      $scope.coordsUpdates = 0;
      $scope.dynamicMoveCtr = 0;
      $scope.marker = new google.maps.Marker({
        position: {
          lat: $scope.newProblem.latitude,
          lng: $scope.newProblem.longitude
        },
        map: MapFactory.getInst(),
        id: Date.now(),
        options: {
          draggable: true,
          labelContent: 'ваше місцезнаходження',
          labelAnchor: '65 0',
          labelClass: 'marker-labels',
          icon: 'http://www.sccmod.org/wp-content/uploads/2014/11/mod-map-marker1.png'
        },
      })
      $scope.marker.addListener('drag', function(event) {
          $scope.newProblem.latitude = this.getPosition().lat();
          $scope.newProblem.longitude = this.getPosition().lng();
          $scope.$apply();
        })
      $scope.$watch($scope.newProblem, function(newVal, oldVal) {
        if (_.isEqual(newVal, oldVal)) {
          return;
        }
        $scope.coordsUpdates++;
      });
    };
    $scope.reloadPos = function() {
      var latlng = new google.maps.LatLng($scope.newProblem.latitude, $scope.newProblem.longitude);
      MapFactory.setCenter(latlng, 14);
      if (!$scope.marker) {
        $scope.createMarker();
      }
      $scope.marker.setPosition(latlng)
    };
    var options = {
      enableHighAccuracy: true,
      timeout: 3000,
      maximumAge: 0
    };

    function error(err) {
      console.warn('ERROR(' + err.code + '): ' + err.message);
    }
    $scope.locateUser = function() {
      navigator.geolocation.getCurrentPosition(getUserPosition, error, options);
      var width = window.innerWidth;

      function getUserPosition(position) {
        $scope.newProblem.latitude = position.coords.latitude;
        $scope.newProblem.longitude = position.coords.longitude;
        var mapCenter = new google.maps.LatLng($scope.newProblem.latitude, $scope.newProblem.longitude);
        if (width < 1000) {
          MapFactory.setCenter(mapCenter, 10);
        } else {
          MapFactory.setCenter(mapCenter, 14);
        }
        $scope.$apply();
        if (!$scope.marker) {
          $scope.createMarker()
        }
        var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        $scope.marker.setPosition(latlng)
      }
    };
    /*End of map & markers section*/
    /*Problem posting section*/
    $scope.addProblemTab = true;
    $scope.addPhotosTab = false;
    $scope.goToPhotos = function(form) {
      if (!form.$invalid) {
        $scope.addProblemTab = false;
        $scope.addPhotosTab = true;
      }
    };
    $scope.goToProblems = function() {
      $scope.addProblemTab = true;
      $scope.addPhotosTab = false;
    };
    $scope.addProblem = function(newProblem, form, photos) {
      $scope.submitted = true;
      if (form.$invalid) {
        toaster.pop('error', 'Помилка при додаванні', 'Форма не відповідає вимогам!')
        return;
      }
      Upload.upload({
        url: '/api/problem_post',
        method: 'POST',
        cache: false,
        headers: {
          'Cache-Control': 'no-cache'
        },
        data: newProblem
      }).then(function successCallback(response) {
        toaster.pop('success', 'Додавання проблеми', 'Проблему було успішно додано!');
        $scope.createdProblemId = response.data.problem_id;
        $scope.arrayUpload(photos);
        $rootScope.mapParams = {
          center: {
            latitude: newProblem.latitude,
            longitude: newProblem.longitude
          },
          zoom: 14
        };
      }, function errorCallback() {
        toaster.pop('error', 'Помилка при додаванні', 'При спробі додавання проблеми виникла помилка!');
      })
    };
    /*End of problem posting section*/
    /*Photos section*/
    $scope.photos = [];
    $scope.check = function(formFile) {
      $scope.validationStatus = 0;
      if (formFile.$error.maxSize) {
        return toaster.pop('error', 'Фото профілю', 'Розмір фото перевищує максимально допустимий!');
      } else if (formFile.$error.pattern) {
        return toaster.pop('error', 'Фото профілю', 'Оберіть зображення в форматі .jpg або .png!');
      } else {
        $scope.validationStatus = 1;
        return 'valid'
      }
    };
    $scope.removePhoto = function(photo, photos) {
      var index = photos.indexOf(photo);
      photos.splice(index, 1);
      toaster.pop('warning', 'Фото', 'Фото видалено');
    };
    $scope.arrayUpload = function(photos) {
      angular.forEach(photos, function(value, key) {
        $scope.uploadPic(value);
      });
      $state.go('map');
    };
    $scope.uploadPic = function(file) {
      file.upload = Upload.upload({
        url: '/api/photo/' + $scope.createdProblemId,
        method: 'POST',
        cache: false,
        headers: {
          'Cache-Control': 'no-cache'
        },
        data: {
          file: file,
          name: file.name,
          description: file.description || ''
        }
      });
      file.upload.then(function(response) {
        $timeout(function() {
          file.result = response.data;
          toaster.pop('success', 'Фото', 'Фото було успішно додано!');
        });
      }, function(response) {
        if (response.status >= 400) toaster.pop('error', 'помилка', 'помилка завантаження фото');
      }, function(evt) {
        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
      });
    };
    /*End of photos section*/
    uiGmapIsReady.promise().then(function(instances) {
      var maps = instances[0].map;
      google.maps.event.trigger(maps, 'resize');
    });
  }
]);
