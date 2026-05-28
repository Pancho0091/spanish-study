"""add_collapsible_nav.py
Rebuilds the sidebar nav with collapsible level groups:
- Each group (A1/A2/Bridge/B1) wraps its links in a .ng-items div
- Clicking the group label collapses/expands the group
- State persisted in localStorage
- Active section's group always auto-expands
- Default state: A1 open, all others collapsed
"""
import re

PATH = r"C:\Users\danie\OneDrive\Desktop\Claude Code Projects\SPanish Project\spanish_study_guide_reference.html"

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. CSS for collapsible groups ──────────────────────────────────────────
COLLAPSE_CSS = """
/* ── Collapsible nav groups ── */
.nav-group { }

.nav-group-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: .12em;
  text-transform: uppercase;
  padding: 14px 20px 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
  transition: color .15s;
}
.nav-group-label:hover { opacity: .8; }

.ng-title { flex: 1; }

.ng-chevron {
  font-size: 11px;
  line-height: 1;
  transition: transform .2s ease;
  margin-left: 6px;
  color: var(--text-soft);
}
.nav-group.collapsed .ng-chevron {
  transform: rotate(-90deg);
}

.ng-items {
  overflow: hidden;
  max-height: 2000px;
  transition: max-height .28s ease;
}
.nav-group.collapsed .ng-items {
  max-height: 0;
}
"""

if '.ng-chevron' not in content:
    # Replace the existing .nav-group-label CSS rule
    old_ngl = """.nav-group-label {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--text-soft);
  padding: 12px 24px 6px;
}"""
    if old_ngl in content:
        content = content.replace(old_ngl, '/* nav-group-label moved to collapsible CSS */', 1)
    content = content.replace('</style>', COLLAPSE_CSS + '\n</style>', 1)
    print("Added collapse CSS")

# ── 2. Define section-to-group mapping ────────────────────────────────────
SEC_TO_GROUP = {
    'n4b': 'a1', 'n4c': 'a1', 'n1': 'a1', 'n2': 'a1',
    'n4':  'a1', 'n4d': 'a1', 'n4e': 'a1', 'n3': 'a1',
    'n5':  'a2', 'n6':  'a2', 'n7':  'a2', 'n8':  'a2',
    'n11b':'a2', 'n10': 'a2', 'n11': 'a2', 'n11c':'a2',
    'n11d':'a2', 'n11e':'a2', 'n9':  'a2',
    'n12': 'bridge', 'n14': 'bridge', 'n13': 'bridge',
    'n16': 'b1', 'n17': 'b1', 'n24': 'b1', 'n19': 'b1',
    'n15': 'b1', 'n21': 'b1', 'n23': 'b1', 'n22': 'b1',
    'n26': 'b1', 'n20': 'b1',
}

# ── 3. Build new nav HTML ─────────────────────────────────────────────────
BADGE_COLORS = {'a1': '#065F46', 'a2': '#3730A3', 'bridge': '#6B21A8', 'b1': '#991B1B'}
BADGE_LABELS = {'a1': 'A1', 'a2': 'A2', 'bridge': 'A2', 'b1': 'B1'}

NAV_TITLES = {
    'n4b':  ('01', 'Género y Número',       'a1'),
    'n4c':  ('02', 'Artículos',             'a1'),
    'n1':   ('03', 'Presente Indicativo',   'a1'),
    'n2':   ('04', 'Ser vs. Estar',         'a1'),
    'n4':   ('05', 'Hay · Había · Habrá',   'a1'),
    'n4d':  ('06', 'Interrogativas',        'a1'),
    'n4e':  ('07', 'Negación Básica',       'a1'),
    'n3':   ('08', 'Acentos · SEGA',        'a1'),
    'n5':   ('09', 'Presente Continuo',     'a2'),
    'n6':   ('10', 'Futuro Próximo',        'a2'),
    'n7':   ('11', 'Pretérito Indefinido',  'a2'),
    'n8':   ('12', 'Pretérito Imperfecto',  'a2'),
    'n11b': ('13', 'Verbos Reflexivos',     'a2'),
    'n10':  ('14', 'Pronombres OD/OI',      'a2'),
    'n11':  ('15', 'Verbos tipo Gustar',    'a2'),
    'n11c': ('16', 'Demostrativos',         'a2'),
    'n11d': ('17', 'Posesivos',             'a2'),
    'n11e': ('18', 'Oraciones con que',     'a2'),
    'n9':   ('19', 'Imperativo',            'a2'),
    'n12':  ('20', 'Por vs. Para',          'bridge'),
    'n14':  ('21', 'Comparativos',          'bridge'),
    'n13':  ('22', 'Infinitivo vs. Que',    'bridge'),
    'n16':  ('23', 'Futuro Simple',         'b1'),
    'n17':  ('24', 'Condicional',           'b1'),
    'n24':  ('25', 'Si Condicional',        'b1'),
    'n19':  ('26', 'Presente Subjuntivo',   'b1'),
    'n15':  ('27', 'Pluscuamperfecto',      'b1'),
    'n21':  ('28', 'Voz Pasiva',            'b1'),
    'n23':  ('29', 'Pronombres Relativos',  'b1'),
    'n22':  ('30', 'Estilo Indirecto',      'b1'),
    'n26':  ('31', 'Pronombres Indefinidos','b1'),
    'n20':  ('32', 'Conectores',            'b1'),
}

