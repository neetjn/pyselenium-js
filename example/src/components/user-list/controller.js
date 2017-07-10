export default ['$scope', function($scope) {
  $scope.addUser = function() {
    $scope.ctrl.users.push({
      name: $scope.name || '???',
      field: $scope.field || '???'
    })
  }
  $scope.removeUser = function(user) {
    $scope.ctrl.users.splice(user, 1)
  }
}]
