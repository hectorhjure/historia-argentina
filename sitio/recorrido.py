#!/usr/bin/env python3
"""
Recorridos: el documento de archivo como objeto central.

Cada estación es **una página propia con su URL**. No es un detalle técnico:
es lo que vuelve el recorrido citable y lo que hace que funcione sin
JavaScript, con el botón de atrás del navegador y para los buscadores.

El avance es por pasos discretos, no por scroll sincronizado. Para historia
densa el problema no es avanzar: es detenerse, releer, retroceder y citar. El
scroll queda para leer dentro de una estación, nunca para gobernar el relato.

Estructura que se espera del markdown de origen:

    ## Estación N · Título
    ### El documento      → la transcripción y su fuente
    ### La escena         → la prosa de enlace
    ### Sabemos           → lo que el papel dice
    ### Inferimos         → lo que se deduce, enunciado como tal
    ### No sabemos        → lo que el archivo no permite responder
    ### Qué sostiene esta escena  → evidencia enlazada

Las cuatro últimas no son decorativas. Si «Inferimos» y «No sabemos» se
vuelven relleno, el recorrido convierte lagunas del archivo en certeza
afectiva — el error que haría irrelevante todo lo demás.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "recorridos"

BLOQUES = [
    ("El documento", "documento", "Documento"),
    ("La escena", "escena", "La escena"),
    ("Sabemos", "sabemos", "Sabemos"),
    ("Inferimos", "inferimos", "Inferimos"),
    ("No sabemos", "nosabemos", "No sabemos"),
    ("Qué sostiene esta escena", "sostiene", "Qué sostiene esta escena"),
]


def frontmatter(texto):
    if not texto.startswith("---\n"):
        return {}, texto
    cierre = texto.find("\n---\n", 4)
    crudo, cuerpo = texto[4:cierre], texto[cierre + 5:]
    datos = {}
    for linea in crudo.split("\n"):
        m = re.match(r"^([a-z_]+):\s*(.*)$", linea)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        datos[k] = ([x.strip() for x in v[1:-1].split(",") if x.strip()]
                    if v.startswith("[") else v)
    return datos, cuerpo


def leer(path):
    fm, cuerpo = frontmatter(path.read_text())

    partes = re.split(r"^## (?=Estación \d|Otra lectura posible|Qué queda abierto)",
                      cuerpo, flags=re.M)
    intro = partes[0]
    estaciones, cierre = [], []

    for p in partes[1:]:
        titulo = p.split("\n", 1)[0].strip()
        resto = p.split("\n", 1)[1] if "\n" in p else ""
        m = re.match(r"Estación (\d+)\s*·\s*(.+)", titulo)
        if not m:
            cierre.append((titulo, resto))
            continue
        bloques = {}
        trozos = re.split(r"^### ", resto, flags=re.M)
        for tr in trozos[1:]:
            cab = tr.split("\n", 1)[0].strip()
            txt = tr.split("\n", 1)[1] if "\n" in tr else ""
            for etiqueta, clave, _ in BLOQUES:
                if cab.lower().startswith(etiqueta.lower()):
                    bloques[clave] = txt.strip()
        estaciones.append(dict(n=int(m.group(1)), titulo=m.group(2).strip(),
                               bloques=bloques))

    titulo_h1 = re.search(r"^# (.+)$", intro, re.M)
    intro_cuerpo = re.sub(r"^# .+$", "", intro, count=1, flags=re.M).strip()
    return dict(fm=fm, id=fm.get("id", path.stem),
                titulo=fm.get("titulo") or (titulo_h1.group(1) if titulo_h1 else path.stem),
                subtitulo=fm.get("subtitulo", ""), intro=intro_cuerpo,
                estaciones=estaciones, cierre=cierre)


def todos():
    return [leer(p) for p in sorted(DIR.glob("REC-*.md"))]


# ------------------------------------------------------------------ navegación

def navegacion(rec, i, total):
    """i: 0 = portada del recorrido, 1..N estaciones, N+1 = cierre."""
    def url(k):
        return "index.html" if k == 0 else ("cierre.html" if k > total else f"{k}.html")

    ant = (f'<a class="nav-paso prev" href="{url(i - 1)}" rel="prev">'
           f'<span>←</span> Anterior</a>' if i > 0 else
           '<span class="nav-paso vacio"></span>')
    sig = (f'<a class="nav-paso sig" href="{url(i + 1)}" rel="next">'
           f'Siguiente <span>→</span></a>' if i <= total else
           '<span class="nav-paso vacio"></span>')
    if i == 0:
        sig = f'<a class="nav-paso sig destacado" href="1.html" rel="next">Empezar <span>→</span></a>'

    if i == 0:
        progreso = f"{total} estaciones"
    elif i > total:
        progreso = "Cierre"
    else:
        progreso = f"Estación {i} de {total}"

    puntos = "".join(
        f'<a class="punto{" activo" if k == i else ""}" href="{k}.html" '
        f'title="Estación {k}" aria-label="Ir a la estación {k}"'
        f'{" aria-current=\"page\"" if k == i else ""}></a>'
        for k in range(1, total + 1))

    return (f'<nav class="pasos" aria-label="Navegación del recorrido">{ant}'
            f'<span class="progreso">{progreso}<span class="puntos">{puntos}</span></span>'
            f'{sig}</nav>')


def indice_estaciones(rec, actual=None):
    filas = "".join(
        f'<a class="fila-est{" activa" if e["n"] == actual else ""}" href="{e["n"]}.html">'
        f'<span class="num">{e["n"]}</span><span>{e["titulo"]}</span></a>'
        for e in rec["estaciones"])
    return f'<div class="indice-est">{filas}</div>'