def nav_link(sec_id):
    num, title, level = NAV_TITLES[sec_id]
    color = BADGE_COLORS[level]
    badge = BADGE_LABELS[level]
    return (
        f'      <a class="nav-link" href="#{sec_id}">'
        f'<span class="nav-num">{num}</span>{title} '
        f'<span class="level-badge {level}" style="font-size:9px;padding:1px 6px;margin-left:4px">'
        f'{badge}</span></a>\n'
    )

def group_block(group_id, label, color, section_ids, drill_links='', default_open=False):
    state_class = '' if default_open else ' collapsed'
    links = ''.join(nav_link(s) for s in section_ids)
    drills = drill_links
    return (
        f'    <div class="nav-group{state_class}" data-group="{group_id}">\n'
        f'      <div class="nav-group-label" style="color:{color}" onclick="toggleNavGroup(\'{group_id}\')">\n'
        f'        <span class="ng-title">● {label}</span>\n'
        f'        <span class="ng-chevron">▾</span>\n'
        f'      </div>\n'
        f'      <div class="ng-items">\n'
        f'{links}'
        f'{drills}'
        f'      </div>\n'
        f'    </div>\n'
    )

drill_a1 = (
    '      <a class="nav-drill-link vocab" href="#fc-vocab-a1">📋 Vocab Review</a>\n'
    '      <a class="nav-drill-link conj"  href="#fc-a1">⚡ Conjugation Drill</a>\n'
)
drill_a2 = (
    '      <a class="nav-drill-link vocab" href="#fc-vocab-a2">📋 Vocab Review</a>\n'
    '      <a class="nav-drill-link conj"  href="#fc-a2">⚡ Conjugation Drill</a>\n'
)
drill_b1 = (
    '      <a class="nav-drill-link vocab" href="#fc-vocab-b1">📋 Vocab Review</a>\n'
    '      <a class="nav-drill-link conj"  href="#fc-b1">⚡ Conjugation Drill</a>\n'
)

new_nav_inner = (
    group_block('a1',     'Nivel A1',       '#065F46',
                ['n4b','n4c','n1','n2','n4','n4d','n4e','n3'], drill_a1, default_open=True)
    + group_block('a2',   'Nivel A2',       '#3730A3',
                ['n5','n6','n7','n8','n11b','n10','n11','n11c','n11d','n11e','n9'], drill_a2)
    + group_block('bridge','A2 → B1 Bridge','#6B21A8',
                ['n12','n14','n13'])
    + group_block('b1',   'Nivel B1',       '#991B1B',
                ['n16','n17','n24','n19','n15','n21','n23','n22','n26','n20'], drill_b1)
)

new_nav = f'<nav class="sidebar-nav" id="sb-nav-ref">\n{new_nav_inner}  </nav>'

# Replace old nav
old_nav_start = content.find('<nav class="sidebar-nav" id="sb-nav-ref">')
old_nav_end   = content.find('</nav>', old_nav_start) + 6
content = content[:old_nav_start] + new_nav + content[old_nav_end:]
print("Rebuilt nav with collapsible groups")

# ── 4. Add collapse JS ────────────────────────────────────────────────────
COLLAPSE_JS = """
// ── Collapsible sidebar nav ──────────────────────────────────────────────
const _SEC_TO_GROUP = """ + str(SEC_TO_GROUP).replace("'", '"') + """;

function toggleNavGroup(groupId) {
  const group = document.querySelector(`.nav-group[data-group="${groupId}"]`);
  if (!group) return;
  group.classList.toggle('collapsed');
  const state = JSON.parse(localStorage.getItem('navGroupState') || '{}');
  state[groupId] = group.classList.contains('collapsed') ? 0 : 1;
  localStorage.setItem('navGroupState', JSON.stringify(state));
}

function expandGroupForSection(sectionId) {
  const groupId = _SEC_TO_GROUP[sectionId];
  if (!groupId) return;
  const group = document.querySelector(`.nav-group[data-group="${groupId}"]`);
  if (group && group.classList.contains('collapsed')) {
    group.classList.remove('collapsed');
  }
}

// Restore saved group states on load
(function() {
  const state = JSON.parse(localStorage.getItem('navGroupState') || '{}');
  ['a1','a2','bridge','b1'].forEach(function(g) {
    const group = document.querySelector(`.nav-group[data-group="${g}"]`);
    if (!group) return;
    if (g in state) {
      if (state[g] === 0) group.classList.add('collapsed');
      else group.classList.remove('collapsed');
    }
    // Default: a1 open, rest collapsed (only if no saved state)
    if (!(g in state) && g !== 'a1') {
      group.classList.add('collapsed');
    }
  });
})();
"""

# Inject JS before the closing </script> of the observer block
observer_script_idx = content.find('// Sidebar active link on scroll')
script_end = content.find('</script>', observer_script_idx)
if 'toggleNavGroup' not in content:
    content = content[:script_end] + '\n' + COLLAPSE_JS + '\n' + content[script_end:]
    print("Added collapse JS")

# ── 5. Update IntersectionObserver to call expandGroupForSection ──────────
old_active_block = """      if (active) {
        active.classList.add('active');
        // Only scroll sidebar after user has manually scrolled (prevents jump-to-bottom on load)
        if (_navScrollReady) {
          active.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
      }"""
new_active_block = """      if (active) {
        active.classList.add('active');
        expandGroupForSection(entry.target.id);
        // Only scroll sidebar after user has manually scrolled (prevents jump-to-bottom on load)
        if (_navScrollReady) {
          active.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
      }"""
if old_active_block in content:
    content = content.replace(old_active_block, new_active_block, 1)
    print("Updated observer to auto-expand active group")

# ── Save ───────────────────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Saved. File: {len(content):,} bytes")
print("add_collapsible_nav.py done.")
