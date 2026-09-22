#!/usr/bin/env python3
"""
Dibuja la línea de tiempo del corpus.

Dos vistas de los mismos datos, renderizadas en el servidor:

  1. Un **mapa temporal** en SVG: 1500-2030 por nueve ejes. Da la forma del
     conjunto de un vistazo — dónde se acumulan los hechos y, sobre todo,
     dónde el ancho de una marca delata que la fecha no se conoce con
     precisión.
  2. Una **lista cronológica** con el contenido, que es donde se lee.

El JavaScript sólo filtra ocultando nodos. Sin JS la página sigue completa y
los buscadores la indexan.

**Se llama «línea de tiempo del corpus», nunca «de la historia argentina».**
No es una convención de estilo: un vacío en esta línea significa que el corpus
no registró nada ahí, no que no haya pasado nada.
"""

import html
import re

INICIO, FIN = 1500, 2030
ANCHO, ALTO_EJE, PAD_IZQ, PAD_SUP = 1060, 26, 8, 22

EJES = [
    ("estructural", "Estructural"), ("economico", "Económico"),
    ("violencia", "Violencia"), ("relevante", "Otros hitos"),
    ("educacion", "Educación"), ("salud", "Salud"),
    ("cultura", "Cultura"), ("mujeres", "Mujeres"), ("mundo", "Mundo"),
]

DECADAS_ROTULO = list(range(1500, 2031, 50))


def _x(anio):
    anio = max(INICIO, min(FIN, anio))
    return PAD_IZQ + (anio - INICIO) / (FIN - INICIO) * (ANCHO - PAD_IZQ * 2)


def _empacar(eventos):
    """Reparte los eventos de un eje en sub-filas para que no se pisen.

    Greedy: cada evento va a la primera fila donde entra. Es el «layout de
    colisiones» que justificaría D3 — en una dimensión son doce líneas."""
    filas = []
    for e in sorted(eventos, key=lambda e: e["fecha"].earliest):
        x0, x1 = _x(e["fecha"].earliest), _x(e["fecha"].latest) + 2.5
        for fila in filas:
            if fila[-1][1] <= x0:
                fila.append((x0, x1, e))
                break
        else:
            filas.append([(x0, x1, e)])
    return filas


def svg(eventos):
    por_eje = {k: [e for e in eventos if e["eje"] == k] for k, _ in EJES}
    capas, y = [], PAD_SUP
    guias = []

    for clave, titulo in EJES:
        filas = _empacar(por_eje[clave])
        alto = max(ALTO_EJE, len(filas) * 7 + 10)
        guias.append(f'<text class="eje-rot" x="{PAD_IZQ}" y="{y - 4}">{titulo} '
                     f'<tspan class="eje-n">{len(por_eje[clave])}</tspan></text>')
        marcas = []
        for i, fila in enumerate(filas):
            yy = y + 4 + i * 7
            for x0, x1, e in fila:
                f = e["fecha"]
                ancho = max(2.2, x1 - x0 - 2.5)
                clases = "m"
                if f.extension > 0:
                    clases += " ext"
                if f.aproximada:
                    clases += " aprox"
                if f.incierta:
                    clases += " incierta"
                marcas.append(
                    f'<rect class="{clases}" x="{x0:.1f}" y="{yy:.1f}" '
                    f'width="{ancho:.1f}" height="4.4" rx="1.4" '
                    f'data-ev="{e["id"]}"><title>{html.escape(f.crudo or f.edtf)} — '
                    f'{html.escape(e["titulo"][:110])}</title></rect>')
        capas.append(f'<g class="eje" data-eje="{clave}">' + "".join(guias[-1:])
                     + "".join(marcas) + "</g>")
        y += alto

    alto_total = y + 24
    ticks = "".join(
        f'<line class="tick" x1="{_x(a):.1f}" y1="{PAD_SUP - 12}" '
        f'x2="{_x(a):.1f}" y2="{alto_total - 20}"/>'
        f'<text class="tick-rot" x="{_x(a):.1f}" y="{alto_total - 6}">{a}</text>'
        for a in DECADAS_ROTULO)

    return (f'<svg class="mapa-temporal" viewBox="0 0 {ANCHO} {alto_total}" '
            f'role="img" aria-label="Mapa temporal del corpus, {INICIO} a {FIN}, '
            f'por eje temático" preserveAspectRatio="xMidYMid meet">'
            f'{ticks}{"".join(capas)}</svg>')


def lista(eventos, prof=0):
    """La vista que se lee. Agrupada por medio siglo."""
    arriba = "../" * prof
    grupos, salida = {}, []
    for e in eventos:
        a = e["fecha"].earliest
        grupos.setdefault(max(INICIO, a - (a % 50)) if a >= INICIO else None, []).append(e)

    for corte in sorted(grupos, key=lambda c: (c is not None, c if c else 0)):
        evs = grupos[corte]
        rot = f"{corte}–{corte + 49}" if corte else f"Antes de {INICIO}"
        salida.append(f'<h2 class="corte" data-corte="{corte or 0}">{rot} '
                      f'<span class="cuenta">{len(evs)}</span></h2>')
        salida.append('<ol class="eventos">')
        for e in evs:
            f = e["fecha"]
            marca = ""
            if f.extension > 0:
                marca = f'<span class="rango" title="La fecha abarca {f.extension + 1} años">±</span>'
            elif f.aproximada:
                marca = '<span class="rango" title="Fecha aproximada">~</span>'
            fichas = "".join(
                f'<a class="chip-ficha" href="{arriba}fichas/{x}.html">{x}</a>'
                for x in e["fichas"][:3])
            cita = (f'<span class="cita-ev">{html.escape(e["cita"])}</span>'
                    if e["cita"] else "")
            salida.append(
                f'<li class="ev" data-eje="{e["eje"]}" data-id="{e["id"]}" '
                f'data-busq="{html.escape((e["titulo"] + " " + (f.crudo or "")).lower(), quote=True)}">'
                f'<span class="ev-fecha"><code>{html.escape(f.crudo or f.edtf)}</code>{marca}</span>'
                f'<div class="ev-cuerpo"><p>{html.escape(e["titulo"])}</p>'
                f'<span class="ev-meta"><span class="badge eje-{e["eje"]}">'
                f'{dict(EJES)[e["eje"]]}</span>{cita}{fichas}'
                f'<a class="ev-origen" href="{arriba}{e["destino"]}">origen</a>'
                f'</span></div></li>')
        salida.append("</ol>")
    return "\n".join(salida)


def chips():
    return "".join(
        f'<button class="chip chip-eje" type="button" aria-pressed="false" '
        f'data-eje="{k}">{t}</button>' for k, t in EJES)
