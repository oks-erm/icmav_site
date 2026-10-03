import DOMPurify from 'dompurify'

// Match the rich-text editor's formatting, excluding active content and inline CSS.
const richTextPolicy = {
  ALLOWED_TAGS: [
    'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'b', 'em', 'i', 'u', 's', 'strike',
    'blockquote', 'pre', 'code', 'ol', 'ul', 'li', 'span', 'div', 'a',
  ],
  ALLOWED_ATTR: ['class', 'href', 'title', 'target', 'rel', 'data-list'],
  ALLOW_DATA_ATTR: false,
  ALLOW_ARIA_ATTR: false,
}

DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName === 'A' && node.hasAttribute('target')) {
    node.setAttribute('rel', 'noopener noreferrer')
  }
})

export function sanitizeHtml(value) {
  return typeof value === 'string' ? DOMPurify.sanitize(value, richTextPolicy) : ''
}
