angular.module('eggly_app', []).
controller('controller', ['$scope', function($scope)
{
    $scope.wpts = test.gpx.wpt;
    $scope.show_wpts = angular.toJson($scope.wpts[8],1);
}]);
