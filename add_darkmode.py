"""add_darkmode.py
Adds a complete dark mode to the Spanish study guide:
1. Inserts [data-theme="dark"] CSS overrides for all color tokens
2. Adds component-specific dark overrides (hardcoded color fixes)
3. Inserts a toggle button in the sidebar-brand area
4. Adds JS to toggle + persist in localStorage + apply on load
"""
import re

PATH = r"C:\Users\danie\OneDrive\Desktop\Claude Code Projects\SPanish Project\spanish_study_guide_reference.html"

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Dark mode CSS ───────────────────────────────────────────────────────
DARK_CSS = """
/* ════════════════════════════════════════════════
   DARK MODE
   ════════════════════════════════════════════════ */
[data-theme="dark"] {
  --bg:         #0F172A;
  --bg-card:    #1E293B;
  --bg-subtle:  #293548;
  --bg-amber:   #1C1A08;
  --bg-indigo:  #1E1B4B;
  --bg-emerald: #042F1E;
  --bg-red:     #1C0A0C;
  --bg-purple:  #1A0E36;
  --bg-slate:   #0F172A;

  --text:       #F1F5F9;
  --text-mid:   #94A3B8;
  --text-soft:  #64748B;

  --indigo:     #818CF8;
  --emerald:    #34D399;
  --amber:      #FCD34D;
  --red:        #F87171;
  --purple:     #A78BFA;
  --slate:      #94A3B8;

  --line:       #334155;

  --shadow-sm: 0 1px 3px rgba(0,0,0,.4), 0 1px 2px rgba(0,0,0,.3);
  --shadow-md: 0 4px 16px rgba(0,0,0,.5);
  --color-scheme: dark;
}

/* ── Component overrides: items with hardcoded light colors ── */

/* rule-body code chips */
[data-theme="dark"] .rule-body code {
  background: rgba(252,211,77,.12);
  color: #FCD34D;
}

/* contrast-table column tints */
[data-theme="dark"] .contrast-table td:nth-child(2) {
  background: rgba(129,140,248,.06);
}
[data-theme="dark"] .contrast-table td:nth-child(3) {
  background: rgba(52,211,153,.06);
}

/* formula-card background */
[data-theme="dark"] .formula-card {
  background: linear-gradient(135deg,#1E1B4B 0%,#1A0E36 100%);
  border-color: #4338CA;
}
[data-theme="dark"] .formula-card .fc-title { color: #818CF8; }

/* fc-slot colors */
[data-theme="dark"] .fc-slot.subj  { background:#042F1E; color:#6EE7B7; border-color:#065F46; }
[data-theme="dark"] .fc-slot.verb  { background:#1E1B4B; color:#A5B4FC; border-color:#3730A3; }
[data-theme="dark"] .fc-slot.aux   { background:#1A0E36; color:#C4B5FD; border-color:#6D28D9; }
[data-theme="dark"] .fc-slot.part  { background:#1C1A08; color:#FCD34D; border-color:#92400E; }
[data-theme="dark"] .fc-slot.obj   { background:#1C1305; color:#FDBA74; border-color:#C2410C; }
[data-theme="dark"] .fc-slot.neg   { background:#1C0A0C; color:#FCA5A5; border-color:#991B1B; }
[data-theme="dark"] .fc-slot.time  { background:#042F1E; color:#6EE7B7; border-color:#065F46; }
[data-theme="dark"] .fc-slot.note  { background:#293548; color:#94A3B8; border-color:#334155; }
[data-theme="dark"] .fc-result     { color:#94A3B8; }
[data-theme="dark"] .fc-plus       { color:#475569; }
[data-theme="dark"] .fc-arrow      { color:#475569; }
[data-theme="dark"] .fc-sep        { color:#475569; }

/* pg-card colors */
[data-theme="dark"] .pg-card.masc { background:#0C1829; border-color:#1D4ED8; }
[data-theme="dark"] .pg-card.fem  { background:#1C0A1C; border-color:#BE185D; }
[data-theme="dark"] .pg-card.a1   { background:#042F1E; border-color:#065F46; }
[data-theme="dark"] .pg-card.a2   { background:#1E1B4B; border-color:#3730A3; }
[data-theme="dark"] .pg-card.b1   { background:#1C0A0C; border-color:#991B1B; }
[data-theme="dark"] .pg-card.pos  { background:#042F1E; border-color:#065F46; }
[data-theme="dark"] .pg-card.neg  { background:#1C0A0C; border-color:#991B1B; }
[data-theme="dark"] .pg-tag       { color:#94A3B8; }
[data-theme="dark"] .pg-es        { color:#F1F5F9; }
[data-theme="dark"] .pg-en        { color:#94A3B8; }
[data-theme="dark"] .pg-ex        { color:#64748B; }

/* ceg-card (vertical conjugation) */
[data-theme="dark"] .ceg-card.ar { background:#042F1E; border-color:#065F46; }
[data-theme="dark"] .ceg-card.er { background:#0C1829; border-color:#1E3A6E; }
[data-theme="dark"] .ceg-card.ir { background:#1A0E36; border-color:#4C1D95; }
[data-theme="dark"] .ceg-card.b1 { background:#1C0A0C; border-color:#991B1B; }
[data-theme="dark"] .ceg-pro     { color:#94A3B8; }
[data-theme="dark"] .ceg-end     { color:#818CF8; }
[data-theme="dark"] .ceg-ex      { color:#64748B; }
[data-theme="dark"] .ceg-header  { color:#64748B; border-bottom-color:#334155; }

/* level badges */
[data-theme="dark"] .level-badge.a1 { background:#042F1E; color:#34D399; }
[data-theme="dark"] .level-badge.a2 { background:#1E1B4B; color:#818CF8; }
[data-theme="dark"] .level-badge.b1 { background:#1C0A0C; color:#F87171; }

/* section-task */
[data-theme="dark"] .section-task {
  background: var(--bg-indigo);
  color: #818CF8;
  border-left-color: #818CF8;
}

/* syl-splitter + sega-dtree widgets */
[data-theme="dark"] .syl-splitter,
[data-theme="dark"] .sega-dtree {
  background: #1E293B;
  border-color: #334155;
}
[data-theme="dark"] .syl-splitter-header,
[data-theme="dark"] .sega-dtree-header {
  background: #293548;
  border-bottom-color: #334155;
}
[data-theme="dark"] .syl-input {
  background: #0F172A;
  border-color: #334155;
  color: #F1F5F9;
}
[data-theme="dark"] .syl-input::placeholder { color: #475569; }
[data-theme="dark"] .dtree-opt {
  background: #293548;
  border-color: #334155;
  color: #F1F5F9;
}
[data-theme="dark"] .dtree-opt:hover,
[data-theme="dark"] .dtree-opt.selected { border-color: #818CF8; background: #1E1B4B; }
[data-theme="dark"] .dtree-q { color: #94A3B8; }
[data-theme="dark"] .dtree-connector { color: #64748B; }

/* nav drill links */
[data-theme="dark"] .nav-drill-link.vocab { color: var(--emerald); }
[data-theme="dark"] .nav-drill-link.conj  { color: var(--amber); }

/* tense timeline */
[data-theme="dark"] .tl-track { background: #334155; }
[data-theme="dark"] .tl-node  { border-color: #334155; background: #1E293B; }
[data-theme="dark"] .tl-label { color: #94A3B8; }

/* ser/estar selector */
[data-theme="dark"] .sesi-option { background: #293548; border-color: #334155; }
[data-theme="dark"] .sesi-option:hover { border-color: #818CF8; }
[data-theme="dark"] .sesi-result { background: #1E293B; border-color: #334155; }

/* stats card */
[data-theme="dark"] .stat-card { background: #1E293B; border-color: #334155; }
[data-theme="dark"] .stat-value { color: #F1F5F9; }
[data-theme="dark"] .stat-label { color: #64748B; }

/* scrollbar */
[data-theme="dark"] .sidebar {
  scrollbar-color: #334155 transparent;
}

/* exam-bar */
[data-theme="dark"] .exam-bar-fill { filter: brightness(.85); }

/* ── Theme toggle button ── */
.theme-toggle {
  position: absolute;
  top: 24px;
  right: 16px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: var(--bg-subtle);
  color: var(--text-soft);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: background .15s, border-color .15s, color .15s;
  flex-shrink: 0;
}
.theme-toggle:hover {
  background: var(--bg-indigo);
  border-color: var(--indigo);
  color: var(--indigo);
}
.sidebar-brand { position: relative; }
"""

