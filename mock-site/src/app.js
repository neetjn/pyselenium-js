import angular from 'angular'
import 'angular-ui-router'

import router from '@/router'

import fooCtrl from '@/controllers/foo.js'

import header from '@/components/header'
import bottom from '@/components/bottom'
import authorTile from '@/components/author-tile'
import userList from '@/components/user-list'

const App = angular.module('psjs', ['ui.router'])

App.config(router)
App.controller('FooCtrl',fooCtrl)
App.component('header', header)
App.component('bottom', bottom)
App.component('authorTile', authorTile)
App.component('userList', userList)

export default App