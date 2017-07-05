import { angular } from 'angular'

const App = angular.module('psjs', ['ui.router'])

App.config(require('@/router'))

import FooCtrl from '@/controllers/foo.js'
App.controller('FooCtrl', FooCtrl)

import { author } from '@/components/author-tile'
import { userList } from '@/components/user-list'
App.component('authorTile', author)
App.component('userList', userList)

export default App