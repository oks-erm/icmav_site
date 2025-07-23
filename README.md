# Project Development README

This is a private development repository for our web app built with **Vue 3**, **Vite**, **Tailwind CSS**, and **DaisyUI**.

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

* [Node.js (>=18.x)](https://nodejs.org/en)
* [npm](https://www.npmjs.com/) or [pnpm](https://pnpm.io) (recommended)
* A modern terminal (e.g., iTerm2, Warp, or VS Code integrated terminal)

---

### Clone and Run in Development

```bash
# Clone the repository
git clone <your-repo-url>.git

# Navigate into the project
cd <your-project-directory>

# Install dependencies
npm install

# Start the development server
npm run dev
```

This starts the Vite dev server with hot-module replacement (HMR). Navigate to `http://localhost:5173`.

---

## Build for Production

To build and preview a production version locally:

```bash
# Build the application
npm run build

# Preview the production build locally
npm run preview
```

This uses Vite’s `preview` command, which serves the `/dist` folder with the correct base path and SPA routing.

---

## Media Workflow

Optimizing media (especially videos) is crucial for performance. Below is the standardized approach for compressing and encoding videos for both desktop and mobile views using `ffmpeg`.

### Hero Videos

> 📌 **No audio** – remove audio track with `-an`

#### Desktop (target size: 10–20 MB, 1080p)

```bash
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080" \
  -c:v libx264 -crf 23 -preset slow \
  -movflags +faststart -an \
  hero-desktop-1080.mp4
```

#### Mobile (target size: 3–6 MB, 480p)

```bash
ffmpeg -i input.mp4 \
  -vf "scale=854:480" \
  -c:v libx264 -crf 25 -preset slow \
  -movflags +faststart -an \
  hero-mobile-480.mp4
```

---

### 📼 Other Videos (Small/Medium sized)

#### Desktop (target size: 3–6 MB, 720p)

```bash
ffmpeg -i input.mp4 \
  -vf "scale=1280:720" \
  -c:v libx264 -crf 25 -preset veryslow \
  -movflags +faststart -an \
  small-desktop-720.mp4
```

#### Mobile (target size: 1–3 MB, 360p)

```bash
ffmpeg -i input.mp4 \
  -vf "scale=640:360" \
  -c:v libx264 -crf 28 -preset veryslow \
  -movflags +faststart -an \
  small-mobile-360.mp4
```

---

### 🖼️ Images

**(TODO)**: Define standard dimensions, formats (prefer `webp`), and compression guidelines using tools like [ImageMagick](https://imagemagick.org/) or [Squoosh](https://squoosh.app/).

---

## 🔗 Reference Docs

### Frameworks & Libraries

* **Vite**: [https://vitejs.dev/guide/](https://vitejs.dev/guide/)
* **Vue 3**: [https://vuejs.org/guide/introduction.html](https://vuejs.org/guide/introduction.html)
* **Tailwind CSS**: [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
* **DaisyUI**: [https://daisyui.com/docs/themes](https://daisyui.com/docs/themes)
* **AOS (Animate On Scroll)**: [https://michalsnik.github.io/aos](https://michalsnik.github.io/aos)