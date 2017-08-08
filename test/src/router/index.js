import Home from '@/router/views/home'
import About from '@/router/views/about'

export default ['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise('/')

  $stateProvider.state('home', Home)
  $stateProvider.state('about', About)

}]
