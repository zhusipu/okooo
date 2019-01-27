import Vue from 'vue'
import Router from 'vue-router'
import layout from '@/components/layout'
import Laocaituijian from '@/components/Laocaituijian'
import History from '@/components/history'
import Probability from '@/components/probability'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'layout',
      component: layout,
      redirect: 'laocai',
      children: [
        {
          path: 'laocai',
          name: 'laocai',
          component: Laocaituijian
        },
        {
          path: 'history',
          name: 'history',
          component: History
        },
        {
          path: 'probability',
          name: 'probability',
          component: Probability
        }
      ]
    }
  ]
})
