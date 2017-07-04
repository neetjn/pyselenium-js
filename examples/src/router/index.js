export default function($stateProvider) {

  const home = {
    name: 'Home',
    url: '/',
    template: require('@/views/home.html')
  }

  const about = {
    name: 'About',
    url: '/about',
    template: require('@/views/about.html')
  }

  $stateProvider.state(home)
  $stateProvider.state(about)

}