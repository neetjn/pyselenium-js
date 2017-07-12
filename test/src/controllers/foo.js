export default ['$scope', function($scope) {

  $scope.clicked = 0

  $scope.incrementClicked = function() {
    $scope.clicked++
    console.log('Incremented!')
  }

}]
