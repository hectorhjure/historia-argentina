#!/usr/bin/env python3
"""
Generador del sitio estático del corpus de historia argentina.

Lee dossier/, dossier/fichas/ y monografias/, y escribe docs/.
Única dependencia externa: pandoc.

    python3 sitio/build.py

Lo que hace que no sea un conversor trivial:
  1. Resuelve los enlaces entre capas. En el markdown, las referencias
     cruzadas se escriben como `10-mujeres.md` o `VID-1774-VALLE-01`
     dentro de code spans. Acá se convierten en enlaces reales, en los
     dos sentidos, sin tocar el markdown.
  2. Construye el panel de incertidumbre recorriendo todo el corpus y
     juntando cada advertencia, cada ficha provisional o debatida y
     cada afirmación marcada [CIRC].
  3. Arma el índice de búsqueda del lado del cliente.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eventos as _eventos   # noqa: E402
import linea as _linea       # noqa: E402
import recorrido as _rec     # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SITIO = RAIZ / "sitio"
SALIDA = RAIZ / "docs"

# ---------------------------------------------------------------- utilidades


def frontmatter(texto):
    """Devuelve (dict, cuerpo). Parser deliberadamente mínimo: el
    frontmatter de este corpus es plano, con listas en línea o con guiones."""
    if not texto.startswith("---\n"):
        return {}, texto
    cierre = texto.find("\n---\n", 4)
    if cierre == -1:
        return {}, texto
    crudo, cuerpo = texto[4:cierre], texto[cierre + 5 :]
    datos, clave = {}, None
    for linea in crudo.split("\n"):
        if not linea.strip():
            continue
        if linea.startswith("  - ") and clave:
            datos.setdefault(clave, [])
            if isinstance(datos[clave], list):
                datos[clave].append(linea[4:].strip())
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", linea)
        if not m:
            continue
        clave, valor = m.group(1), m.group(2).strip()
        if valor.startswith("[") and valor.endswith("]"):
            datos[clave] = [v.strip() for v in valor[1:-1].split(",") if v.strip()]
        elif valor:
            datos[clave] = valor
        else:
            datos[clave] = []
    return datos, cuerpo


def pandoc(markdown):
    r = subprocess.run(
        ["pandoc", "-f", "markdown+pipe_tables+yaml_metadata_block-raw_html",
         "-t", "html5", "--no-highlight"],
        input=markdown, capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:600])
    return r.stdout


def titulo_de(cuerpo, respaldo):
    m = re.search(r"^#\s+(.+)$", cuerpo, re.M)
    return m.group(1).strip() if m else respaldo


RE_NEGRITA = re.compile(r"\*\*(.+?)\*\*", re.S)
RE_CURSIVA = re.compile(r"(?<![\*\w])\*([^\*\n]+?)\*(?!\*)")
RE_TICKS = re.compile(r"`([^`\n]+)`")


def inline_md(s):
    """Convierte el markdown de línea a HTML. El panel de incertidumbre cita
    fragmentos crudos del corpus; sin esto se ven los asteriscos."""
    import html as _h
    s = _h.escape(s, quote=False)
    s = RE_TICKS.sub(r"<code>\1</code>", s)
    s = RE_NEGRITA.sub(r"<strong>\1</strong>", s)
    s = RE_CURSIVA.sub(r"<em>\1</em>", s)
    return s.replace("**", "").strip(" *|—-")


def texto_plano(html):
    t = re.sub(r"<[^>]+>", " ", html)
    t = re.sub(r"&[a-z]+;|&#\d+;", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------ recolección

def recolectar():
    docs = []

    for p in sorted((RAIZ / "dossier").glob("[0-9][0-9]-*.md")):
        fm, cuerpo = frontmatter(p.read_text())
        docs.append({
            "capa": "capitulo", "fuente": p, "slug": p.stem,
            "url": f"capitulos/{p.stem}.html",
            "titulo": titulo_de(cuerpo, p.stem), "fm": fm, "cuerpo": cuerpo,
        })

    for p in sorted((RAIZ / "dossier" / "fichas").glob("*.md")):
        if p.stem in ("README", "RUBRICA"):
            continue
        fm, cuerpo = frontmatter(p.read_text())
        m = re.search(r"\*\*Afirmación\.\*\*\s*(.+?)(?:\n\n|$)", cuerpo, re.S)
        docs.append({
            "capa": "ficha", "fuente": p, "slug": p.stem,
            "url": f"fichas/{p.stem}.html", "titulo": p.stem, "fm": fm,
            "cuerpo": cuerpo,
            "afirmacion": re.sub(r"\s+", " ", m.group(1)).strip() if m else "",
        })

    for p in sorted((RAIZ / "monografias").glob("*.md")):
        if p.stem == "README":
            continue
        fm, cuerpo = frontmatter(p.read_text())
        docs.append({
            "capa": "monografia", "fuente": p, "slug": fm.get("id", p.stem),
            "url": f"monografias/{fm.get('id', p.stem)}.html",
            "titulo": fm.get("titulo") or titulo_de(cuerpo, p.stem),
            "fm": fm, "cuerpo": cuerpo,
        })

    return docs


# ------------------------------------------------- resolución de enlaces

def construir_mapa(docs):
    """Mapa de referencia -> URL. Cubre las tres formas en que el corpus
    se cita a sí mismo: nombre de archivo, id de ficha e id de monografía."""
    mapa = {}
    for d in docs:
        mapa[d["slug"]] = d["url"]
        mapa[d["slug"] + ".md"] = d["url"]
        if d["capa"] == "monografia":
            mapa[d["fuente"].stem] = d["url"]
    # La rúbrica no es una ficha, pero las fichas la citan.
    mapa["RUBRICA"] = mapa["RUBRICA.md"] = "fichas/rubrica.html"
    return mapa


RE_CODE = re.compile(r"<code>([^<>]+)</code>")
RE_HREF = re.compile(r'href="([^"]+\.md)(#[^"]*)?"')


def envolver_tablas(html):
    """Cada tabla en su propio contenedor con scroll horizontal, para que el
    cuerpo de la página nunca se desplace de costado en pantallas chicas.

    El patrón es `<table[^>]*>` y no `<table>` a propósito: pandoc emite
    algunas tablas con atributos (style="width:100%"). Un reemplazo literal
    se saltea esas aperturas pero sí cierra todos los `</table>`, y deja
    `</div>` huérfanos que desbalancean el documento entero."""
    html = re.sub(r"<table[^>]*>", '<div class="tw"><table>', html)
    return html.replace("</table>", "</table></div>")


def resolver(html, mapa, prof):
    """prof = cuántos '../' hacen falta desde esta página hasta la raíz."""
    arriba = "../" * prof

    def de_code(m):
        crudo = m.group(1)
        clave = re.sub(r"#.*$", "", crudo).strip().lstrip("./").split("/")[-1]
        destino = mapa.get(clave) or mapa.get(clave.replace(".md", ""))
        if not destino:
            return m.group(0)
        anc = re.search(r"(#[\w\-.]+)", crudo)
        return (f'<a class="xref" href="{arriba}{destino}{anc.group(1) if anc else ""}">'
                f"<code>{crudo}</code></a>")

    def de_href(m):
        clave = m.group(1).lstrip("./").split("/")[-1]
        destino = mapa.get(clave) or mapa.get(clave.replace(".md", ""))
        return (f'href="{arriba}{destino}{m.group(2) or ""}"' if destino
                else m.group(0))

    html = envolver_tablas(RE_HREF.sub(de_href, html))
    # no linkificar code spans que ya están dentro de un <a>
    partes, salida, dentro = re.split(r"(</?a\b[^>]*>)", html), [], False
    for parte in partes:
        if parte.startswith("<a"):
            dentro = True
        elif parte.startswith("</a"):
            dentro = False
        salida.append(parte if dentro or parte.startswith("<") and len(parte) < 60
                      and parte.endswith(">") and "<" not in parte[1:-1]
                      else (parte if dentro else RE_CODE.sub(de_code, parte)))
    return "".join(salida)


def retrolinks(docs):
    """Quién apunta a quién. Permite mostrar 'referenciado en' al pie."""
    entrantes = {d["slug"]: set() for d in docs}
    claves = {d["slug"] for d in docs} | {d["fuente"].stem for d in docs}
    for d in docs:
        for ref in set(re.findall(r"`([A-Za-z0-9\-.]+(?:\.md)?)`", d["cuerpo"])):
            base = ref.replace(".md", "")
            if base in claves and base != d["slug"] and base != d["fuente"].stem:
                for otro in docs:
                    if base in (otro["slug"], otro["fuente"].stem):
                        entrantes[otro["slug"]].add(d["slug"])
    return entrantes


# ------------------------------------------------ panel de incertidumbre

def incertidumbres(docs):
    """Recorre el corpus y junta todo lo que el propio corpus declara como
    inseguro. Es la vista que ninguna otra síntesis ofrece."""
    filas = []
    for d in docs:
        fm = d["fm"]
        estado, conf = str(fm.get("estado", "")), str(fm.get("confianza", ""))
        tipo = fm.get("tipo", [])
        tipo = tipo if isinstance(tipo, list) else [tipo]

        if d["capa"] == "ficha":
            motivos = []
            if "provisional" in estado:
                motivos.append(("provisional", "Estado provisional"))
            if conf.startswith("baja"):
                motivos.append(("baja", "Confianza baja"))
            if any("debatido" in str(t) for t in tipo):
                motivos.append(("debatido", "Punto debatido"))
            for clase, etiqueta in motivos:
                filas.append({"clase": clase, "etiqueta": etiqueta, "url": d["url"],
                              "origen": d["slug"], "capa": d["capa"],
                              "texto": d.get("afirmacion", "")[:400]})

        for linea in d["cuerpo"].split("\n"):
            l = linea.strip()
            if len(l) < 40:
                continue
            clase = etiqueta = None
            if l.startswith("⚠") or "⚠" in l[:8]:
                clase, etiqueta = "aviso", "Advertencia"
            elif "**no verificada" in l.lower() or "no verificadas**" in l.lower():
                clase, etiqueta = "sincifra", "Cifra no verificada"
            elif "**no leído en directo**" in l:
                clase, etiqueta = "indirecta", "Fuente no leída en directo"
            elif "[CIRC]" in l:
                clase, etiqueta = "circ", "Circula sin respaldo documental"
            if clase:
                limpio = re.sub(r"^(?:[>|\s⚠]|-(?=\s)|\*(?!\*))+", "", l)
                filas.append({"clase": clase, "etiqueta": etiqueta, "url": d["url"],
                              "origen": d["slug"], "capa": d["capa"],
                              "texto": limpio[:400]})
    orden = {"circ": 0, "sincifra": 1, "baja": 2, "provisional": 3,
             "debatido": 4, "indirecta": 5, "aviso": 6}
    filas.sort(key=lambda f: (orden.get(f["clase"], 9), f["origen"]))
    return filas


# ------------------------------------------------------------- plantilla

NAV = [("", "Portada"), ("linea.html", "Línea de tiempo"),
       ("recorridos/", "Recorridos"),
       ("capitulos/", "Capítulos"), ("fichas/", "Fichas"),
       ("monografias/", "Monografías"), ("incertidumbre.html", "Incertidumbre")]


def pagina(titulo, contenido, prof=0, activo="", descripcion="", clase=""):
    arriba = "../" * prof
    nav = "".join(
        f'<a href="{arriba}{h or "index.html"}"'
        f'{" class=\"activo\"" if h.rstrip("/") == activo else ""}>{t}</a>'
        for h, t in NAV)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}{" · Historia argentina" if titulo != "Historia argentina" else ""}</title>
<meta name="description" content="{descripcion}">
<link rel="stylesheet" href="{arriba}assets/estilo.css">
</head>
<body class="{clase}">
<a class="saltar" href="#principal">Saltar al contenido</a>
<header class="barra">
  <a class="marca" href="{arriba}index.html">Historia argentina<span>corpus de trabajo</span></a>
  <nav>{nav}</nav>
  <button id="tema" type="button" aria-label="Cambiar tema">◐</button>
</header>
<main id="principal">
{contenido}
</main>
<footer class="pie">
  <p><strong>Corpus de trabajo, no obra de referencia.</strong> Es una síntesis de fuentes
  secundarias con sus límites declarados. Cada afirmación se cita por su fuente, nunca
  «según el dossier».</p>
  <p class="tenue">Generado desde markdown · <a href="{arriba}incertidumbre.html">Qué no sabemos</a></p>
</footer>
<script src="{arriba}assets/app.js"></script>
</body>
</html>
"""


