# Roadmap Builder

A simple, offline web app for building one-page product roadmaps.
No install. No signup. No backend. Runs anywhere a browser does.

---

## Quick start

### Option A — Recommended (works in every browser)

```bash
cd roadmap-builder
python3 -m http.server 8000
```

Open `http://localhost:8000` in your browser.

If you don't have Python, here are equivalents:

```bash
# Node.js
npx serve .

# PHP
php -S localhost:8000

# Ruby
ruby -run -ehttpd . -p8000
```

### Option B — Direct (just double-click)

Double-click `index.html`. Some browsers (especially Safari) restrict
LocalStorage when files are opened directly via `file://`. If your saved
roadmaps don't persist between pages, switch to Option A.

---

## What's in here

| File | What it does |
|---|---|
| `index.html` | Home page — list of saved roadmaps, create / duplicate / delete |
| `editor.html` | Form editor — fill in your roadmap (auto-saves as you type) |
| `output.html` | Generated visual roadmap — view, print, or download |
| `README.md` | this file |

That's it. Four files. Total folder size under 100 KB.

---

## How to use

1. Open the home page
2. Click **+ Create new roadmap**
3. Fill in the form sections — every section is optional, empty ones are hidden in the output
4. Click **View output** to see your generated roadmap
5. Click **Download HTML** to save a self-contained file you can email, share, embed in Notion, or open offline anywhere

---

## Privacy

Everything stays on your machine. The app never sends your data anywhere.
The only network call is loading Google Fonts on first view; if you want
fully offline operation, download the fonts locally and update the
`<link>` tags in each HTML file.

---

## Editing the visual style

All design tokens (colors, fonts, spacing) live in CSS variables at the
top of each HTML file's `<style>` tag — look for the `:root` block.
Change the values once, the whole page updates.

```css
:root {
  --bg:        #F7F5F0;   /* page background */
  --ink:       #1A1A18;   /* main text color */
  --brand:     #1F3F4F;   /* accent color */
  --go:        #2D5F3F;   /* "on track" green */
  --decide:    #B8851F;   /* "caution" amber */
  --risk:      #A1342B;   /* "at risk" red */
  /* ... etc */
}
```

---

## Backup / portability

Your roadmaps live in browser LocalStorage under the key
`roadmap-builder.roadmaps`. To back up or move to a different browser:

1. Open browser DevTools (F12) on any page of the app
2. Console tab, run: `copy(localStorage.getItem('roadmap-builder.roadmaps'))`
3. Paste the result somewhere safe
4. To restore on another browser:
   `localStorage.setItem('roadmap-builder.roadmaps', PASTE_HERE)`

A future version may add export / import buttons for this.

---

Built once, edit forever.
