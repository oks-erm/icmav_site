// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import DonationFormView from '../views/DonationFormView.vue'

const HomeView = () => import('../views/HomeView.vue')
const AdminView = () => import('../views/AdminView.vue')
const MinistriesDetailView = () => import('../views/MinistriesDetailView.vue')
const MaintenanceView = () => import('../views/MaintenanceView.vue')
const TermsView = () => import('../views/TermsView.vue')
const PrivacyView = () => import('../views/PrivacyView.vue')
const RefundView = () => import('../views/RefundView.vue')
const CookiePolicyView = () => import('../views/CookiePolicyView.vue')
const NotFoundView = () => import('../views/NotFoundView.vue')

// Modo manutenção ativado por variável de ambiente se configurado como 'true'
const isMaintenanceMode = import.meta.env.VITE_MAINTENANCE_MODE === 'true'

const routes = [
  {
    path: '/',
    name: 'Root',
    component: isMaintenanceMode ? MaintenanceView : HomeView,
  },
  {
    path: '/manutencao',
    name: 'Maintenance',
    component: MaintenanceView,
  },
  {
    path: '/igrejaicmav',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
  },
  {
    path: '/igrejaicmav/admin',
    redirect: '/admin',
  },
  {
    path: '/oferta',
    redirect: { name: 'Home', hash: '#donations' },
  },
  {
    path: '/donativos',
    name: 'Donativos',
    component: DonationFormView,
  },
  {
    path: '/termos-e-condicoes',
    name: 'Terms',
    component: TermsView,
  },
  {
    path: '/politica-privacidade',
    name: 'Privacy',
    component: PrivacyView,
  },
  {
    path: '/politica-cookies',
    name: 'Cookies',
    component: CookiePolicyView,
  },
  {
    path: '/politica-de-cookies',
    redirect: '/politica-cookies',
  },
  {
    path: '/cookies',
    redirect: '/politica-cookies',
  },
  {
    path: '/politica-cancelamento-reembolso',
    name: 'Refund',
    component: RefundView,
  },
  {
    path: '/ministerio/:slug',
    name: 'MinistryDetail',
    component: MinistriesDetailView,
    props: true,
  },
  // Mantém retrocompatibilidade com slugs diretos (ex: /mulheres)
  {
    path: '/:slug([a-z0-9-]+)',
    name: 'MinistryDetailLegacy',
    component: MinistriesDetailView,
    props: true,
  },
  {
    path: '/:catchAll(.*)*',
    name: 'NotFound',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return new Promise((resolve) => {
        setTimeout(() => {
          const el = document.querySelector(to.hash)
          if (el) {
            const header = document.getElementById('site-sticky-header')
            const offset = header ? header.offsetHeight : 80
            const y = el.getBoundingClientRect().top + window.scrollY - offset
            resolve({
              top: Math.max(0, y),
              behavior: 'smooth',
            })
          } else {
            resolve({ top: 0, behavior: 'smooth' })
          }
        }, 150)
      })
    }
    return { top: 0 }
  },
})

export default router
