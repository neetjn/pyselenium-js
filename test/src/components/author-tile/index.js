import controller from '@/components/author-tile/controller.js'

export default {
  template: require('angularjs-template-loader!@/components/author-tile/author-tile.html'),
  bindings: {
    author: '='
  },
  controllerAs: 'ctrl',
  controller
}