def badge(texto, clase=""):
    return f'<span class="badge {clase}">{texto}</span>' if texto else ""


def clase_de(valor, prefijo):
    """Primera palabra del valor como sufijo de clase. Un campo vacío devuelve
    cadena vacía en vez de romper el build con IndexError."""
    partes = str(valor or "").split()
    return prefijo + partes[0] if partes else ""


# --------------------------------------------------------------- páginas

def render(docs, mapa, entrantes):
    SALIDA.mkdir(exist_ok=True)
    for sub in ("capitulos", "fichas", "monografias", "assets"):
        (SALIDA / sub).mkdir(exist_ok=True)

    por_slug = {d["slug"]: d for d in docs}

    for d in docs:
        prof = 1
        cuerpo = re.sub(r"^#\s+.+$", "", d["cuerpo"], count=1, flags=re.M)
        html = resolver(pandoc(cuerpo), mapa, prof)
        fm = d["fm"]

        meta = ""
        if d["capa"] == "ficha":
            meta = ("<div class='meta'>"
                    + badge(fm.get("estado", ""), clase_de(fm.get("estado"), "e-"))
                    + badge("confianza " + str(fm.get("confianza", "")),
                            clase_de(fm.get("confianza"), "c-"))
                    + badge(fm.get("periodo", ""), "neutro")
                    + "".join(badge(t, "tema") for t in (fm.get("temas") or []))
                    + "</div>")
        elif d["capa"] == "monografia":
            meta = ("<div class='meta'>" + badge(fm.get("tipo", ""), "neutro")
                    + badge(fm.get("periodo", ""), "neutro")
                    + badge(fm.get("estado", ""), "e-actualizado") + "</div>")

        # "Aparece en estos recorridos": el vínculo inverso. Se calcula desde
        # lo que el recorrido declara en su frontmatter y desde las estaciones
        # que citan explícitamente este documento, no por parecido temático.
        en_rec = ""
        for r in _rec.todos():
            decl = ([r["fm"].get("monografia", "")]
                    + list(r["fm"].get("fichas", []))
                    + list(r["fm"].get("capitulos", [])))
            if d["slug"] not in decl and d["fuente"].stem not in decl:
                continue
            estaciones = [e for e in r["estaciones"]
                          if d["slug"] in e["bloques"].get("sostiene", "")
                          or d["fuente"].stem in e["bloques"].get("sostiene", "")]
            detalle = (", ".join(
                f'<a href="../recorridos/{r["id"]}/{e["n"]}.html">estación {e["n"]}</a>'
                for e in estaciones) if estaciones else "")
            en_rec += (
                f'<aside class="en-recorridos"><h2>Aparece en un recorrido</h2>'
                f'<a href="../recorridos/{r["id"]}/index.html">{r["titulo"]}</a>'
                + (f"<p>Sostiene {detalle}.</p>" if detalle else
                   "<p>Es una de sus fuentes de base.</p>")
                + "</aside>")

        refs = sorted(entrantes.get(d["slug"], set()))
        pie = ""
        if refs:
            enlaces = " · ".join(
                f'<a href="../{por_slug[r]["url"]}">{por_slug[r]["titulo"] if por_slug[r]["capa"]!="ficha" else r}</a>'
                for r in refs if r in por_slug)
            if enlaces:
                pie = f"<aside class='retro'><h2>Referenciado en</h2><p>{enlaces}</p></aside>"

        etiqueta = {"capitulo": "Capítulo", "ficha": "Ficha de evidencia",
                    "monografia": "Monografía"}[d["capa"]]
        art = (f"<article class='lectura {d['capa']}'>"
               f"<p class='kicker'>{etiqueta}</p><h1>{d['titulo']}</h1>"
               f"{meta}{html}{en_rec}{pie}</article>")
        (SALIDA / d["url"]).write_text(
            pagina(d["titulo"], art, prof, d["url"].split("/")[0],
                   d.get("afirmacion", "")[:180]))


