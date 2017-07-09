import homeCtrl from '@/router/routes/home/controller.js'
import aboutCtrl from '@/router/routes/about/controller.js'

export default ['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('/')

  $stateProvider.state('home', {
    url: '/',
    template: require('angularjs-template-loader!@/router/routes/home/home.html'),
    controller: homeCtrl
  })

  $stateProvider.state('about', {
    url: '/about',
    template: require('angularjs-template-loader!@/router/routes/about/about.html'),
    controller: aboutCtrl
  })

}]
