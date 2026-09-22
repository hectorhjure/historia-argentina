#!/usr/bin/env python3
"""
Auditoría de accesibilidad del sitio.

    python3 sitio/a11y.py

Lo que comprueba, y por qué cada cosa:

1. **Contraste real, calculado.** No «se ve bien»: la razón de contraste WCAG
   de cada par texto/fondo, en los dos temas. Un token que en claro pasa puede
   fallar en oscuro, y al revés.
2. **Jerarquía de encabezados.** Un `h3` después de un `h1` rompe la navegación
   por encabezados, que es cómo se lee una página con lector de pantalla.
3. **Un solo `h1` por página** y los landmarks presentes.
4. **Tamaño de los blancos táctiles**: 44×44 px es el mínimo de WCAG 2.5.5.
5. **Texto de enlace ambiguo.** Trescientos enlaces que dicen «origen» son
   trescientos enlaces indistinguibles fuera de contexto.
6. **Foco visible.** Si se quita el `outline` y no se pone nada, la navegación
   por teclado queda a ciegas.
7. **Desborde horizontal**: nada con ancho mínimo mayor que la pantalla.
8. **`prefers-reduced-motion`** respetado.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
D = RAIZ / "docs"

# ------------------------------------------------------------------ contraste


def _lum(hexcolor):
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contraste(a, b):
    la, lb = _lum(a), _lum(b)
    claro, oscuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (oscuro + 0.05)


def tokens(css, bloque):
    """Variables --x:#hex de TODOS los bloques que coincidan con el selector.

    Tiene que ser `finditer` y no `search`: la hoja declara el mismo selector
    más de una vez (la paleta base y, más abajo, los colores de los ejes). Con
    `search` sólo se leía el primero, el tema oscuro quedaba con los colores
    claros y el auditor inventaba quince fallos de contraste que no existían."""
    acc = {}
    for m in re.finditer(re.escape(bloque) + r"\s*\{(.*?)\}", css, re.S):
        acc.update(dict(re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})", m.group(1))))
    return acc


# Pares que de verdad se pintan juntos en el sitio.
PARES = [
    ("tinta", "papel", 4.5, "texto de lectura sobre el fondo"),
    ("tinta-2", "papel", 4.5, "texto secundario sobre el fondo"),
    ("tinta-2", "papel-2", 4.5, "texto secundario sobre tarjeta"),
    ("tinta-3", "papel", 3.0, "texto tenue sobre el fondo"),
    ("tinta-3", "papel-2", 3.0, "texto tenue sobre tarjeta"),
    ("acento", "papel", 4.5, "enlaces sobre el fondo"),
    ("acento", "papel-2", 4.5, "enlaces sobre tarjeta"),
    ("papel", "acento", 4.5, "texto del botón primario"),
    ("ok", "ok-bg", 4.5, "insignia de confianza alta"),
    ("duda", "duda-bg", 4.5, "insignia de confianza media"),
    ("alerta", "alerta-bg", 4.5, "insignia de confianza baja"),
    ("frio", "frio-bg", 4.5, "insignia informativa"),
    ("e-estructural", "papel-2", 3.0, "eje estructural en el mapa"),
    ("e-economico", "papel-2", 3.0, "eje económico en el mapa"),
    ("e-violencia", "papel-2", 3.0, "eje violencia en el mapa"),
    ("e-relevante", "papel-2", 3.0, "eje otros hitos en el mapa"),
    ("e-educacion", "papel-2", 3.0, "eje educación en el mapa"),
    ("e-salud", "papel-2", 3.0, "eje salud en el mapa"),
    ("e-cultura", "papel-2", 3.0, "eje cultura en el mapa"),
    ("e-mujeres", "papel-2", 3.0, "eje mujeres en el mapa"),
    ("e-mundo", "papel-2", 3.0, "eje mundo en el mapa"),
    ("papel", "e-estructural", 4.5, "texto de la insignia de eje estructural"),
    ("papel", "e-economico", 4.5, "texto de la insignia de eje económico"),
    ("papel", "e-violencia", 4.5, "texto de la insignia de eje violencia"),
    ("papel", "e-relevante", 4.5, "texto de la insignia de eje otros"),
    ("papel", "e-educacion", 4.5, "texto de la insignia de eje educación"),
    ("papel", "e-salud", 4.5, "texto de la insignia de eje salud"),
    ("papel", "e-cultura", 4.5, "texto de la insignia de eje cultura"),
    ("papel", "e-mujeres", 4.5, "texto de la insignia de eje mujeres"),
    ("papel", "e-mundo", 4.5, "texto de la insignia de eje mundo"),
]


def revisar_contraste(problemas):
    css = (D / "assets" / "estilo.css").read_text()
    claro = tokens(css, ":root")
    oscuro = dict(claro)
    oscuro.update(tokens(css, ':root[data-theme="dark"]'))

    for nombre, paleta in (("claro", claro), ("oscuro", oscuro)):
        for frente, fondo, minimo, que in PARES:
            if frente not in paleta or fondo not in paleta:
                problemas.append(f"A11Y contraste: falta el token --{frente} o "
                                 f"--{fondo} en el tema {nombre}")
                continue
            r = contraste(paleta[frente], paleta[fondo])
            if r < minimo:
                problemas.append(
                    f"A11Y contraste {nombre}: {que} da {r:.2f}:1, "
                    f"mínimo {minimo}:1 (--{frente} sobre --{fondo})")
    return claro, oscuro


# --------------------------------------------------------------------- páginas

def revisar_paginas(problemas):
    generico = {"origen", "acá", "aquí", "leer más", "ver más", "más", "link",
                "este enlace", "click", "ver"}
    for f in sorted(D.rglob("*.html")):
        rel = f.relative_to(D)
        h = f.read_text()
        cuerpo = re.sub(r"<script.*?</script>|<!--.*?-->", "", h, flags=re.S)

        if 'lang="es"' not in h:
            problemas.append(f"A11Y {rel}: falta lang en <html>")
        for marca, etiqueta in (("<main", "main"), ("<header", "header"),
                                ("<footer", "footer"), ("<nav", "nav")):
            if marca not in cuerpo:
                problemas.append(f"A11Y {rel}: sin landmark <{etiqueta}>")

        h1 = re.findall(r"<h1[^>]*>", cuerpo)
        if len(h1) != 1:
            problemas.append(f"A11Y {rel}: {len(h1)} elementos h1 (debe haber 1)")

        # jerarquía: no saltar niveles
        niveles = [int(m.group(1)) for m in re.finditer(r"<h([1-6])\b", cuerpo)]
        previo = 0
        for n in niveles:
            if previo and n > previo + 1:
                problemas.append(f"A11Y {rel}: salto de h{previo} a h{n}")
                break
            previo = n

        # texto de enlace ambiguo y repetido
        textos = {}
        for m in re.finditer(r"<a\b([^>]*)>(.*?)</a>", cuerpo, re.S):
            attrs, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
            txt = re.sub(r"\s+", " ", txt).strip().lower()
            if not txt or "aria-label" in attrs:
                continue
            if txt in generico:
                textos[txt] = textos.get(txt, 0) + 1
        for txt, n in textos.items():
            if n > 2:
                problemas.append(f"A11Y {rel}: «{txt}» se repite en {n} enlaces "
                                 f"sin aria-label que los distinga")

        # tablas con encabezados
        for tabla in re.findall(r"<table.*?</table>", cuerpo, re.S):
            if "<th" not in tabla:
                problemas.append(f"A11Y {rel}: tabla sin <th>")
                break


# ------------------------------------------------------------------------ css

def revisar_css(problemas):
    css = (D / "assets" / "estilo.css").read_text()

    if "prefers-reduced-motion" not in css:
        problemas.append("A11Y: no se respeta prefers-reduced-motion")

    # foco visible: si se anula el outline hay que reponer algo
    for m in re.finditer(r"([^{}]+)\{([^}]*outline\s*:\s*(?:none|0)[^}]*)\}", css):
        if not re.search(r"box-shadow|border|background", m.group(2)):
            problemas.append(f"A11Y foco: {m.group(1).strip()} anula el outline "
                             f"sin reponer una señal visible")
    if ":focus" not in css and ":focus-visible" not in css:
        problemas.append("A11Y foco: ninguna regla define el estado de foco")

    # Blancos táctiles. Dos umbrales distintos a propósito: WCAG 2.2 exige
    # 24x24 px (criterio 2.5.8, nivel AA) y recomienda 44x44 (2.5.5, AAA).
    # Los controles del recorrido son el camino principal de lectura y van al
    # umbral alto; el conmutador de tema es secundario y va al de AA con margen.
    for sel, minimo in (("#tema", 32), (".nav-paso", 44)):
        m = re.search(re.escape(sel) + r"\s*\{([^}]*)\}", css)
        if not m:
            continue
        alto = re.search(r"(?:min-height|height)\s*:\s*([\d.]+)(px|rem)", m.group(1))
        if not alto:
            problemas.append(f"A11Y táctil: {sel} no declara alto mínimo")
            continue
        px = float(alto.group(1)) * (16 if alto.group(2) == "rem" else 1)
        if px < minimo:
            problemas.append(f"A11Y táctil: {sel} mide {px:.0f}px, mínimo {minimo}px")

    # Ancho mínimo mayor que una pantalla angosta. Se permite —tablas, gráficos
    # y bloques de código lo necesitan— pero sólo dentro de un contenedor que se
    # desplace Y que avise. Ocultar el desborde sin señal es peor que el
    # desborde: el lector no sabe que hay más contenido, y con una rueda
    # vertical no puede llegar a él.
    desplazables = set(re.findall(r"\.([\w-]+)[^{}]*\{[^}]*overflow-x\s*:\s*auto", css))
    # Las señales se buscan como CLASES, no como subcadenas: "flecha" aparecía
    # en la prosa de la página («no dibuja flechas causales») y hacía pasar el
    # chequeo por una coincidencia de texto corriente.
    SEÑALES = ("borde-izq", "borde-der", "aviso-scroll", "flecha-scroll")

    def _tiene_señal(html):
        clases = " ".join(re.findall(r'class="([^"]*)"', html)).split()
        return any(s in clases for s in SEÑALES)

    for m in re.finditer(r"([^{}]+)\{([^}]*min-width\s*:\s*([\d.]+)px[^}]*)\}", css):
        sel, ancho = m.group(1).strip(), float(m.group(3))
        if ancho <= 380 or "@media" in sel:
            continue
        clases = set(re.findall(r"\.([\w-]+)", sel))
        if not (clases & desplazables):
            problemas.append(f"A11Y desborde: {sel} fija min-width {ancho:.0f}px "
                             f"y no está dentro de un contenedor con overflow-x")
            continue
        # las señales se verifican donde importan: en el HTML servido
        contenedor = (clases & desplazables).pop()
        paginas = [f for f in D.rglob("*.html") if contenedor in f.read_text()]
        sin_señal = [f.relative_to(D) for f in paginas
                     if not _tiene_señal(f.read_text())]
        if sin_señal:
            problemas.append(f"A11Y desborde: .{contenedor} se desplaza sin avisar en "
                             f"{', '.join(map(str, sin_señal[:3]))} — hace falta "
                             f"degradado, flechas o aviso textual")
        elif not paginas:
            problemas.append(f"A11Y desborde: .{contenedor} no aparece en ninguna "
                             f"página — el chequeo quedó mirando otra cosa")


def main():
    problemas = []
    if not D.exists():
        sys.exit("Falta docs/. Corré primero: python3 sitio/build.py")
    claro, oscuro = revisar_contraste(problemas)
    revisar_paginas(problemas)
    revisar_css(problemas)

    print(f"páginas auditadas: {len(list(D.rglob('*.html')))} · "
          f"tokens: {len(claro)} claro / {len(oscuro)} oscuro · "
          f"problemas: {len(problemas)}")
    for p in problemas:
        print("  ✗", p)
    if not problemas:
        print("  ✓ sin hallazgos")
    return len(problemas)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
