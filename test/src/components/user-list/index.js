import controller from '@/components/user-list/controller.js'

export default {
  template: require('angularjs-template-loader!@/components/user-list/user-list.html'),
  bindings: {
    users: '='
  },
  controllerAs: 'ctrl',
  controller
}