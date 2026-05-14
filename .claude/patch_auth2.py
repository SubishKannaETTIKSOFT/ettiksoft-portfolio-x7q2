"""Fix the 4 remaining auth element injections."""
import os, sys

BASE = r"C:/Users/SubishKannaSenthilku/OneDrive - Ettik Group/Cowork Playground/Subish/04_TOOLS_INSTALLERS/04_INTERNAL/01_ROADMAP_BUILDER/roadmap-builder/.claude/worktrees/serene-driscoll-e3edd5"
os.chdir(BASE)

errors = []

BADGE = '<span id="auth-user-badge" style="display:none;font-size:11px;color:var(--text-muted,#6B7280);background:rgba(94,138,123,0.12);padding:4px 10px;border-radius:20px;margin-left:8px;align-items:center;"></span>'
LOGOUT = '<button id="auth-logout-btn" style="background:none;border:none;cursor:pointer;font-size:11px;color:var(--text-muted,#6B7280);padding:0;margin-left:12px;text-decoration:underline;">Sign out</button>'

def fix(fname, target_id, anchor_old, anchor_new):
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    if target_id in c:
        print(f'  {fname}: {target_id} already present — skipping')
        return
    if anchor_old in c:
        c = c.replace(anchor_old, anchor_new, 1)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'  {fname}: {target_id} injected')
    else:
        errors.append(f'{fname}: anchor not found for {target_id}: {repr(anchor_old[:70])}')

# index.html — badge before </header> (masthead). Two blank lines follow.
fix('index.html', 'auth-user-badge',
    '    <div class="meta" id="now"></div>\n  </header>',
    f'    <div class="meta" id="now"></div>\n  {BADGE}\n  </header>')

# dashboard.html — logout before </footer>
fix('dashboard.html', 'auth-logout-btn',
    '  </footer>\n</div>',
    f'  {LOGOUT}\n  </footer>\n</div>')

# heatmap.html — logout before </footer>
fix('heatmap.html', 'auth-logout-btn',
    '  </footer>\n</div>',
    f'  {LOGOUT}\n  </footer>\n</div>')

# GETTING_STARTED.html — logout before </footer>
fix('GETTING_STARTED.html', 'auth-logout-btn',
    '    </footer>\n\n  </main>',
    f'    {LOGOUT}\n    </footer>\n\n  </main>')

if errors:
    print('\nERRORS:')
    for e in errors: print(f'  {e}')
    sys.exit(1)
else:
    print('\nAll 4 remaining elements injected.')
