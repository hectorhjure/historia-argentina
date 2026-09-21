import re, pathlib, collections, json
D = pathlib.Path(__file__).resolve().parent.parent / 'docs' 
VOID = {'br','hr','img','input','meta','link','source','col','area','base','wbr','track','embed','param'}
problemas = []

# 1 · balance de etiquetas
for f in sorted(D.rglob('*.html')):
    h = f.read_text()
    cuerpo = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    cuenta = collections.Counter()
    for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>', cuerpo):
        cierre, tag, auto = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or auto: continue
        cuenta[tag] += -1 if cierre else 1
    desbal = {t:n for t,n in cuenta.items() if n}
    if desbal:
        problemas.append(f"DESBALANCE {f.relative_to(D)}: {desbal}")

# 2 · contraste de botones: toda regla con 'button' debe fijar color
css = (D/'assets/estilo.css').read_text()
for m in re.finditer(r'([^{}]*button[^{}]*)\{([^}]*)\}', css):
    sel, cuerpo = m.group(1).strip(), m.group(2)
    if ':hover' in sel or ':focus' in sel or 'aria-pressed' in sel: continue
    limpio = cuerpo.replace('background-color','').replace('border-color','')
    if 'color:' not in limpio:
        problemas.append(f"CONTRASTE: regla sin color explícito -> {sel}")

# 3 · cifras declaradas vs reales
idx = (D/'index.html').read_text()
reales = {
 'capítulos': len(list((D/'capitulos').glob('[0-9]*.html'))),
 'fichas de evidencia': len([p for p in (D/'fichas').glob('*.html') if p.stem!='index']),
 'monografía': len([p for p in (D/'monografias').glob('*.html') if p.stem!='index']),
}
for etiqueta, real in reales.items():
    m = re.search(r'<strong>(\d+)</strong><span>'+etiqueta, idx)
    if not m: problemas.append(f"CIFRA: no encontré el contador de '{etiqueta}'"); continue
    if int(m.group(1)) != real:
        problemas.append(f"CIFRA: portada dice {m.group(1)} {etiqueta}, reales {real}")

# 4 · enlaces internos rotos
for f in sorted(D.rglob('*.html')):
    for href in re.findall(r'href="([^"#?]+)(?:[#?][^"]*)?"', f.read_text()):
        if href.startswith(('http','mailto:','#')): continue
        if not (f.parent/href).resolve().exists():
            problemas.append(f"ENLACE ROTO {f.relative_to(D)} -> {href}")

# 5 · huérfanos: páginas que nadie enlaza
todas = {str(p.relative_to(D)) for p in D.rglob('*.html')}
enlazadas = set()
for f in D.rglob('*.html'):
    for href in re.findall(r'href="([^"#?]+)', f.read_text()):
        if href.startswith(('http','mailto:')): continue
        try: enlazadas.add(str((f.parent/href).resolve().relative_to(D)))
        except Exception: pass
huerfanas = todas - enlazadas - {'index.html'}
if huerfanas: problemas.append(f"HUÉRFANAS ({len(huerfanas)}): {sorted(huerfanas)[:6]}")

import sys
print(f"páginas: {len(list(D.rglob('*.html')))} · problemas: {len(problemas)}")
for p in problemas[:25]: print("  ✗", p)
if not problemas: print("  ✓ todo limpio")

if problemas:
    sys.exit(f"\n{len(problemas)} problema(s) — no se publica")