def indices(docs, filas, mapa):
    caps = [d for d in docs if d["capa"] == "capitulo"]
    fichas = [d for d in docs if d["capa"] == "ficha"]
    monos = [d for d in docs if d["capa"] == "monografia"]
    palabras = sum(len(d["cuerpo"].split()) for d in docs)
    n_eventos = len(_eventos.todos())
    recs = _rec.todos()

    # ---- portada
    tarjetas = "".join(f"""
      <a class="tarjeta" href="capitulos/{c['slug']}.html">
        <span class="num">{c['slug'][:2]}</span>
        <h3>{c['titulo']}</h3></a>""" for c in caps)

    destacadas = "".join(f"""
      <a class="tarjeta mono" href="{m['url']}">
        <span class="num">{m['fm'].get('tipo','')}</span>
        <h3>{m['titulo']}</h3>
        <p>{texto_plano(pandoc(m['cuerpo']))[:180]}…</p></a>""" for m in monos)

    portada = f"""
<section class="hero">
  <p class="kicker">Corpus de trabajo</p>
  <h1>Historia argentina</h1>
  <p class="bajada">Una síntesis de {palabras:,} palabras construida sobre fuentes
  académicas, con cada afirmación trazada a su origen —y cada límite declarado
  en voz alta.</p>
  <div class="buscador">
    <input id="q" type="search" placeholder="Buscar en las tres capas…"
           autocomplete="off" aria-label="Buscar">
    <div id="resultados" hidden></div>
  </div>
  <div class="cifras">
    <div><strong>{len(caps)}</strong><span>capítulos</span></div>
    <div><strong>{len(fichas)}</strong><span>fichas de evidencia</span></div>
    <div><strong>{len(monos)}</strong><span>monografía{'s' if len(monos)!=1 else ''}</span></div>
    <div><strong>{n_eventos}</strong><span>hechos fechados</span></div>
    <div><strong>{len(filas)}</strong><span>límites declarados</span></div>
  </div>
</section>

<section class="capas">
  <h2>Tres capas, tres modos de consulta</h2>
  <div class="rejilla-capas">
    <div class="capa-card"><span class="etiq">Capa 1 · se lee</span>
      <h3>Síntesis</h3><p>Quince capítulos que explican, contextualizan y discuten.
      Para entender un tema de punta a punta.</p>
      <a href="capitulos/index.html">Ver capítulos →</a></div>
    <div class="capa-card"><span class="etiq">Capa 2 · se busca</span>
      <h3>Evidencia</h3><p>{len(fichas)} fichas autocontenidas. Cada una lleva adentro su
      fuente, su estado de verificación y su límite. Para citar sin equivocarse.</p>
      <a href="fichas/index.html">Explorar fichas →</a></div>
    <div class="capa-card"><span class="etiq">Capa 3 · se profundiza</span>
      <h3>Monografías</h3><p>Desarrollos con aparato de archivo propio. Cuando una
      monografía contradice a un capítulo, <strong>manda la monografía</strong>.</p>
      <a href="monografias/index.html">Ver monografías →</a></div>
  </div>
</section>

<section class="destacado-incert recorrido-destacado">
  <div>
    <p class="kicker">La otra cara</p>
    <h2>{recs[0]['titulo'] if recs else 'Recorridos'}</h2>
    <p>Siete documentos de archivo sobre María Remedios del Valle, de a uno. Cada
    estación separa <strong>lo que el papel dice, lo que se infiere de él y lo que no
    se puede saber</strong>. No es una biografía ni un homenaje: es una lectura de
    archivo.</p>
    <a class="boton" href="recorridos/{recs[0]['id']}/index.html">Empezar el recorrido →</a>
    <a class="enlace-sec" href="recorridos/index.html">Todos los recorridos</a>
  </div>
</section>

<section class="destacado-incert linea-destacada">
  <div>
    <p class="kicker">Vista del corpus</p>
    <h2>Línea de tiempo</h2>
    <p>{n_eventos} hechos fechados en nueve ejes, de 1500 a 2026. <strong>El ancho de
    cada marca es la precisión de su fecha</strong>, no su importancia: lo que se conoce
    al año es una marca fina, lo que se conoce a la década es una banda. Se genera
    leyendo las cronologías del dossier, así que no puede contradecirlas.</p>
    <a class="boton" href="linea.html">Recorrer la línea →</a>
  </div>
</section>

<section class="destacado-incert">
  <div>
    <p class="kicker">Lo que este corpus tiene y otros no</p>
    <h2>Panel de incertidumbre</h2>
    <p>{len(filas)} puntos en los que el corpus declara que no está seguro: cifras sin
    verificar, fuentes leídas de segunda mano, afirmaciones que circulan sin respaldo
    documental y debates abiertos. Reunidos en un solo lugar en vez de escondidos
    en notas al pie.</p>
    <a class="boton" href="incertidumbre.html">Ver qué no sabemos →</a>
  </div>
</section>

<section class="capas"><h2>Monografías</h2>
  <div class="rejilla">{destacadas}</div></section>

<section class="capas"><h2>Capítulos</h2>
  <div class="rejilla">{tarjetas}</div></section>
"""
    (SALIDA / "index.html").write_text(
        pagina("Historia argentina", portada, 0, "",
               "Corpus de historia argentina en tres capas: síntesis, evidencia y monografías.",
               clase="portada"))

    # ---- índice de capítulos
    lista = "".join(f"""
      <a class="fila-cap" href="{c['slug']}.html"><span class="num">{c['slug'][:2]}</span>
      <div><h3>{c['titulo']}</h3>
      <p>{texto_plano(pandoc(re.sub(r'^#.+$','',c['cuerpo'],count=1,flags=re.M)))[:200]}…</p>
      </div></a>""" for c in caps)
    (SALIDA / "capitulos" / "index.html").write_text(
        pagina("Capítulos", f"<article class='lectura'><p class='kicker'>Capa 1 · síntesis</p>"
               f"<h1>Capítulos</h1><div class='lista-cap'>{lista}</div></article>",
               1, "capitulos"))

    # ---- explorador de fichas
    # Mejora progresiva: las fichas se renderizan en el HTML y el JS sólo
    # las filtra ocultándolas. Así funcionan sin JavaScript y las indexan
    # los buscadores, en vez de existir sólo tras ejecutar un script.
    import html as _h
    items, datos = [], []
    for f in fichas:
        fm = f["fm"]
        est = str(fm.get("estado", ""))
        conf = str(fm.get("confianza", "")).split()[0] if fm.get("confianza") else ""
        temas = fm.get("temas") or []
        tipo = fm.get("tipo") or []
        per = str(fm.get("periodo", ""))
        busq = " ".join([f["slug"], f.get("afirmacion", ""), " ".join(map(str, temas)), per])
        datos.append({"id": f["slug"], "est": est, "conf": conf,
                      "temas": temas, "tipo": tipo})
        items.append(
            f'<a class="item-ficha" href="{f["slug"]}.html" data-id="{f["slug"]}"'
            f' data-busq="{_h.escape(busq, quote=True)}">'
            f'<span class="fid">{f["slug"]}</span>'
            f'<p>{_h.escape(f.get("afirmacion", ""))}</p>'
            f'<span class="meta">{badge(est, clase_de(est, "e-"))}'
            f'{badge("confianza " + conf, "c-" + conf) if conf else ""}'
            f'{badge(per, "neutro")}</span></a>')
    listado = "".join(items)
    (SALIDA / "fichas" / "index.html").write_text(
        pagina("Fichas de evidencia", f"""
<article class='lectura ancho'>
<p class='kicker'>Capa 2 · evidencia</p>
<h1>Fichas de evidencia</h1>
<p class="bajada">{len(fichas)} afirmaciones portantes. Cada ficha es autocontenida: lleva
su fuente, su estado de verificación y su límite adentro. <strong>Citá la fuente que la
ficha declara, no «el dossier».</strong></p>
<div class="regla-destacada"><strong><code>confianza</code> mide el respaldo, no el
consenso.</strong> Una afirmación puede ser <code>debatido</code> y <code>alta</code> a la
vez: el hecho está documentado y su interpretación se discute. Los tres campos se asignan
con criterios falsables — <a href="rubrica.html">ver la rúbrica</a>.</div>
<div class="filtros">
  <input id="ff" type="search" placeholder="Filtrar por texto, id o tema…" aria-label="Filtrar fichas">
  <div id="chips" class="chips"></div>
</div>
<p id="conteo" class="tenue">{len(fichas)} fichas</p>
<div id="lista-fichas" class="lista-fichas">{listado}</div>
<p id="vacio" class="tenue" hidden>Ninguna ficha coincide con ese filtro.</p>
</article>
<script>window.FICHAS={json.dumps(datos, ensure_ascii=False)};</script>""",
               1, "fichas"))

    # ---- índice de monografías
    readme_mono = (RAIZ / "monografias" / "README.md").read_text()
    cola = re.search(r"## Cola de trabajo\n(.*?)$", readme_mono, re.S)
    cola_html = resolver(pandoc(cola.group(1)), {}, 1) if cola else ""
    tarj = "".join(f"""
      <a class="tarjeta mono" href="{m['fm'].get('id', m['slug'])}.html">
        <span class="num">{m['fm'].get('id','')}</span><h3>{m['titulo']}</h3>
        <p>{texto_plano(pandoc(m['cuerpo']))[:220]}…</p></a>""" for m in monos)
    (SALIDA / "monografias" / "index.html").write_text(
        pagina("Monografías", f"""
<article class='lectura ancho'><p class='kicker'>Capa 3 · profundidad</p>
<h1>Monografías</h1>
<p class="bajada">Desarrollos en profundidad de un tema por vez, con aparato de archivo
propio. Entre 3.000 y 6.000 palabras, marcado explícito de inferencia y enlace
bidireccional con el capítulo y la ficha correspondientes.</p>
<div class="regla-destacada"><strong>La regla que la justifica:</strong> cuando una
monografía contradice al dossier, <strong>manda la monografía</strong>, y la corrección
se aplica al capítulo en el mismo movimiento. Profundizar sirve para encontrar errores
de la síntesis, no sólo para agregar color.</div>
<div class="rejilla">{tarj}</div>
<h2>Cola de trabajo</h2>{cola_html}</article>""", 1, "monografias"))

    # ---- panel de incertidumbre
    ETIQ = {"circ": "Circula sin respaldo", "sincifra": "Cifra no verificada",
            "baja": "Confianza baja", "provisional": "Estado provisional",
            "debatido": "Punto debatido", "indirecta": "Fuente no leída en directo",
            "aviso": "Advertencia"}
    grupos = ""
    for clase, etiqueta in ETIQ.items():
        grupo = [f for f in filas if f["clase"] == clase]
        if not grupo:
            continue
        items = "".join(
            f"""<li><a href="{f['url']}"><code>{f['origen']}</code></a>
            <p>{inline_md(f['texto'])}</p></li>""" for f in grupo)
        grupos += (f"<section class='grupo-incert i-{clase}'>"
                   f"<h2>{etiqueta} <span class='cuenta'>{len(grupo)}</span></h2>"
                   f"<ul class='incert'>{items}</ul></section>")
    (SALIDA / "incertidumbre.html").write_text(
        pagina("Panel de incertidumbre", f"""
<article class='lectura ancho'><p class='kicker'>Transparencia</p>
<h1>Qué no sabemos</h1>
<p class="bajada">Los {len(filas)} puntos en los que este corpus declara que no está
seguro, reunidos en un solo lugar. Ninguno está escondido en una nota al pie.</p>
<div class="regla-destacada">Publicar tienta a limpiar las admisiones de incertidumbre
para verse mejor. Acá es al revés: <strong>estas marcas son el producto</strong>. Una
síntesis que no puede decir dónde falla no es verificable.</div>
{grupos}</article>""", 0, "incertidumbre.html"))

    # ---- recorridos
    (SALIDA / "recorridos").mkdir(exist_ok=True)
    for r in recs:
        base = SALIDA / "recorridos" / r["id"]
        base.mkdir(exist_ok=True)
        total = len(r["estaciones"])
        prof = 2

        # portada del recorrido
        (base / "index.html").write_text(pagina(
            r["titulo"],
            f"<article class='lectura recorrido'>"
            f"<p class='kicker'>Recorrido · {total} estaciones</p>"
            f"<h1>{r['titulo']}</h1>"
            f"<p class='bajada'>{r['subtitulo']}</p>"
            + resolver(pandoc(r["intro"]), mapa, prof)
            + "<h2>Las estaciones</h2>" + _rec.indice_estaciones(r)
            + _rec.navegacion(r, 0, total)
            + "</article>", prof, "recorridos", r["subtitulo"]))

        # una página por estación
        for e in r["estaciones"]:
            bloques = ""
            for etiqueta, clave, rotulo in _rec.BLOQUES:
                if clave not in e["bloques"]:
                    continue
                html_b = resolver(pandoc(e["bloques"][clave]), mapa, prof)
                bloques += (f"<section class='bloque b-{clave}'>"
                            f"<h2>{rotulo}</h2>{html_b}</section>")
            (base / f"{e['n']}.html").write_text(pagina(
                f"{e['titulo']} · {r['titulo']}",
                f"<article class='lectura recorrido estacion'>"
                f"<p class='kicker'>Estación {e['n']} de {total} · "
                f"<a href='index.html'>{r['titulo']}</a></p>"
                f"<h1>{e['titulo']}</h1>{bloques}"
                + _rec.navegacion(r, e["n"], total)
                + "<details class='otras-est'><summary>Todas las estaciones</summary>"
                + _rec.indice_estaciones(r, e["n"]) + "</details>"
                + "</article>", prof, "recorridos",
                f"Estación {e['n']} de {r['titulo']}: {e['titulo']}"))

        # cierre
        cuerpo_cierre = "".join(
            f"<h2>{tit}</h2>" + resolver(pandoc(txt), mapa, prof)
            for tit, txt in r["cierre"])
        (base / "cierre.html").write_text(pagina(
            f"Cierre · {r['titulo']}",
            f"<article class='lectura recorrido'>"
            f"<p class='kicker'>Cierre · <a href='index.html'>{r['titulo']}</a></p>"
            f"<h1>Después de los siete documentos</h1>{cuerpo_cierre}"
            + _rec.navegacion(r, total + 1, total)
            + "</article>", prof, "recorridos"))

    # índice de recorridos
    tarjetas_rec = "".join(
        f"<a class='tarjeta mono' href='{r['id']}/index.html'>"
        f"<span class='num'>{len(r['estaciones'])} estaciones</span>"
        f"<h3>{r['titulo']}</h3><p>{r['subtitulo']}</p></a>" for r in recs)
    (SALIDA / "recorridos" / "index.html").write_text(pagina(
        "Recorridos", f"""
<article class='lectura ancho'><p class='kicker'>Capa narrativa</p>
<h1>Recorridos</h1>
<p class="bajada">Lecturas guiadas de archivo. Cada estación pone un documento
en el centro y separa tres cosas que se confunden todo el tiempo: lo que el
papel dice, lo que se infiere de él y lo que no se puede saber.</p>
<div class="regla-destacada">Un recorrido no reemplaza al capítulo ni a la ficha:
las <strong>compone y las enlaza</strong>. Y sólo existe aguas abajo de evidencia
ya terminada — no se puede narrar lo que todavía no se investigó.</div>
<div class="rejilla">{tarjetas_rec}</div></article>""", 1, "recorridos"))

    # ---- línea de tiempo del corpus
    evs = _eventos.todos()
    con_ficha = sum(1 for e in evs if e["fichas"])
    con_ancho = sum(1 for e in evs if e["fecha"].extension > 0)
    (SALIDA / "linea.html").write_text(
        pagina("Línea de tiempo del corpus", f"""
<article class='lectura ancho'>
<p class='kicker'>Vista del corpus</p>
<h1>Línea de tiempo del corpus</h1>
<p class="bajada">{len(evs)} hechos extraídos de las cronologías del dossier,
distribuidos en nueve ejes. <strong>El ancho de cada marca es la precisión de su
fecha</strong>, no su importancia.</p>

<div class="regla-destacada">
<strong>Es la línea de tiempo del corpus, no de la historia argentina.</strong>
Un vacío acá significa que <em>este</em> corpus no registró nada en ese punto —no que
no haya pasado nada—. La regla de selección es simple y verificable: se incluye todo
hecho fechado que aparezca en <code>01-timeline-alto-nivel.md</code> o en las
cronologías temáticas de <code>11-timelines-por-categoria.md</code>, y nada más.
<strong>No hay una base de datos aparte:</strong> esta página se genera leyendo esos
dos capítulos, así que no puede contradecirlos.
</div>

<div class="leyenda">
  <span><i class="mu"></i> fecha de un año</span>
  <span><i class="mu ext"></i> la fecha abarca varios años: el ancho es la imprecisión</span>
  <span><i class="mu aprox"></i> fecha aproximada</span>
</div>

{_linea.svg(evs)}

<div class="filtros">
  <input id="fe" type="search" placeholder="Filtrar hechos por texto o año…"
         aria-label="Filtrar hechos">
  <div class="chips">{_linea.chips()}</div>
</div>
<p id="conteo-ev" class="tenue">{len(evs)} hechos</p>

<div id="lista-eventos">
{_linea.lista(evs)}
</div>
<p id="vacio-ev" class="tenue" hidden>Ningún hecho coincide con ese filtro.</p>

<h2>Qué no hace esta página</h2>
<p>No dibuja flechas causales: sólo las habría si el corpus declarara una relación
causal explícita, y hoy casi no lo hace. No tiene mapa, porque los datasets de fronteras
históricas disponibles no cubren 1810-1885 y poner hechos del siglo XIX sobre un mapa
moderno <strong>afirma</strong> una territorialidad que no existía. Y no muestra
densidad documental por eje: esa cifra mediría qué se cargó acá, no qué quedó
registrado en los archivos.</p>
<p class="tenue">De los {len(evs)} hechos, {con_ancho} tienen fecha imprecisa y
{con_ficha} tienen al menos una ficha de evidencia vinculada — el vínculo lo declara
la ficha en su <code>prosa_relacionada</code>, no se infiere por cercanía temporal.</p>
</article>""", 0, "linea.html",
               f"{len(evs)} hechos fechados del corpus de historia argentina, "
               f"con la precisión de cada fecha representada como ancho."))

    # ---- página de la rúbrica
    rub = (RAIZ / "dossier" / "fichas" / "RUBRICA.md").read_text()
    cuerpo_rub = re.sub(r"^#\s+.+$", "", rub, count=1, flags=re.M)
    (SALIDA / "fichas" / "rubrica.html").write_text(
        pagina("Rúbrica de confianza",
               "<article class='lectura'><p class='kicker'>Capa 2 · criterio</p>"
               "<h1>Rúbrica de confianza y estado</h1>"
               + resolver(pandoc(cuerpo_rub), {}, 1) + "</article>",
               1, "fichas",
               "Criterios falsables para los campos de estado, confianza y tipo "
               "de las fichas de evidencia."))

    # ---- índice de búsqueda
    idx = [{"t": d["titulo"], "u": d["url"], "c": d["capa"],
            "x": texto_plano(pandoc(d["cuerpo"]))[:1500]} for d in docs]
    (SALIDA / "assets" / "indice.js").write_text(
        "window.INDICE=" + json.dumps(idx, ensure_ascii=False) + ";")


def main():
    if not shutil.which("pandoc"):
        sys.exit("Falta pandoc. brew install pandoc")
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    docs = recolectar()
    mapa = construir_mapa(docs)
    entr = retrolinks(docs)
    filas = incertidumbres(docs)
    render(docs, mapa, entr)
    indices(docs, filas, mapa)
    for a in (SITIO / "assets").glob("*"):
        shutil.copy(a, SALIDA / "assets" / a.name)
    (SALIDA / ".nojekyll").write_text("")
    n = len(list(SALIDA.rglob("*.html")))
    print(f"✓ {n} páginas · {len(docs)} documentos · {len(filas)} incertidumbres → docs/")


if __name__ == "__main__":
    main()
