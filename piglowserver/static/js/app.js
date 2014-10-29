var pgApp = angular.module('pgApp',['ui.bootstrap']);


function PgController($scope, $http) {

    var color_list = ["red", "orange", "yellow", "green", "blue", "white"]
    var led_list = [];
    var color = 0;
    for (i=1; i<=18; i++) {
        led = {"number": i,
               "arm": Math.ceil(i/6),
               "color": color_list[color],
           }
        led_list.push(led);
        color++;
        if (color>=6) color=0;
        console.log(i + ' ' + i%6 + ' ' + Math.ceil(i/6));
    }
    $scope.color_list = color_list;
    $scope.led_list = led_list;

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

    $scope.setArm = function(arm, brightness) {


        var url = 'http://192.168.2.124:5000' + '/arms/' + arm;
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

    $scope.alerts = [];

}