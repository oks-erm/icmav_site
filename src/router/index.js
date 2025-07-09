// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MinistryDetail from '../views/MinistryDetail.vue'

const routes = [
    { 
        path: '/', 
        name: 'Home',  
        component: Home 
    },
    // redirect /oferta → /#oferta
    {
        path: '/oferta',
        redirect: { name: 'Home', hash: '#oferta' }
    },
    {
        path: '/:slug',
        name: 'MinistryDetail',
        component: MinistryDetail,
        props: true
    },
    { path: '/:catchAll(.*)*', redirect: '/' }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {

        if (savedPosition) {
            return savedPosition
        }

        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth'
            }
        }

        return { top: 0 }
    }
  })