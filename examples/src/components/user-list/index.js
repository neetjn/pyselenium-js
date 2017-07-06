export default {
  template: require('angularjs-template-loader!@/components/user-list/user-list.html'),
  bindings: {
    users: '='
  },
  controllerAs: 'ctrl',
  controller: ['$scope', function($scope) {
  }]
}