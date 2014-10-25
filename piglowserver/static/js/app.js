var pgApp = angular.module('pgApp',[]);


function PgController($scope, $http) {

    $scope.setLed = function(led, brightness) {

        var url = 'http://192.168.2.124:5000' + '/leds/' + led;
        console.log(url);
        var data = {'brightness': brightness};
       $http.put(url, data, null)
            .success(function (data, status, headers, config) {
                $scope.alerts.push({type: 'success', msg: data.message});
            })
            .error(function (data, status, headers, config) {
                console.log('ERROR:' + data);
                $scope.alerts.push({type: 'danger', msg: data.message});
                })
    };

    $scope.clear = function() {

        var url = 'http://192.168.2.124:5000' + '/patterns/clear';
        console.log(url);
        $http.put(url, {}, null)
            .success(function (data, status, headers, config) {
                $scope.alerts.push({type: 'success', msg: data.message});
            })
            .error(function (data, status, headers, config) {
                console.log('ERROR:' + data);
                $scope.alerts.push({type: 'danger', msg: data.message});
                })
    };
    var led_list = [];
    for (var i=1; i<=18; i++) {
        led_list.push(i);
    }

    $scope.led_list = led_list;
    $scope.alerts = [];
}