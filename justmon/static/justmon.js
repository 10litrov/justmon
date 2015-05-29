"use strict";

angular.module('justmon', ['ngMaterial'])
    .constant('moment', moment)

    .config(['$mdThemingProvider', '$mdIconProvider', function ($mdThemingProvider, $mdIconProvider) {
        $mdThemingProvider.theme('default');

        $mdIconProvider
            .icon('smile', 'img/smile.svg')
            .icon('sad', 'img/sad.svg');
    }])

    .factory('Data', ['$http', '$interval', function ($http, $interval) {
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

    .filter('momentCalendar', ['moment', function (moment) {
        return function (input) {
            return moment.unix(input).calendar()
        }
    }])

    .controller('StatusCtrl', ['$scope', 'Data', function ($scope, Data) {
        $scope.data = Data;
    }])
;