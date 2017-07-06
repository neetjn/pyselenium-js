import angular from 'angular'
import 'angular-ui-router'

const App = angular.module('psjs', ['ui.router'])

App.config(require('@/router'))

App.controller('FooCtrl', require('@/controllers/foo.js'))

App.component('header', require('@/components/header'))
App.component('footer', require('@/components/footer'))
App.component('authorTile', require('@/components/author-tile'))
App.component('userList', require('@/components/user-list'))

export default App