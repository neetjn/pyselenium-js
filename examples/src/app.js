import angular from 'angular'
import 'angular-ui-router'

const App = angular.module('psjs', ['ui.router'])

import router from '@/router'
App.config(router)

import FooCtrl from '@/controllers/foo.js'
App.controller('FooCtrl', FooCtrl)

import authorTile from '@/components/author-tile'
App.component('authorTile', authorTile)
import userList from '@/components/user-list'
App.component('userList', userList)

export default App