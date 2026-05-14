"""
Inject MSAL auth into all 8 HTML pages:
  1. <script src="./auth.js"> + <script src="./auth-guard.js"> in <head>
  2. #auth-user-badge span in each topbar
  3. #auth-logout-btn button in each footer
"""
import os, sys

BASE = r"C:/Users/SubishKannaSenthilku/OneDrive - Ettik Group/Cowork Playground/Subish/04_TOOLS_INSTALLERS/04_INTERNAL/01_ROADMAP_BUILDER/roadmap-builder/.claude/worktrees/serene-driscoll-e3edd5"
os.chdir(BASE)

errors = []

AUTH_SCRIPTS = """\
  <script src="./auth.js"></script>
  <script src="./auth-guard.js"></script>
"""

USER_BADGE = '<span id="auth-user-badge" style="display:none;font-size:11px;color:var(--text-muted,#6B7280);background:rgba(94,138,123,0.12);padding:4px 10px;border-radius:20px;margin-left:8px;align-items:center;"></span>'

LOGOUT_BTN = '<button id="auth-logout-btn" style="background:none;border:none;cursor:pointer;font-size:11px;color:var(--text-muted,#6B7280);padding:0;margin-left:12px;text-decoration:underline;">Sign out</button>'

def patch(fname, ops):
    """ops = list of (old, new) replacements."""
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    if 'auth-user-badge' in c and 'auth-logout-btn' in c and 'auth-guard.js' in c:
        print(f'  {fname}: already patched — skipping')
        return
    for old, new in ops:
        if old in c:
            c = c.replace(old, new, 1)
        else:
            errors.append(f'{fname}: anchor not found: {repr(old[:60])}')
    if c != orig:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'  {fname}: patched')
    else:
        print(f'  {fname}: no changes made')


# ── index.html ───────────────────────────────────────────────────────────────
# head: before </head>
# badge: inside <header class="masthead rise d1"> before </header>
# logout: inside <footer class="foot"> before </footer>
patch('index.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '  </header>\n\n  <div class="sec-banner',
        f'  {USER_BADGE}\n  </header>\n\n  <div class="sec-banner'
    ),
    (
        '\n  </footer>\n\n</div>\n\n<script>',
        f'\n  {LOGOUT_BTN}\n  </footer>\n\n</div>\n\n<script>'
    ),
])

# ── dashboard.html ───────────────────────────────────────────────────────────
# topbar closes with </header> after </nav>
# footer is <footer class="foot">
patch('dashboard.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '    </nav>\n  </header>',
        f'    </nav>\n    {USER_BADGE}\n  </header>'
    ),
    (
        '\n  </footer>\n\n</div>',
        f'\n  {LOGOUT_BTN}\n  </footer>\n\n</div>'
    ),
])

# ── product.html ─────────────────────────────────────────────────────────────
# static topbar closes with:
#   <button id="tour-retrigger-btn"...></button>
#   </header>
# footer (in JS template): </button>\n    </footer>\n  `
patch('product.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '    <button id="tour-retrigger-btn" title="Restart guided tour">?</button>\n  </header>',
        f'    <button id="tour-retrigger-btn" title="Restart guided tour">?</button>\n    {USER_BADGE}\n  </header>'
    ),
    (
        '        Delete product\n      </button>\n      <div class="sec-footer-notice"',
        f'        Delete product\n      </button>\n      {LOGOUT_BTN}\n      <div class="sec-footer-notice"'
    ),
])

# ── editor.html ──────────────────────────────────────────────────────────────
# topbar-inner closes: then outer topbar closes
# no footer — logout goes near the sec-footer-notice div before </body>
patch('editor.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '    <a href="#" class="btn primary" id="view-output-btn">',
        f'    {USER_BADGE}\n    <a href="#" class="btn primary" id="view-output-btn">'
    ),
    (
        '<div class="sec-footer-notice" style="max-width:1080px;',
        f'{LOGOUT_BTN}\n<div class="sec-footer-notice" style="max-width:1080px;'
    ),
])

# ── heatmap.html ─────────────────────────────────────────────────────────────
# topbar closes with </header> after </nav>
# footer: <footer class="foot">
patch('heatmap.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '    </nav>\n  </header>\n\n  <div id="page-content">',
        f'    </nav>\n    {USER_BADGE}\n  </header>\n\n  <div id="page-content">'
    ),
    (
        '\n  </footer>\n\n</div>\n\n<script>',
        f'\n  {LOGOUT_BTN}\n  </footer>\n\n</div>\n\n<script>'
    ),
])

# ── deck.html ────────────────────────────────────────────────────────────────
# Static topbar: <header class="deck-topbar"> closes with </header>
# Footer is in JS template — put both badge AND logout in topbar nav
patch('deck.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '    </nav>\n  </header>\n\n  <div id="deck-content">',
        f'    </nav>\n    {USER_BADGE}\n    {LOGOUT_BTN}\n  </header>\n\n  <div id="deck-content">'
    ),
])

# ── output.html ──────────────────────────────────────────────────────────────
# Static: <div class="app-toolbar"> / app-toolbar-inner closes before render-target
# Logout also in app-toolbar (footer is in JS template)
patch('output.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '    <button class="primary" id="download-btn">',
        f'    {USER_BADGE}\n    {LOGOUT_BTN}\n    <button class="primary" id="download-btn">'
    ),
])

# ── GETTING_STARTED.html ─────────────────────────────────────────────────────
# No topbar — add badge to toc nav footer area, logout to <footer class="foot">
patch('GETTING_STARTED.html', [
    ('</head>', AUTH_SCRIPTS + '</head>'),
    (
        '  </nav>\n\n  <!-- ============================================================\n       MAIN CONTENT',
        f'    {USER_BADGE}\n  </nav>\n\n  <!-- ============================================================\n       MAIN CONTENT'
    ),
    (
        '\n    </footer>\n</div>\n\n</body>',
        f'\n    {LOGOUT_BTN}\n    </footer>\n</div>\n\n</body>'
    ),
])

# ── Summary ──────────────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print('\nAll 8 pages patched.')
