export default function($stateProvider) {

  const home = {
    name: 'Home',
    url: '/',
    template: require('angularjs-template-loader!@/views/home.html')
  }

  const about = {
    name: 'About',
    url: '/about',
    template: require('angularjs-template-loader!@/views/about.html')
  }

  $stateProvider.state(home)
  $stateProvider.state(about)

}