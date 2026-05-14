# Roadmap Builder

A single-page, offline, no-backend web app for product teams to create one-page roadmaps.
Built as 3 static HTML files. Data lives in browser LocalStorage. No build step.

## Files

| File | Purpose |
|---|---|
| `index.html` | Home — list of saved roadmaps. Create / duplicate / delete. |
| `editor.html` | Form editor — 9 sections. Auto-saves to LocalStorage as you type. |
| `output.html` | Rendered roadmap. Print, download self-contained HTML, embed inside an iframe for live preview from the editor. |
| `GETTING_STARTED.html` | User-facing onboarding doc. |
| `README.md` | Repo readme. |

No package.json. No build. Open in any browser via `python3 -m http.server 8000` and visit localhost:8000.

## How data is stored

- LocalStorage key: `roadmap-builder.roadmaps`
- Shape: `[{id, name, createdAt, updatedAt, data: {masthead, hero, kpis, bets, products, actions, quarters, decisions, risks}}]`
- The 9 editor sections (`SECTION_LIST_KEYS` in editor.html) are: `kpis, bets, products, actions, quarters, decisions, risks` plus `masthead` and `hero` objects.

## Visual design system (bright aurora light theme)

Tokens are at the bottom of each file's last `<style>` block. The cascade is intentional — final overrides win.

- **Body:** `#FAF7F2` warm cream (not pure white)
- **Aurora orbs:** 3 large radial-gradient orbs + 1 via `::before`, all blurred 85px, drifting on 60-80s loops. Colors: `#38BDF8` cyan, `#FB7185` coral, `#34D399` mint, `#C084FC` lavender
- **Schematic SVG backdrop:** PCB-style traces and components at `opacity: 0.16`, blur 0.5px — engineering texture, not detail
- **Glass cards:** `rgba(255, 255, 255, 0.62)` with `backdrop-filter: blur(22px) saturate(180%)`. Heavier blur (28-32px) on hero and preview pane.
- **Card shadow stack:** 3 layers — inset white top shine + close shadow + mid shadow. Don't add more layers; tested as the perf sweet spot.
- **Primary button gradient:** `linear-gradient(135deg, #06B6D4 0%, #A78BFA 55%, #FB7185 100%)` cyan→lavender→coral
- **Text:** `#0F172A` slate-near-black on cards. `#475569` muted helper text. Both pass AAA on cream.
- **Border radius:** hero 24px, sections 20px, cards 18px, dyn-rows 14px, buttons 12px, chips 999px
- **Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` everywhere. Three durations only: 160ms / 280ms / 420ms.

## Watch out for (gotchas we've hit)

1. **Broad `div { color: #0F172A !important }` rules will kill toast/dialog text.** The `.toast` has dark glass bg with white text; if you add a generic dark-text rule for cards, scope it to exclude `.toast *` or re-assert `.toast, .toast * { color: white !important }` after.

2. **`backdrop-filter: blur()` is the #1 scroll-perf killer.** Every glass surface re-composites every frame. Keep blur ≤ 24px on most surfaces. Anything over 32px noticeably stutters on mid-range laptops.

3. **The preview pane uses JavaScript inline styles with `setProperty(prop, val, 'important')`** to force `position: fixed; top: 0; right: 0; transform: translateX(0)`. CSS-only rules kept losing specificity battles against accumulated overrides. The pane builds in `function build()` around line 3498 of editor.html.

4. **iframe race condition** in the preview: `iframe.onload` MUST be attached BEFORE `iframe.src` is set. Cached loads fire the load event before the handler is wired otherwise → spinner-forever.

5. **`window.toast.confirm(msg, opts)`** is the custom modal. NOT the native browser `confirm()`. Used at index.html line ~3880 for delete confirmation.

6. **Output page renders into `#render-target`** via `function render(rm)`. There's a wrapped version `window.render` that handles the newer quarters/decisions/risks sections. The original render is captured as `window.__originalRender`. When patching the postMessage handler, call `window.render` (current), not `window.__render`.

7. **Cache control meta tags** are set in `<head>` of all three files. If users still see stale CSS after a change, the answer is hard-refresh (`Ctrl/Cmd+Shift+R`), not more cache headers.

8. **The "+ Add" buttons in editor sections** rebuild that section's DOM. After rebuilding, the priority radios need to be re-checked from data — there was a bug where `setAttribute('checked', false)` was being treated as truthy in HTML. The `el()` helper handles this — don't change it.

## Common tasks and where to do them

- **Change body bg or theme colors** → bottom `<style>` of all 3 files, look for `body { background: #FAF7F2 !important; }`
- **Change card opacity / blur** → the `:root { --glass-bg: ... }` token + `.sec, .card, .bet, ... { backdrop-filter: blur(22px) ... !important }` rule
- **Add a new section to roadmap data** → 4 places: editor.html (`SECTION_LIST_KEYS` array, the section markup, the row template), output.html (the render function), plus optional preview update
- **Change button gradient** → search `linear-gradient(135deg, #06B6D4` — only used on `.btn.primary`
- **Change schematic** → the SVG with `class="schematic-bg"`, inserted after `<body>` in each file. Pure SVG, ~150 lines.

## Browser support

Modern Chromium-based browsers, Firefox, Safari 16+. `backdrop-filter` requires `-webkit-` prefix included throughout. `view-transition` API is feature-detected and degrades to instant nav.

## Testing locally

```bash
cd roadmap-builder
python3 -m http.server 8000
# open http://localhost:8000
```

Hard refresh after CSS changes: `Ctrl/Cmd + Shift + R`.

## Don't

- Don't add a build step. The whole point is no-install, edit-and-refresh.
- Don't add tracking, analytics, or any network requests beyond Google Fonts.
- Don't refactor into multiple JS/CSS files. Each HTML file is self-contained on purpose so users can download a single file and host it anywhere.
- Don't switch the inline-style preview pane fix back to CSS. It will regress.

---

## Session 14 May 2026 — End-of-day state

**Status:** Authentication 95% complete. One Azure admin change pending — blocks final test.

**What works:**
- Tool deployed to GitHub Pages
- URL: https://subishkannaettiksoft.github.io/ettiksoft-portfolio-x7q2/
- MSAL loads from local bundle (no CDN)
- Loading overlay prevents page flash
- Error handling with retry button (no infinite loops)
- Dedicated app registration: ettiksoft-portfolio-auth
- ClientId: 7d009dc9-11a5-4f31-b984-cdcb526bdfd8
- TenantId: f5d1d2b4-0083-43ed-92b3-f80cb2db9f27
- 3 redirect URIs registered in Azure

**Pending blocker:**
Azure app registration platform type is "Web" but needs to be "Single-Page Application" (SPA).
Error: AADSTS9002326 cross-origin token redemption.

Admin (Gowthami) needs to:
1. Azure → ettiksoft-portfolio-auth → Authentication
2. Add platform → Single-page application
3. Add SPA URIs: x7q2/ and x7q2 (both)
4. Delete the existing "Web" platform entirely
5. Save

**Resume next session:**
- Verify Azure platform change with screenshot
- Test live URL in Edge InPrivate
- If working: enter real ETTIKSOFT product data (CYPHERA, AUTOPENTRIX, CYMAS, HSM, E-SUMO)
- Run 5-minute demo rehearsal for KAM presentation
- Don't add `overflow: hidden` to card surfaces — it clips the indigo glow shadows that give depth.
