// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import MuseUI from 'muse-ui'
import iView from 'iview'
import store from './store'
import 'muse-ui/dist/muse-ui.css'
import 'iview/dist/styles/iview.css'

Vue.use(MuseUI)
Vue.use(iView)
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
