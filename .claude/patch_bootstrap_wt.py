"""
Inject a silent bootstrap IIFE into all 7 HTML pages (worktree version).
Seeds ETTIKSOFT demo data if localStorage is empty.
Runs BEFORE the migration IIFE.
"""
import json, os, sys

BASE = r"C:/Users/SubishKannaSenthilku/OneDrive - Ettik Group/Cowork Playground/Subish/04_TOOLS_INSTALLERS/04_INTERNAL/01_ROADMAP_BUILDER/roadmap-builder/.claude/worktrees/serene-driscoll-e3edd5"
os.chdir(BASE)

NA = 'n/a'
FIXED_DATE = '2026-01-15T09:00:00.000Z'

demo = {
  "id": "ettiksoft-001",
  "name": "ETTIKSOFT Product Portfolio",
  "isSnapshot": False,
  "snapshotDate": None,
  "createdAt": FIXED_DATE,
  "updatedAt": FIXED_DATE,
  "lastEditedBy": "me",
  "strategicContext": {
    "masthead": {
      "company": "ETTIKSOFT",
      "tagline": "Security · Connectivity · Autonomy",
      "date": "2026-05-11",
      "version": "2.0"
    },
    "hero": {
      "eyebrow": "Q2 2026 Product Roadmap",
      "headline": "From prototype to production — ship security that scales",
      "accentWord": "security",
      "lede": "Three flagship products moving from lab to market this year. Hardware certification on track, cloud platform in beta, autonomous pen-test in concept."
    },
    "kpis": [
      {"value": "TRL 9", "label": "HSM target by Q4", "subscript": ""},
      {"value": "3", "label": "Products in portfolio", "subscript": ""},
      {"value": "£2.4M", "label": "Pipeline value", "subscript": "committed"}
    ],
    "bets": [
      {"verb": "Certify", "headline": "HSM for automotive market", "lede": "ISO 21434 and UNECE R155 clearance unlocks Tier-1 pipeline worth £1.8M.", "priority": "high"},
      {"verb": "Scale", "headline": "CYPHERA to 50 enterprise tenants", "lede": "Move from 3 pilot customers to 50 paying accounts by end of year.", "priority": "high"},
      {"verb": "Validate", "headline": "AUTOPENTRIX market fit", "lede": "Three paid POCs with MSSP partners to confirm ICP before Series A.", "priority": "medium"}
    ],
    "actions": [
      {"text": "Complete HSM FIPS 140-3 Level 3 lab testing", "owner": "HW Eng", "due": "2026-06-30", "priority": "high"},
      {"text": "Onboard 5 new CYPHERA design-partners", "owner": "Sales", "due": "2026-07-15", "priority": "high"},
      {"text": "Kick off AUTOPENTRIX POC #1 with RedTeam Inc", "owner": "BD", "due": "2026-06-01", "priority": "medium"}
    ],
    "quarters": [
      {"label": "Q2 2026", "theme": "Certify & Validate", "milestones": "HSM lab cert complete · CYPHERA 10 tenants · AUTOPENTRIX POC #1"},
      {"label": "Q3 2026", "theme": "Scale & Harden", "milestones": "HSM first Tier-1 shipment · CYPHERA 30 tenants · AUTOPENTRIX POC #2-3"},
      {"label": "Q4 2026", "theme": "Launch & Grow", "milestones": "HSM ISO 21434 certified · CYPHERA 50 tenants · AUTOPENTRIX GA decision"}
    ],
    "decisions": [
      {"decision": "AUTOPENTRIX build-vs-buy for LLM reasoning layer", "status": "Open", "owner": "CTO", "deadline": "2026-06-15"}
    ],
    "risks": [
      {"risk": "HSM silicon supply chain delay (14-week lead time)", "likelihood": "Medium", "impact": "High", "mitigation": "Dual-source arrangement with two foundries in negotiation."},
      {"risk": "CYPHERA EU data residency compliance gap", "likelihood": "Low", "impact": "Medium", "mitigation": "Legal review in progress; EU region deployment planned Q3."}
    ]
  },
  "products": [
    {
      "id": "prod-hsm-001",
      "type": "hardware",
      "identity": {
        "name": "HSM Security Module",
        "owner": "Dr. Priya Nair",
        "oneLiner": "Automotive-grade hardware security module for key management and secure boot.",
        "vision": "Become the de facto HSM for connected vehicles across EU Tier-1 suppliers by 2028.",
        "currentCustomers": "Pilot with AutoSec GmbH (3 units on test bench); letter of intent from VehicleCorp."
      },
      "technologyReadiness": {"trl": 4, "evidence": "Functional prototype validated in lab environment. FIPS 140-3 Level 3 pre-assessment passed.", "targetTrl": 9, "targetDate": "2026-12-31"},
      "maturity": {"level": 3, "evidence": "Prototype manufacturing process defined. First article inspection complete on 10 units."},
      "commercializationStage": 2,
      "businessStage": "Pre-GA",
      "investment": {"fteCount": 6, "budgetTier": "L", "capacityNotes": "4 HW engineers, 1 firmware, 1 certification specialist. £380K allocated Q2-Q4."},
      "rag": {"status": "A", "reasoning": "Silicon supply chain risk flagged. Dual-source negotiations ongoing; fallback adds 6-week delay."},
      "nextMilestone": {"description": "FIPS 140-3 Level 3 lab test completion and certification submission", "targetDate": "2026-06-30", "owner": "Dr. Priya Nair"},
      "compliance": {
        "iso21434": "in_progress", "aisXXX": "not_started", "uneceR155": "in_progress",
        "certIn": NA, "iso27001": "aligned", "tisax": "not_started",
        "custom": [{"name": "FIPS 140-3 Level 3", "state": "in_progress"}, {"name": "Common Criteria EAL4+", "state": "not_started"}]
      },
      "customerEvidence": [
        {"name": "AutoSec GmbH", "type": "pilot", "since": "2026-02-01", "notes": "3-unit lab evaluation, positive feedback on integration API."},
        {"name": "VehicleCorp", "type": "prospect", "since": "2026-04-10", "notes": "LOI signed; conditional on FIPS cert."}
      ],
      "productRisks": [
        {"risk": "Silicon supply chain delay (14-week lead time)", "likelihood": "M", "impact": "H", "mitigation": "Dual-source arrangement in negotiation."}
      ],
      "productRoadmap": [
        {"title": "FIPS 140-3 lab cert", "targetDate": "2026-06-30", "status": "In progress"},
        {"title": "ISO 21434 audit", "targetDate": "2026-09-30", "status": "Planned"},
        {"title": "First Tier-1 shipment (AutoSec)", "targetDate": "2026-10-15", "status": "Planned"}
      ],
      "createdAt": FIXED_DATE, "updatedAt": FIXED_DATE, "lastEditedBy": "me"
    },
    {
      "id": "prod-cyphera-001",
      "type": "software",
      "identity": {
        "name": "CYPHERA",
        "owner": "James Okafor",
        "oneLiner": "Cloud-native cryptographic key lifecycle management platform for enterprise.",
        "vision": "The Stripe of cryptographic infrastructure — so simple any developer can secure their stack.",
        "currentCustomers": "FinTrust Ltd (paying), SecureLogix (paying), DataVault Co (pilot). 3 total customers."
      },
      "technologyReadiness": {"trl": 6, "evidence": "System prototype demonstrated in operational environment. 99.95% uptime over 90-day pilot.", "targetTrl": 8, "targetDate": "2026-09-30"},
      "maturity": {"level": 3, "evidence": "Limited production deployment with 3 customers. SLAs met. On-call runbook established."},
      "commercializationStage": 4,
      "businessStage": "Beta",
      "investment": {"fteCount": 8, "budgetTier": "L", "capacityNotes": "5 engineers, 2 DevOps, 1 PM. AWS credits + £520K cash budget for FY2026."},
      "rag": {"status": "G", "reasoning": "Ahead of customer acquisition target. EU data residency gap is low risk given Q3 timeline."},
      "nextMilestone": {"description": "Onboard 5 new design-partner customers to reach 10-tenant milestone", "targetDate": "2026-07-15", "owner": "James Okafor"},
      "compliance": {
        "iso21434": NA, "aisXXX": NA, "uneceR155": NA,
        "certIn": "in_progress", "iso27001": "certified", "tisax": NA,
        "custom": [{"name": "SOC 2 Type II", "state": "in_progress"}, {"name": "GDPR Article 32", "state": "aligned"}]
      },
      "customerEvidence": [
        {"name": "FinTrust Ltd", "type": "paid", "since": "2026-01-01", "notes": "Flagship customer. Full KMS workload migrated. NPS 72."},
        {"name": "SecureLogix", "type": "paid", "since": "2026-03-01", "notes": "Certificate automation use case."},
        {"name": "DataVault Co", "type": "pilot", "since": "2026-04-15", "notes": "Evaluating for 50K key/month workload."}
      ],
      "productRisks": [
        {"risk": "EU data residency compliance gap", "likelihood": "L", "impact": "M", "mitigation": "EU region deployment planned Q3 2026."}
      ],
      "productRoadmap": [
        {"title": "10-tenant milestone", "targetDate": "2026-07-15", "status": "In progress"},
        {"title": "EU region deployment", "targetDate": "2026-09-01", "status": "Planned"},
        {"title": "SOC 2 Type II audit", "targetDate": "2026-10-31", "status": "Planned"},
        {"title": "50-tenant GA", "targetDate": "2026-12-31", "status": "Planned"}
      ],
      "createdAt": FIXED_DATE, "updatedAt": FIXED_DATE, "lastEditedBy": "me"
    },
    {
      "id": "prod-autopentrix-001",
      "type": "software",
      "identity": {
        "name": "AUTOPENTRIX",
        "owner": "Selin Çelik",
        "oneLiner": "LLM-powered autonomous penetration testing platform for continuous red-team coverage.",
        "vision": "Every company gets Fortune-500 red-team quality — automated, continuous, affordable.",
        "currentCustomers": "No paying customers yet. Three MSSP partners in POC discussions."
      },
      "technologyReadiness": {"trl": 5, "evidence": "Technology validated in relevant environment. Internal red-team CTF scored 68% find rate vs human team.", "targetTrl": 7, "targetDate": "2026-12-31"},
      "maturity": {"level": 1, "evidence": "Concept-stage OperationalReadiness. Single-tenant prototype only; no multi-tenant or SLA capability yet."},
      "commercializationStage": 1,
      "businessStage": "Concept",
      "investment": {"fteCount": 3, "budgetTier": "S", "capacityNotes": "2 ML engineers, 1 security researcher. £95K seed allocation. LLM API costs ~£8K/month at current scale."},
      "rag": {"status": "A", "reasoning": "ICP not yet confirmed. POC pipeline dependent on MSSP relationship that is early-stage."},
      "nextMilestone": {"description": "First paid POC with RedTeam Inc MSSP partner (scope defined, contract pending)", "targetDate": "2026-06-01", "owner": "Selin Çelik"},
      "compliance": {
        "iso21434": NA, "aisXXX": "not_started", "uneceR155": NA,
        "certIn": NA, "iso27001": "not_started", "tisax": NA,
        "custom": []
      },
      "customerEvidence": [],
      "productRisks": [
        {"risk": "LLM reasoning quality insufficient for complex targets", "likelihood": "M", "impact": "H", "mitigation": "Fine-tuning pipeline in progress; fallback to human-in-loop for complex scopes."},
        {"risk": "Legal liability for autonomous exploitation actions", "likelihood": "L", "impact": "H", "mitigation": "Scope-limiting architecture (no destructive payloads); legal review Q2."}
      ],
      "productRoadmap": [
        {"title": "POC #1 with RedTeam Inc", "targetDate": "2026-06-01", "status": "Planned"},
        {"title": "Multi-tenant architecture", "targetDate": "2026-09-30", "status": "Planned"},
        {"title": "POC #2 and #3", "targetDate": "2026-09-30", "status": "Planned"}
      ],
      "createdAt": FIXED_DATE, "updatedAt": FIXED_DATE, "lastEditedBy": "me"
    }
  ]
}

