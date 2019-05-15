import Vue from 'vue'
import Router from 'vue-router'
import DashboardLayout from '@/layout/DashboardLayout'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: 'main',
      component: DashboardLayout,
      children: [
        {
          path: '/analysis',
          name: 'dashboard',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "demo" */ './views/Dashboard.vue')
        },
        {
          path: '/map1',
          name: 'Map',
          component: () => import(/* webpackChunkName: "demo" */ './views/map1.vue')
        },
        {
          path: '/person',
          name: 'Person',
          component: () => import(/* webpackChunkName: "demo" */ './views/person.vue')
        },
        {
          path: '/main',
          name: 'main',
          component: () => import(/* webpackChunkName: "demo" */ './views/main.vue')
        },

      ]
    }
  ]
})
