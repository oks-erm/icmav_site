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

function collectPerfMetrics(stage) {
    if (typeof window === 'undefined' || typeof performance === 'undefined') return null
    const nav = performance.getEntriesByType?.('navigation')?.[0]
    const paints = performance.getEntriesByType?.('paint') || []
    const resources = performance.getEntriesByType?.('resource') || []

    const fp = Math.round(paints.find(p => p.name === 'first-paint')?.startTime || 0)
    const fcp = Math.round(paints.find(p => p.name === 'first-contentful-paint')?.startTime || 0)

    const topRes = resources
        .filter(r => !r.name.includes('/api/health'))
        .map(r => {
            const shortName = r.name.replace(/^https?:\/\/[^/]+/, '').slice(0, 42)
            return {
                n: shortName,
                st: Math.round(r.startTime),
                dur: Math.round(r.duration),
                end: Math.round(r.responseEnd),
            }
        })
        .sort((a, b) => b.end - a.end)
        .slice(0, 6)

    return {
        st: stage,
        path: window.location.pathname,
        proto: nav?.nextHopProtocol || '?',
        type: nav?.type || '?',
        redir: nav ? Math.round(nav.redirectEnd - nav.redirectStart) : 0,
        preDns: nav ? Math.round(nav.domainLookupStart - nav.startTime) : 0,
        dns: nav ? Math.round(nav.domainLookupEnd - nav.domainLookupStart) : 0,
        conn: nav ? Math.round(nav.connectEnd - nav.connectStart) : 0,
        tls: nav && nav.secureConnectionStart > 0 ? Math.round(nav.connectEnd - nav.secureConnectionStart) : 0,
        ttfb: nav ? Math.round(nav.responseStart - nav.requestStart) : 0,
        dl: nav ? Math.round(nav.responseEnd - nav.responseStart) : 0,
        respEnd: nav ? Math.round(nav.responseEnd - nav.startTime) : 0,
        tHead: window.__PERF_T0 || 0,
        tBody: window.__PERF_TBODY || 0,
        tMount: window.__PERF_TMOUNT || 0,
        tReady: window.__PERF_TREADY || 0,
        fp,
        fcp,
        domInt: nav ? Math.round(nav.domInteractive - nav.startTime) : 0,
        dcl: nav ? Math.round(nav.domContentLoadedEventEnd - nav.startTime) : 0,
        load: nav && nav.loadEventEnd > 0 ? Math.round(nav.loadEventEnd - nav.startTime) : -1,
        res: topRes,
    }
}

function sendPerfBeacon(stage) {
    try {
        const m = collectPerfMetrics(stage)
        if (!m) return
        const resStr = m.res.map(r => `${r.n}@${r.st}+${r.dur}=${r.end}`).join('|')
        const q = new URLSearchParams({
            _perf: stage,
            p: m.path,
            pr: m.proto,
            ty: m.type,
            pre: String(m.preDns),
            dns: String(m.dns),
            con: String(m.conn),
            tls: String(m.tls),
            ttfb: String(m.ttfb),
            dl: String(m.dl),
            re: String(m.respEnd),
            tb: String(m.tBody),
            tm: String(m.tMount),
            tr: String(m.tReady),
            fcp: String(m.fcp),
            di: String(m.domInt),
            dcl: String(m.dcl),
            ld: String(m.load),
            r: resStr,
        })
        fetch(`/api/health?${q.toString()}`, { keepalive: true, cache: 'no-store' }).catch(() => {})
        if (window.location.search.includes('debug=1')) {
            renderDebugOverlay(m)
        }
    } catch {
        // ignore
    }
}

function renderDebugOverlay(m) {
    let box = document.getElementById('icmav-perf-debug')
    if (!box) {
        box = document.createElement('div')
        box.id = 'icmav-perf-debug'
        box.style.cssText = 'position:fixed;bottom:8px;left:8px;right:8px;z-index:99999;background:rgba(0,0,0,0.92);color:#4ade80;font-family:monospace;font-size:11px;padding:10px;border-radius:10px;border:1px solid #22c55e;max-height:48vh;overflow:auto;line-height:1.35;box-shadow:0 10px 25px rgba(0,0,0,0.6)'
        document.body.appendChild(box)
    }
    const resLines = m.res.map(r => `  ${r.end}ms (${r.st}+${r.dur}ms) ${r.n}`).join('\n')
    box.textContent =
        `[PERF ${m.st}] ${m.path} (${m.proto}, ${m.type})\n` +
        `preDNS:${m.preDns}ms | DNS:${m.dns}ms | Conn:${m.conn}ms (TLS:${m.tls}ms)\n` +
        `TTFB:${m.ttfb}ms | DL:${m.dl}ms | RespEnd:${m.respEnd}ms\n` +
        `tBody:${m.tBody}ms | VueMount:${m.tMount}ms | RouterReady:${m.tReady}ms\n` +
        `FCP:${m.fcp}ms | DOMInt:${m.domInt}ms | DCL:${m.dcl}ms | Load:${m.load}ms\n` +
        `Recursos (fim ms = início+dur):\n${resLines}`
}

const app = createApp(App).use(router)
app.mount('#app')
window.__PERF_TMOUNT = typeof performance !== 'undefined' ? Math.round(performance.now()) : 0

router.isReady().then(() => {
    window.__PERF_TREADY = typeof performance !== 'undefined' ? Math.round(performance.now()) : 0
    setTimeout(() => sendPerfBeacon('ready'), 250)
})

let isInitialNav = true
router.afterEach((to) => {
    if (isInitialNav) {
        isInitialNav = false
        return
    }
    setTimeout(() => sendPerfBeacon(`spa:${to.path}`), 250)
})

if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        updateFavicon()
        window
            .matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', updateFavicon)
        setTimeout(() => sendPerfBeacon('load'), 100)
    }, { once: true })
}
