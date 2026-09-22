import re, pathlib, collections, json, subprocess, sys
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
 'fichas de evidencia': len([p for p in (D/'fichas').glob('*.html')
                             if p.stem not in ('index', 'rubrica')]),
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

# ---------------------------------------------------------------------------
# 6 · Rúbrica de las fichas (dossier/fichas/RUBRICA.md)
# Una rúbrica que no se verifica vuelve a ser impresión editorial en un plazo
# corto. Esto la vuelve exigible.
# ---------------------------------------------------------------------------
RAIZ = D.parent
FICHAS = RAIZ / 'dossier' / 'fichas'

CONFIANZA = {'alta', 'media', 'baja'}
ESTADO    = {'actualizado', 'provisional'}
TIPO      = {'hecho', 'interpretación', 'debatido', 'corrección', 'metodológica'}
INSTITUCIONAL = ['indec', 'bcra', 'ley ', 'leyes ', 'infoleg', 'agn', 'censo',
                 'conadep', 'ruvte', 'diario de sesiones', 'sentencia',
                 'banco mundial', 'deis', 'boletín oficial', 'cabildo',
                 'acuerdos del', 'archivo general', 'cepal', 'familysearch']

def _fm(texto):
    crudo = texto.split('---\n')[1]
    datos, clave = {}, None
    for linea in crudo.split('\n'):
        if linea.startswith('  - ') and clave:
            datos.setdefault(clave, [])
            if isinstance(datos[clave], list):
                datos[clave].append(linea[4:].strip())
            continue
        m = re.match(r'^([a-z_]+):\s*(.*)$', linea)
        if not m:
            continue
        clave, valor = m.group(1), m.group(2).strip()
        if valor.startswith('[') and valor.endswith(']'):
            datos[clave] = [v.strip() for v in valor[1:-1].split(',') if v.strip()]
        elif valor:
            datos[clave] = valor
        else:
            # Clave sin valor en la misma línea: abre una lista con guiones.
            # Sin esta rama, los ítems `  - ...` que siguen se descartan en
            # silencio y `fuentes` queda vacío.
            datos[clave] = []
    return datos

for f in sorted(FICHAS.glob('*.md')):
    if f.stem in ('README', 'RUBRICA'):
        continue
    texto = f.read_text()
    fm = _fm(texto)
    cuerpo = texto.split('---\n', 2)[2]

    # vocabulario
    for nivel in str(fm.get('confianza', '')).replace('·', ' ').split():
        if nivel in CONFIANZA or not nivel.isalpha():
            continue
        if nivel in ('sobre', 'el', 'la', 'aparato', 'documental', 'biografía'):
            continue
        problemas.append(f"RUBRICA {f.stem}: confianza '{nivel}' fuera del vocabulario")
    if fm.get('estado') not in ESTADO:
        problemas.append(f"RUBRICA {f.stem}: estado '{fm.get('estado')}' fuera del vocabulario")
    tipos = fm.get('tipo', [])
    tipos = tipos if isinstance(tipos, list) else [tipos]
    for tp in tipos:
        if tp not in TIPO:
            problemas.append(f"RUBRICA {f.stem}: tipo '{tp}' fuera del vocabulario")

    fuentes = fm.get('fuentes', [])
    fuentes = fuentes if isinstance(fuentes, list) else [fuentes]
    bajo = ' '.join(fuentes).lower()

    # criterio 1 de `alta`: fuente leída en directo o primaria institucional.
    # Las metodológicas están exentas: el corpus es fuente primaria sobre sí mismo.
    if str(fm.get('confianza', '')).startswith('alta') and 'metodológica' not in tipos:
        directas = [s for s in fuentes
                    if 'no leído en directo' not in s and not re.search(r'\bvía\b', s, re.I)]
        if not directas and not any(k in bajo for k in INSTITUCIONAL):
            problemas.append(
                f"RUBRICA {f.stem}: confianza 'alta' sin fuente directa ni "
                f"institucional (criterio 1 de alta)")

    # `debatido` obliga a presentar el debate, no una posición
    if 'debatido' in tipos and not re.search(
            r'debat|discut|disput|controvers|en cambio|frente a|posicion', cuerpo, re.I):
        problemas.append(f"RUBRICA {f.stem}: tipo 'debatido' sin presentar el debate")

# ---------------------------------------------------------------------------
# 7 · Linter de vocabulario teleológico
# El corpus declara estar narrado como historia de decadencia y declara que eso
# es una elección interpretativa. La inmersión amplifica ese sesgo porque reduce
# fricción. Esto lo vuelve un error de build, no una buena intención.
# Excepciones justificadas: marcar la línea con <!-- teleologia-ok: razón -->
# ---------------------------------------------------------------------------
TELEOLOGICO = [
    r'condujo inevitablemente', r'estaba destinad[oa]', r'fracaso anunciado',
    r'desde entonces nunca', r'no pudo sino', r'la decadencia argentina',
    r'era inevitable que', r'el fin de la Argentina', r'irremediablemente',
]
for md in sorted(list((RAIZ / 'dossier').rglob('*.md'))
                 + list((RAIZ / 'monografias').glob('*.md'))):
    if md.stem in ('README', 'RUBRICA'):
        continue
    for n, linea in enumerate(md.read_text().split('\n'), 1):
        if 'teleologia-ok' in linea:
            continue
        for patron in TELEOLOGICO:
            if re.search(patron, linea, re.I):
                problemas.append(
                    f"TELEOLOGÍA {md.relative_to(RAIZ)}:{n}: «{patron}» — "
                    f"reformular o justificar con <!-- teleologia-ok: razón -->")

# ---------------------------------------------------------------------------
# 8 · Índices derivados al día (deriva entre corpus y derivados)
# ---------------------------------------------------------------------------
_r = subprocess.run([sys.executable, str(RAIZ / 'sitio' / 'indices.py'), '--verificar'],
                    capture_output=True, text=True)
if _r.returncode != 0:
    problemas.append('DERIVA: ' + (_r.stderr or _r.stdout).strip().replace('\n', ' / '))


print(f"páginas: {len(list(D.rglob('*.html')))} · problemas: {len(problemas)}")
for p in problemas[:25]: print("  ✗", p)
if not problemas: print("  ✓ todo limpio")

if problemas:
    sys.exit(f"\n{len(problemas)} problema(s) — no se publica")
