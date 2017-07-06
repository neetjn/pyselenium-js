export default {
  template: require('angularjs-template-loader!@/components/author-tile/author-tile.html'),
  bindings: {
    author: '='
  },
  controllerAs: 'ctrl',
  controller: ['$scope', function($scope) {
    $scope.date = new Date()
  }]
}