if '[data-theme="dark"]' not in content:
    content = content.replace('</style>', DARK_CSS + '\n</style>', 1)
    print("Injected dark mode CSS")

# ── 2. Add toggle button to sidebar-brand ─────────────────────────────────
TOGGLE_BTN = '''<button class="theme-toggle" id="theme-toggle-btn" title="Toggle dark mode" onclick="toggleTheme()">🌙</button>'''

brand_end = content.find('</div>', content.find('class="sidebar-brand"'))
if brand_end != -1 and 'theme-toggle' not in content:
    content = content[:brand_end] + '\n      ' + TOGGLE_BTN + '\n    ' + content[brand_end:]
    print("Added toggle button to sidebar-brand")
else:
    print("WARN: sidebar-brand end not found or toggle already present")

# ── 3. Add JS: toggle, persist, on-load apply ─────────────────────────────
DARK_JS = """
// ── Dark mode ────────────────────────────────────────────────────────────
(function() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (saved === 'dark' || (!saved && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
})();

function toggleTheme() {
  const html  = document.documentElement;
  const btn   = document.getElementById('theme-toggle-btn');
  const isDark = html.getAttribute('data-theme') === 'dark';
  if (isDark) {
    html.removeAttribute('data-theme');
    localStorage.setItem('theme', 'light');
    if (btn) btn.textContent = '🌙';
  } else {
    html.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    if (btn) btn.textContent = '☀️';
  }
}

// Set correct icon on load
document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('theme-toggle-btn');
  if (btn && document.documentElement.getAttribute('data-theme') === 'dark') {
    btn.textContent = '☀️';
  }
});
"""

# Insert JS just before </script> closing or right before the first <script>
# Find the first <script> block after </style>
style_end = content.find('</style>')
script_start = content.find('<script>', style_end)
if script_start != -1 and 'toggleTheme' not in content:
    content = content[:script_start] + '<script>\n' + DARK_JS + '\n</script>\n\n' + content[script_start:]
    print("Injected dark mode JavaScript")
else:
    if 'toggleTheme' in content:
        print("JS already present")
    else:
        print("WARN: script insertion point not found")

# ── Save ───────────────────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Final file size: {len(content):,} bytes")
print("add_darkmode.py done.")
