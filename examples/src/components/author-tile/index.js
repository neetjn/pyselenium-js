export default {
  template: require('angularjs-template-loader!@/components/author-tile/author-tile.html'),
  bindings: {
    author: '='
  },
  controllerAs: 'ctrl',
  controller: require('@/components/author-tile/controller.js')
}