import aboutCtrl from '@/router/views/about/controller'

export default {
  url: '/about',
  template: require('angularjs-template-loader!@/router/views/about/view.html'),
  controller: aboutCtrl
}
