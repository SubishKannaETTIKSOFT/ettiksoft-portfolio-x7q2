"""
Add security banners:
1. index.html — full glass card banner between topbar and hero
2. All other pages — compact single-line footer notice
"""
import os, sys

BASE = r"C:/Users/SubishKannaSenthilku/OneDrive - Ettik Group/Cowork Playground/Subish/04_TOOLS_INSTALLERS/04_INTERNAL/01_ROADMAP_BUILDER/roadmap-builder/.claude/worktrees/serene-driscoll-e3edd5"
os.chdir(BASE)

errors = []

# ── 1. INDEX.HTML — full banner + CSS ────────────────────────────────────────

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

if 'sec-banner' in idx:
    print('index.html: banner already present — skipping')
else:
    # CSS — insert just before the closing </style> of the last style block
    BANNER_CSS = """
/* ---- SECURITY BANNER ---- */
.sec-banner {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  max-width: var(--max-w, 1080px);
  margin: 0 auto 0;
  padding: 16px 24px;
  background: rgba(181,164,145,0.18);
  border: 1px solid rgba(201,155,107,0.22);
  border-left: 4px solid var(--highlight, #C99B6B);
  border-radius: 14px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.sec-banner-icon {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--highlight, #C99B6B);
}
.sec-banner-body { flex: 1; }
.sec-banner-heading {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--secondary, #B5A491);
  margin-bottom: 4px;
}
.sec-banner-text {
  font-size: 13px;
  line-height: 1.55;
  color: var(--text, #1F2937);
}
/* ---- END SECURITY BANNER ---- */
"""

    # Inject CSS just before the last </style> tag
    last_style_close = idx.rfind('</style>')
    if last_style_close == -1:
        errors.append('index.html: </style> not found')
    else:
        idx = idx[:last_style_close] + BANNER_CSS + idx[last_style_close:]

    # HTML banner — insert between </header> and <section class="hero
    BANNER_HTML = """
  <div class="sec-banner rise d2">
    <span class="sec-banner-icon">
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
        <path d="M10 2L3 5v5c0 4.418 3.134 8.547 7 9.5C13.866 18.547 17 14.418 17 10V5L10 2z"/>
        <line x1="10" y1="8" x2="10" y2="12"/>
        <circle cx="10" cy="14.5" r="0.6" fill="currentColor" stroke="none"/>
      </svg>
    </span>
    <div class="sec-banner-body">
      <div class="sec-banner-heading">Internal Tool</div>
      <div class="sec-banner-text">This is an ETTIKSOFT internal portfolio tool. Data stays in your browser only — nothing is uploaded or shared. Do not enter customer-confidential information, third-party NDAs, or anything you would not put in a personal note.</div>
    </div>
  </div>

"""

    ANCHOR_HTML = '  <section class="hero'
    if ANCHOR_HTML in idx:
        idx = idx.replace(ANCHOR_HTML, BANNER_HTML + ANCHOR_HTML, 1)
        print('index.html: full security banner added')
    else:
        errors.append('index.html: hero section anchor not found')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)

# ── 2. OTHER PAGES — compact footer notice ───────────────────────────────────

FOOTER_NOTICE = '    <div class="sec-footer-notice"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" width="13" height="13" style="flex-shrink:0;opacity:0.7"><path d="M8 1.5L2 4v4c0 3.534 2.507 6.837 6 7.6C11.493 14.837 14 11.534 14 8V4L8 1.5z"/></svg>ETTIKSOFT internal &nbsp;·&nbsp; Data stays in your browser &nbsp;·&nbsp; No customer-confidential information</div>'

FOOTER_CSS = """
/* ---- SECURITY FOOTER NOTICE ---- */
.sec-footer-notice {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 11px;
  letter-spacing: 0.02em;
  color: var(--secondary, #B5A491);
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(181,164,145,0.25);
}
/* ---- END SECURITY FOOTER NOTICE ---- */
"""

OTHER_PAGES = ['dashboard.html', 'product.html', 'editor.html', 'heatmap.html', 'deck.html', 'output.html']

for fname in OTHER_PAGES:
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()

    if 'sec-footer-notice' in c:
        print(f'  {fname}: footer notice already present — skipping')
        continue

    changed = False

    # Inject CSS before last </style>
    last_style = c.rfind('</style>')
    if last_style != -1:
        c = c[:last_style] + FOOTER_CSS + c[last_style:]
        changed = True
    else:
        errors.append(f'{fname}: </style> not found for CSS')

    # For output.html the footer is inside a JS template string — use a different anchor
    if fname == 'output.html':
        # The footer inside the render template
        ANCHOR_OUT = '<footer class="foot">'
        if ANCHOR_OUT in c:
            c = c.replace(ANCHOR_OUT, '<footer class="foot">', 1)  # no-op anchor check
            # Insert notice just before </footer> that belongs to the render template
            # Find the first </footer> after the foot class
            foot_start = c.find('<footer class="foot">')
            if foot_start != -1:
                foot_end = c.find('</footer>', foot_start)
                if foot_end != -1:
                    c = c[:foot_end] + '    ' + FOOTER_NOTICE + '\n    ' + c[foot_end:]
                    print(f'  {fname}: footer notice added')
                else:
                    errors.append(f'{fname}: </footer> not found after .foot')
            else:
                errors.append(f'{fname}: .foot not found')
        else:
            errors.append(f'{fname}: <footer class="foot"> not found')
    else:
        # Standard pages — insert before </footer>
        FOOT_ANCHOR = '<footer class="foot">'
        if FOOT_ANCHOR in c:
            foot_start = c.find(FOOT_ANCHOR)
            foot_end = c.find('</footer>', foot_start)
            if foot_end != -1:
                c = c[:foot_end] + '    ' + FOOTER_NOTICE + '\n  ' + c[foot_end:]
                print(f'  {fname}: footer notice added')
            else:
                errors.append(f'{fname}: </footer> not found')
        else:
            errors.append(f'{fname}: <footer class="foot"> not found')

    if changed or 'footer notice added' in str(errors):
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)

# ── Summary ──────────────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print('\nAll security banners applied.')
