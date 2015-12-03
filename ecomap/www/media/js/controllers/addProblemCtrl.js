app.controller('addProblemCtrl', ['$scope', '$state', '$http', 'toaster', 'Upload',
    '$timeout', 'uiGmapIsReady',
    function($scope, $state, $http, toaster, Upload, $timeout, uiGmapIsReady) {

    $scope.mapParams = { center: { latitude: 49.357826, longitude: 31.518239 }, zoom: 6 };
    $scope.getMapParams = function(){
        return $scope.mapParams;
    };

    $scope.pattern = {
      'coords': /^[-]{0,1}[0-9]{0,3}[.]{1}[0-9]{0,20}$/
    };

    $scope.zoomMarker = function(data){
        console.log(data);
        $scope.mapParams = {
            center: { latitude: data.model.latitude,
                      longitude: data.model.longitude },
            zoom: 17
        }
    };

    $scope.markers = [];
    $scope.loadProblems = function(){
        $http({
            method: 'GET',
            url: '/api/problems'
        }).then(function successCallback(response){
            $scope.markers = response.data;
            //console.log($scope.markers);
            //console.log($scope.markers[0]);
            angular.forEach($scope.markers, function(value, key){
                $scope.markers[key].iconUrl = "/image/markers/" + value.problem_type_Id + ".png";
            });
        }, function errorCallback(error){});
    };
    $scope.loadProblems();


//FORM for ADDING PROBLEMS

    $scope.map = {
        events: {
            click: function (map, eventName, originalEventArgs) {
                var e = originalEventArgs[0];
                var lat = e.latLng.lat(),lon = e.latLng.lng();
                $scope.newProblem.latitude = lat;
                $scope.newProblem.longitude = lon;
                $scope.$apply();
            }
        }
    };

    $scope.newProblem = {
    "title": "",
    "type": "",
    "latitude": "",
    "longitude": "",
    "content": "",
    "proposal":""
    };


    $scope.validationStatus = 0;
    $scope.createdProblemId = 0;

    $scope.marker = {id: Date.now(),
        coords: {
            latitude: $scope.newProblem.latitude,
            longitude: $scope.newProblem.longitude
        }
    };
    $scope.problemTypes =
        [
            {name: 'Проблеми лісів', id: 1},
            {name: 'Сміттєзвалища', id: 2},
            {name: 'Незаконна забудова', id: 3},
            {name: 'Проблеми водойм', id: 4},
            {name: 'Загрози біорізноманіттю', id: 5},
            {name: 'Браконьєрство', id: 6},
            {name: 'Інші проблеми', id: 7}
        ];

    $scope.createMarker = function(position){
        console.info('created');

        $scope.options = {scrollwheel: true};
        $scope.coordsUpdates = 0;
        $scope.dynamicMoveCtr = 0;

        $scope.marker = {
            id: Date.now(),
            coords: {
                latitude: $scope.newProblem.latitude,
                longitude: $scope.newProblem.longitude
            },
            options: {
            draggable: true,
            labelContent: 'ваше місцезнаходження',
            labelAnchor: "65 0",
            labelClass: "marker-labels",
            icon:'http://www.sccmod.org/wp-content/uploads/2014/11/mod-map-marker1.png'},
            events: {
                drag: function (marker, eventName, args) {
                    console.log('marker dragend');

                    $scope.newProblem.latitude = marker.getPosition().lat();
                    $scope.newProblem.longitude =  marker.getPosition().lng();

                    $scope.marker.options = {
                        draggable: true,
                        labelContent: 'location',
                        labelAnchor: "20 0",
                        labelClass: "marker-labels",
                        icon:'https://2ip.com.ua/images/marker_map.png'
                    }
                }
            }
        };

        $scope.$watchCollection("marker.coords", function (newVal, oldVal) {
            if (_.isEqual(newVal, oldVal)) {
                return;
            }
            $scope.coordsUpdates++;
        });
    };

    $scope.reloadPos = function(){
        $scope.mapParams ={ center: {latitude: $scope.newProblem.latitude,
                                     longitude: $scope.newProblem.longitude }, zoom: 7 };
        $scope.createMarker();       
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
            
            mapCenter = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            $scope.newProblem.latitude = position.coords.latitude;
            $scope.newProblem.longitude = position.coords.longitude;

            if (width < 1000) {
                $scope.mapParams ={ center: mapCenter, zoom: 10 };
            } else {
                $scope.mapParams ={ center: mapCenter, zoom: 17 };
            }
            $scope.$apply();
            $scope.createMarker()
        }

    };

    $scope.addProblem = function(newProblem, form, photos) {
        $scope.submitted = true;

        if(form.$invalid){
            return;
        }
        console.log(newProblem);
        Upload.upload({
            url: '/api/problem_post',
            method: "POST",
            cache: false,
            headers: {
                'Cache-Control': 'no-cache'
            },
            data: newProblem

        }).then(function successCallback(response) {
                toaster.pop('success', 'Оповіщення', 'Оповіщення про проблему' +
                    ' було успішно додано!');
                $scope.createdProblemId = response.data.problem_id;
                toaster.pop('info', 'Фото', 'Додайте фотографіі до' +
                    ' вашого оповіщення!');
                //$scope.arrayUpload($scope.photos,  $scope.createdProblemId )
            }, function errorCallback() {
                toaster.pop('error', 'Помилка при додаванні', 'При спробі' +
                    ' додавання проблеми виникла помилка!');
            })
    };


    //PHOTOS CTRL

    $scope.photos = [];
    $scope.check = function(formFile) {
    $scope.validationStatus = 0;

    //$scope.arrayValidation = {
    //  'len':$scope.photos.length,
    //  'totalSize':0
    //};

    if (formFile.$error.maxSize) {
      return toaster.pop('error', 'Фото профілю', 'Розмір фото перевищує максимально допустимий!');
    } else if (formFile.$error.pattern) {
      return toaster.pop('error', 'Фото профілю', 'Оберіть зображення в форматі .jpg або .png!');
    } else {
      $scope.validationStatus = 1;
      return 'valid'
    }
  };


  $scope.removePhoto = function(photo, photos){
    var index = photos.indexOf(photo);
    photos.splice(index, 1);
    toaster.pop('warning', 'Фото', 'Фото видалено');
  };

  $scope.arrayUpload = function (photos) {
    console.log(photos);
    angular.forEach(photos, $scope.uploadPic);
    console.log(photos);
      $state.go('map');
  };

  $scope.uploadPic = function(file) {
    file.upload = Upload.upload({
      url: '/api/photo/' + $scope.createdProblemId,
      method: "POST",
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

    file.upload.then(function (response) {
      $timeout(function () {
        file.result = response.data;
        toaster.pop('success', 'Фото', 'Фото було успішно додано!');
      });
    }, function (response) {
      if (response.status >= 400)
        toaster.pop('error', 'помилка', 'помилка завантаження фото');
        //$scope.errorMsg = response.status + ': ' + response.data;
    }, function (evt) {
      // Math.min is to fix IE which reports 200% sometimes
      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
    });
    };
    uiGmapIsReady.promise().then(function(instances) {
        var maps = instances[0].map;
        google.maps.event.trigger(maps, 'resize');
    });
}]);
