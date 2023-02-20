import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Home'
import Settings from '../views/Settings.vue'
import Diagnostics from '../views/Diagnostics'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
  {
    path: '/diagnostics',
    name: 'Diagnostics',
    component: Diagnostics,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router