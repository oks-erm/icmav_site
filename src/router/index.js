// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MinistryDetail from '../views/MinistryDetail.vue'

const routes = [
    { path: '/', component: Home },
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
    routes
})