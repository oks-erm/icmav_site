import assert from 'node:assert/strict'
import { test } from 'node:test'
import { createServer } from 'vite'

// Exercises the actual service URL after Vite has injected its build environment.
test('default API requests use the website origin', async () => {
  const originalBaseUrl = process.env.VITE_API_BASE_URL
  delete process.env.VITE_API_BASE_URL
  let server
  const originalFetch = globalThis.fetch
  let requestUrl
  globalThis.fetch = async (url) => {
    requestUrl = url
    return { ok: true, json: async () => ({ value: 'Welcome' }) }
  }
  try {
    server = await createServer({
      envDir: false,
      server: { middlewareMode: true, hmr: false },
      mode: 'production',
    })
    const api = await server.ssrLoadModule('/src/services/api.js')
    await api.getWelcomeContent()
    assert.equal(requestUrl, '/api/settings/welcome')
  } finally {
    globalThis.fetch = originalFetch
    if (originalBaseUrl === undefined) delete process.env.VITE_API_BASE_URL
    else process.env.VITE_API_BASE_URL = originalBaseUrl
    await server?.close()
  }
})

test('relative API configuration supports the local backend proxy', async () => {
  const originalBaseUrl = process.env.VITE_API_BASE_URL
  process.env.VITE_API_BASE_URL = '/api'
  try {
    const { default: config } = await import('../vite.config.js?relative-api')
    assert.equal(config.server.proxy['/api'].target, 'http://127.0.0.1:8000')
    assert.equal(config.server.proxy['/uploads'].target, 'http://127.0.0.1:8000')
  } finally {
    if (originalBaseUrl === undefined) delete process.env.VITE_API_BASE_URL
    else process.env.VITE_API_BASE_URL = originalBaseUrl
  }
})
