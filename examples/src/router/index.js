export default function($stateProvider) {

  const home = {
    name: 'Home',
    url: '/',
    template: require('@/views/home.html')
  }

  const about = {
    name: 't',
    url: '/about',
    template: require('@/views/about.html')
  }

  $stateProvider.state(helloState)
  $stateProvider.state(aboutState)

}