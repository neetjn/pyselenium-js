export default ['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('/')

  $stateProvider.state('home', {
    url: '/',
    template: require('angularjs-template-loader!@/views/home.html')
  })

  $stateProvider.state('about', {
    url: '/about',
    template: require('angularjs-template-loader!@/views/about.html')
  })

}]