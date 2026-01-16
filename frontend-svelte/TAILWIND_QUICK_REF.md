# ⚡ Quick Reference: TailwindCSS v4 vs v3

## 🔄 MIGRATION SUMMARY

| Aspect            | v3 (Old)                | v4 (New - Your Setup)      |
| ----------------- | ----------------------- | -------------------------- |
| **Config File**   | `tailwind.config.js` ❌ | `app.css` with `@theme` ✅ |
| **Import**        | `@tailwind base;`       | `@import 'tailwindcss';`   |
| **Plugins**       | `plugins: [...]` in JS  | `@plugin '...'` in CSS     |
| **Custom Colors** | `theme.extend.colors`   | `--color-name` CSS vars    |
| **Build Speed**   | ~2.5s                   | ~1.2s (2x faster!)         |

---

## 📝 YOUR CURRENT SETUP

```
✅ vite.config.ts    → import tailwindcss from '@tailwindcss/vite'
✅ app.css           → @theme { --color-primary-500: #a855f7 }
✅ +layout.svelte    → import '../app.css'
✅ +page.svelte      → Ready to use Tailwind classes!
```

---

## 🎨 AVAILABLE CUSTOM CLASSES

### Colors

```html
<div class="bg-primary-500">Purple</div>
<div class="bg-chess-light">Beige board</div>
<div class="bg-chess-dark">Brown board</div>
<div class="bg-success-500">Green</div>
<div class="bg-warning-500">Orange</div>
<div class="bg-error-500">Red</div>
```

### Animations

```html
<div class="animate-slide-in-bottom">Slides up</div>
<div class="animate-fade-in">Fades in</div>
<div class="animate-scale-in">Scales in</div>
<div class="animate-spin">Spins</div>
<div class="animate-pulse">Pulses</div>
<div class="animate-shimmer">Loading shimmer</div>
```

### Common Patterns

```html
<!-- Button -->
<button
	class="bg-primary-600 hover:bg-primary-700 rounded-lg px-4 py-2 text-white transition-colors"
>
	Click me
</button>

<!-- Card -->
<div class="rounded-xl bg-white p-6 shadow-lg transition-shadow hover:shadow-2xl">Card content</div>

<!-- Gradient -->
<div class="from-primary-500 bg-gradient-to-r to-purple-600">Gradient background</div>
```

---

## ✅ NEXT STEP

Install Bits UI:

```bash
cd d:\Portofolio\portfolio\chess-recs-nextgen\frontend-svelte
npm install bits-ui motion svelte-motion @tanstack/svelte-query zod sveltekit-superforms lucide-svelte svelte-sonner
```

Then run:

```bash
npm run dev
```

**Full docs:** `TAILWIND_V4_GUIDE.md`