demo_json = json.dumps(demo, ensure_ascii=False, separators=(',', ':'))

if '</script' in demo_json.lower():
    print("ERROR: JSON contains </script — aborting")
    sys.exit(1)

BOOTSTRAP_IIFE = f"""/* ============================================================
   DEMO BOOTSTRAP — seeds ETTIKSOFT data if localStorage is empty
   Runs before migration; never overwrites existing user data.
   ============================================================ */
(function bootstrap() {{
  try {{
    var _key = 'roadmap-builder.portfolios';
    var _raw = localStorage.getItem(_key);
    var _existing = [];
    try {{ _existing = JSON.parse(_raw || '[]'); }} catch(e) {{}}
    if (!Array.isArray(_existing) || _existing.length === 0) {{
      var _demo = {demo_json};
      localStorage.setItem(_key, JSON.stringify([_demo]));
    }}
  }} catch(e) {{}}
}})();

"""

# Anchor shared across pages that have the migration IIFE
MIGRATION_ANCHOR = '/* ============================================================\n   DATA MODEL MIGRATION'
# Fallback anchor for Tideland-native pages (heatmap, deck, dashboard, product)
LOAD_ANCHOR = 'function loadPortfolios() {'

PAGES = [
    'index.html', 'dashboard.html', 'product.html', 'editor.html',
    'heatmap.html', 'deck.html', 'output.html'
]

errors = []
for fname in PAGES:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'DEMO BOOTSTRAP' in content:
        print(f'  {fname}: bootstrap already present — skipping')
        continue

    injected = False
    if MIGRATION_ANCHOR in content:
        content = content.replace(MIGRATION_ANCHOR, BOOTSTRAP_IIFE + MIGRATION_ANCHOR, 1)
        injected = True
    elif LOAD_ANCHOR in content:
        content = content.replace(LOAD_ANCHOR, BOOTSTRAP_IIFE + LOAD_ANCHOR, 1)
        injected = True

    if injected:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  {fname}: bootstrap injected')
    else:
        errors.append(f'{fname}: no suitable anchor found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print(f'\nAll 7 pages bootstrapped. Demo JSON: {len(demo_json)} bytes.')
