import { angular } from 'angular'

const App = angular.module('psjs', [])

import FooCtrl from '@/controllers/foo.js'
App.controller('FooCtrl', FooCtrl)

import { author } from '@/components/author'
import { userList } from '@/components/user-list'
App.component('author', author)
App.component('user-list', userList)

export default App