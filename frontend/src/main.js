import './index.css'
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

createApp(App)
    .use(router)
    .mount('#app')

if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        updateFavicon()
        window
            .matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', updateFavicon)
    }, { once: true })
}
