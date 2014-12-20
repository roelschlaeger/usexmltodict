angular.module('eggly_app', []).
controller('controller', ['$scope', function($scope)
{
    // var wpts = test.gpx.wpt;
    // console.log(wpts.length);
    $scope.wpts = test.gpx.wpt;
    // console.log($scope.wpts.length);
}]);
