import './index.css'
import '@fortawesome/fontawesome-free/css/all.css'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

function updateFavicon() {
    const favicon = document.getElementById('app-favicon')
    if (!favicon) return

    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches

    favicon.href = isDark
        ? '/logo_provisory_white.png'
        : '/logo_provisory_black.png'
}

updateFavicon()

window
    .matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', updateFavicon)

createApp(App)
    .use(router)
    .mount('#app')

AOS.init({ duration: 800, once: true })
