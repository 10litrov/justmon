"use strict";

angular.module('justmon', ['ngAnimate', 'ngMaterial'])
    .constant('google', google)

    .config(['$mdThemingProvider', '$mdIconProvider', function ($mdThemingProvider, $mdIconProvider) {
        $mdThemingProvider.theme('default');

        $mdIconProvider
            .icon('smile', 'img/smile.svg')
            .icon('sad', 'img/sad.svg')
            .icon('back', 'img/back.svg');
    }])

    .factory('status', ['$http', '$interval', function ($http, $interval) {
        var data = {
            hosts: [],
            ok: true
        };

        function update() {
            $http.get('/api/hosts').then(function (result) {
                data.hosts = result.data;
                data.ok = data.hosts.filter(function (host) { return !host.status }).length == 0
            })
        }

        update();
        $interval(update, 30000);

        return data;
    }])

    .factory('stats', ['$http', function ($http) {
        return function (host) {
            return $http.get('/api/stats/' + host);
        }
    }])

    .directive('timeline', ['google', 'stats', function (google, stats) {
        return {
            restrict: 'E',
            scope: {
                host: '='
            },
            link: function (scope, element) {
                function render() {
                    var chart = new google.visualization.Timeline(element[0]);
                    var dataTable = new google.visualization.DataTable();
                    chart.draw(dataTable)
                }
                google.load('visualization', '1', {packages:['timeline'], callback: render});
            }
        }
    }])

    .controller('StatusCtrl', ['$scope', 'status', function ($scope, status) {
        $scope.status = status;
    }])
;