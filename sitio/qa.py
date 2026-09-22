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
                 + list((RAIZ / 'monografias').glob('*.md'))
                 + list((RAIZ / 'recorridos').glob('*.md'))):
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



# ---------------------------------------------------------------------------
# 9 · Línea de tiempo: nada se dibuja sin origen verificable
# ---------------------------------------------------------------------------
sys.path.insert(0, str(RAIZ / 'sitio'))
import edtf as _edtf          # noqa: E402
import eventos as _ev         # noqa: E402

if _edtf._probar_silencioso():
    problemas.append('EDTF: la batería de pruebas de sitio/edtf.py falla')

_evs = _ev.todos()
_linea_html = (D / 'linea.html').read_text() if (D / 'linea.html').exists() else ''

# cada hecho tiene fecha resuelta y un capítulo de origen
for e in _evs:
    if e['fecha'] is None:
        problemas.append(f"LÍNEA {e['id']}: sin fecha resuelta")
    if not e.get('destino'):
        problemas.append(f"LÍNEA {e['id']}: sin capítulo de origen — "
                         f"no puede dibujarse un hecho sin procedencia")

# marcas del SVG == hechos de la lista == cifra declarada
_marcas = len(re.findall(r'class="m[^"]*" x=', _linea_html))
_items  = len(re.findall(r'class="ev" data-', _linea_html))
if _linea_html and not (_marcas == _items == len(_evs)):
    problemas.append(f"LÍNEA: descalce — {len(_evs)} hechos extraídos, "
                     f"{_marcas} marcas en el SVG, {_items} en la lista")
# La cifra aparece en dos lugares del texto; las dos tienen que coincidir.
# Si el patrón deja de encontrarla, eso también es un fallo: un chequeo que no
# mira nada pasa siempre.
for _pat, _donde in ((r'class="bajada">\s*(\d+)\s+hechos', 'la bajada'),
                     (r'id="conteo-ev"[^>]*>\s*(\d+)\s+hechos', 'el contador')):
    _m = re.search(_pat, _linea_html)
    if _linea_html and not _m:
        problemas.append(f"LÍNEA: no encuentro la cifra declarada en {_donde} — "
                         f"el chequeo quedó mirando otra cosa")
    elif _m and int(_m.group(1)) != len(_evs):
        problemas.append(f"LÍNEA: {_donde} declara {_m.group(1)} hechos, "
                         f"reales {len(_evs)}")

# el título no debe prometer más de lo que es
if _linea_html and 'línea de tiempo de la historia argentina' in _linea_html.lower():
    problemas.append('LÍNEA: se presenta como línea de tiempo de la historia '
                     'argentina; es del corpus')



# ---------------------------------------------------------------------------
# 10 · Recorridos: la matriz de trazabilidad, ejecutable
# El killer mistake identificado en el debate es publicar un recorrido que haga
# sentir como hecho una inferencia narrativa. Si los bloques epistémicos son
# decorativos, da igual que todo lo demás esté impecable. Esto los vuelve
# obligatorios y verifica que citen evidencia que existe.
# ---------------------------------------------------------------------------
import recorrido as _rc      # noqa: E402

_ids_validos = {f.stem for f in (RAIZ / 'dossier' / 'fichas').glob('*.md')}
_ids_validos |= {f.stem for f in (RAIZ / 'dossier').glob('[0-9][0-9]-*.md')}
_ids_validos |= {re.search(r'^id:\s*(.+)$', f.read_text().split('---')[1], re.M).group(1).strip()
                 for f in (RAIZ / 'monografias').glob('VID-*.md')}

for _r in _rc.todos():
    _tot = len(_r['estaciones'])
    if not _tot:
        problemas.append(f"RECORRIDO {_r['id']}: sin estaciones")
    for _e in _r['estaciones']:
        _b = _e['bloques']
        # los cuatro bloques epistémicos son obligatorios y no pueden ser triviales
        for _clave, _rotulo in (('documento', 'El documento'), ('escena', 'La escena'),
                                ('sabemos', 'Sabemos'), ('inferimos', 'Inferimos'),
                                ('nosabemos', 'No sabemos'),
                                ('sostiene', 'Qué sostiene esta escena')):
            _txt = _b.get(_clave, '').strip()
            if not _txt:
                problemas.append(f"RECORRIDO {_r['id']} est.{_e['n']}: falta «{_rotulo}»")
            elif _clave in ('sabemos', 'nosabemos') and len(_txt) < 40:
                problemas.append(f"RECORRIDO {_r['id']} est.{_e['n']}: «{_rotulo}» es "
                                 f"demasiado breve para no ser decorativo")
        # el documento tiene que declarar su fuente
        if '**Fuente.**' not in _b.get('documento', ''):
            problemas.append(f"RECORRIDO {_r['id']} est.{_e['n']}: el documento no "
                             f"declara su fuente")
        # cero celdas sin respaldo: lo citado tiene que existir
        _citas = re.findall(r'`([A-Za-z0-9\-]+)`', _b.get('sostiene', ''))
        _reales = [c for c in _citas if c in _ids_validos]
        if not _reales:
            problemas.append(f"RECORRIDO {_r['id']} est.{_e['n']}: «Qué sostiene esta "
                             f"escena» no cita ninguna ficha, capítulo ni monografía real")
        for _c in _citas:
            if _c not in _ids_validos and re.match(r'^(MUJ|VID|ECO|POL|EST|SOC|CUL|INT|IDE|VIO|MET|REC)-', _c):
                problemas.append(f"RECORRIDO {_r['id']} est.{_e['n']}: cita «{_c}», "
                                 f"que no existe")

    # la cadena de páginas está completa y navegable
    _base = D / 'recorridos' / _r['id']
    for _n in ['index.html', 'cierre.html'] + [f'{i}.html' for i in range(1, _tot + 1)]:
        if not (_base / _n).exists():
            problemas.append(f"RECORRIDO {_r['id']}: falta la página {_n}")
    # cada estación declara su posición en texto, no sólo en gráfico
    for _i in range(1, _tot + 1):
        _h = (_base / f'{_i}.html').read_text() if (_base / f'{_i}.html').exists() else ''
        if f'Estación {_i} de {_tot}' not in _h:
            problemas.append(f"RECORRIDO {_r['id']} est.{_i}: sin progreso textual")

    # vínculo bidireccional: lo que el recorrido declara tiene que apuntarle de vuelta
    for _fid in list(_r['fm'].get('fichas', [])):
        _fh = D / 'fichas' / f'{_fid}.html'
        if _fh.exists() and 'en-recorridos' not in _fh.read_text():
            problemas.append(f"RECORRIDO {_r['id']}: la ficha {_fid} no muestra "
                             f"«Aparece en un recorrido» — el vínculo quedó en un solo sentido")


print(f"páginas: {len(list(D.rglob('*.html')))} · problemas: {len(problemas)}")
for p in problemas[:25]: print("  ✗", p)
if not problemas: print("  ✓ todo limpio")

if problemas:
    sys.exit(f"\n{len(problemas)} problema(s) — no se publica")
