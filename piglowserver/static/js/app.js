/*
    A simple single page app to control a PiGlow board
    http://shop.pimoroni.com/products/piglow
    via the pg_rest_server
    https://github.com/pkshiu/piglowserver
*/
var pgApp = angular.module('pgApp',['ui.bootstrap']);


function PgController($scope, $http) {

    var color_list = ["red", "orange", "yellow", "green", "blue", "white"]
    var led_list = [];
    var color = 0;

    // Compute LED list knowing the configuration of 3 arms
    // of 6 colors
    for (i=1; i<=18; i++) {
        led = {"number": i,
               "arm": Math.ceil(i/6),
               "color": color_list[color],
           }
        led_list.push(led);
        color++;
        if (color>=6) color=0;
    }
    $scope.color_list = color_list;
    $scope.led_list = led_list;

    $scope.setLed = function(led, brightness) {

        var url = $scope.API_SERVER + '/leds/' + led;
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


        var url = $scope.API_SERVER + '/arms/' + arm;
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

        var url = $scope.API_SERVER + '/patterns/clear';
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