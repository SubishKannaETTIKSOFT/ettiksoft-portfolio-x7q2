"""
Inject #auth-loading overlay div immediately after <body> in all 8 HTML pages.
Prevents page flash — overlay covers content until auth completes.
"""
import os, sys

BASE = r"C:/Users/SubishKannaSenthilku/OneDrive - Ettik Group/Cowork Playground/Subish/04_TOOLS_INSTALLERS/04_INTERNAL/01_ROADMAP_BUILDER/roadmap-builder/.claude/worktrees/serene-driscoll-e3edd5"
os.chdir(BASE)

OVERLAY = """<div id="auth-loading" style="position:fixed;inset:0;background:#F7F4ED;z-index:99999;display:flex;align-items:center;justify-content:center;font-family:system-ui,-apple-system,sans-serif;">
  <div style="text-align:center;color:#6B7280;">
    <div style="width:32px;height:32px;border:3px solid #E5E7EB;border-top-color:#5E8A7B;border-radius:50%;animation:authspin 0.8s linear infinite;margin:0 auto 16px;"></div>
    <div>Signing you in…</div>
  </div>
</div>
<style>@keyframes authspin{to{transform:rotate(360deg);}}</style>
"""

PAGES = [
    'index.html', 'dashboard.html', 'product.html', 'editor.html',
    'heatmap.html', 'deck.html', 'output.html', 'GETTING_STARTED.html'
]

errors = []

for fname in PAGES:
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()

    if 'auth-loading' in c:
        print(f'  {fname}: overlay already present — skipping')
        continue

    # Find the opening <body> tag (may have attributes or be plain)
    import re
    m = re.search(r'(<body[^>]*>)', c)
    if not m:
        errors.append(f'{fname}: <body> tag not found')
        continue

    body_tag = m.group(1)
    c = c.replace(body_tag, body_tag + '\n' + OVERLAY, 1)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'  {fname}: overlay injected')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print(f'\nAll {len(PAGES)} pages have auth-loading overlay.')
