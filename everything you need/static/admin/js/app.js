'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
    'ngRoute',
    'ngCookies',
    'lr.upload',
    'ngSanitize',
    'ngTagEditor',
    'loginControllers',
    'articleControllers',
    'listControllers'
]).
config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/login', {
            templateUrl: 'partials/login.html',
            controller: 'LoginCtrl'
        });
        $routeProvider.when('/create', {
            templateUrl: 'partials/create.html',
            controller: 'CreateCtrl'
        });
        $routeProvider.when('/list', {
            templateUrl: 'partials/list.html',
            controller: 'ListCtrl'
        });
        $routeProvider.when('/view/:title', {
            templateUrl: 'partials/view.html',
            controller: 'ViewCtrl'
        });
        $routeProvider.when('/edit/:title', {
            templateUrl: 'partials/edit.html',
            controller: 'EditCtrl'
        });
        $routeProvider.otherwise({
            redirectTo: '/login'
        });
    }
]);

// var loginUrl = "http://localhost:5000/login"
var loginUrl = "http://54.149.235.253:4000/login"
var url = 'http://54.149.235.253:4000';
// var url = 'http://localhost:5000'