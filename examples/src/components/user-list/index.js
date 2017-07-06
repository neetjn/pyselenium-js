export default {
  template: require('angularjs-template-loader!@/components/user-list/user-list.html'),
  bindings: {
    users: '='
  },
  controllerAs: 'ctrl',
  controller: require('@/components/user-list/controller.js')
}