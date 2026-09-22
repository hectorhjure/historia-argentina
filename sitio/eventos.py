#!/usr/bin/env python3
"""
Extrae los eventos de la línea de tiempo desde la prosa del dossier.

    python3 sitio/eventos.py        # inspección: cuántos, de dónde, con qué fechas

**No hay capa de datos paralela, y es deliberado.** La revisión adversarial
señaló que un `eventos.json` mantenido a mano se convierte en «una segunda
autoridad editorial, peor auditada que el Markdown», y que la deriva entre el
corpus y sus derivados era la fragilidad más grave del proyecto. La respuesta
más fuerte a eso es no tener derivado: los capítulos `01-timeline-alto-nivel`
y `11-timelines-por-categoria` son la única fuente de verdad, y la línea de
tiempo es una **vista** de esa prosa, no un conjunto de datos aparte.

Consecuencia que hay que aceptar: el evento sólo puede llevar los atributos
que la prosa ya declara. No se le inventan coordenadas, ni mecanismos causales,
ni grados de prueba. Si el dato no está escrito, no existe.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edtf import resolver  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DOSSIER = RAIZ / "dossier"

# El marcador del timeline maestro codifica el eje. Es la clasificación del
# autor, ya publicada en el capítulo; acá sólo se lee.
MARCADORES = {
    "●": ("estructural", "Hito estructural"),
    "○": ("relevante", "Hito relevante"),
    "▲": ("violencia", "Violencia política o ruptura institucional"),
    "◆": ("economico", "Hito económico"),
}

# Cronologías en línea del capítulo 11, separadas por «·».
TEMATICAS = {
    "E": ("educacion", "Educación"),
    "F": ("salud", "Salud"),
    "G": ("cultura", "Cultura"),
    "H": ("mujeres", "Mujeres y disidencias"),
    "I": ("mundo", "Relación con el mundo"),
}

ROMANOS_SEC = re.compile(r"^##\s+([IVX]+)\.\s+(.+)$", re.M)


def _limpiar(texto):
    """Quita marcas de markdown dejando el texto legible, y recorta la cita."""
    t = re.sub(r"\[([^\]]*?(?:cap\.|§|\*)[^\]]*?)\]", "", texto)   # citas entre corchetes
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return re.sub(r"\s+", " ", t).strip(" .;·")


def _cita(texto):
    """La referencia entre corchetes, si la fila la trae."""
    m = re.search(r"\[([^\]]+)\]", texto)
    if m and not m.group(1).startswith("http"):
        return _limpiar(m.group(1))
    return ""


def fichas_por_seccion():
    """Fichas que declararon vínculo con una sección del timeline.

    El vínculo lo declara la ficha en `prosa_relacionada`; no se infiere por
    cercanía temporal ni por tema. Una ficha que no lo declaró no se enlaza."""
    mapa = {}
    for p in sorted((DOSSIER / "fichas").glob("*.md")):
        if p.stem in ("README", "RUBRICA"):
            continue
        fm = p.read_text().split("---\n")[1]
        m = re.search(r"^prosa_relacionada:\s*\[(.+?)\]", fm, re.M)
        if not m:
            continue
        for ref in m.group(1).split(","):
            s = re.match(r"\s*01-timeline#([IVX]+)", ref)
            if s:
                mapa.setdefault(s.group(1), []).append(p.stem)
    return mapa


def leer_maestro():
    """Los 115 hechos del timeline maestro, con su eje y su sección."""
    texto = (DOSSIER / "01-timeline-alto-nivel.md").read_text()
    vinculos = fichas_por_seccion()
    eventos, seccion, titulo_sec = [], None, None

    for n, linea in enumerate(texto.split("\n"), 1):
        s = ROMANOS_SEC.match(linea)
        if s:
            seccion, titulo_sec = s.group(1), s.group(2).strip()
            continue
        m = re.match(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", linea)
        if not m or seccion is None:
            continue
        celda_fecha, celda_hecho = m.group(1), m.group(2)
        if set(celda_fecha) <= set("-: ") or celda_fecha.strip() == "Año":
            continue

        marca = next((c for c in celda_hecho if c in MARCADORES), None)
        eje = MARCADORES[marca][0] if marca else "relevante"
        hecho = _limpiar(celda_hecho.replace(marca or "", ""))
        if not hecho:
            continue

        for f in resolver(celda_fecha):
            eventos.append(dict(
                fecha=f, titulo=hecho, eje=eje, seccion=seccion,
                seccion_titulo=titulo_sec, fuente="01-timeline-alto-nivel",
                linea=n, cita=_cita(celda_hecho),
                fichas=vinculos.get(seccion, []),
                destino=f"capitulos/01-timeline-alto-nivel.html",
            ))
    return eventos


def leer_tematicas():
    """Las cronologías temáticas en línea del capítulo 11."""
    texto = (DOSSIER / "11-timelines-por-categoria.md").read_text()
    eventos, actual = [], None

    for n, linea in enumerate(texto.split("\n"), 1):
        s = re.match(r"^##\s+([A-I])\.\s+(.+)$", linea)
        if s:
            actual = TEMATICAS.get(s.group(1))
            continue
        if not actual or not linea.strip() or linea.startswith(("#", "|", ">", "-")):
            continue
        eje, eje_titulo = actual
        for trozo in linea.split("·"):
            trozo = trozo.strip()
            # cada ítem arranca con la fecha y sigue con el hecho
            m = re.match(r"^\**\s*([\d~cs][^\s]*(?:\s*[-–/]\s*\d+)?)\s+(.+)$", trozo)
            if not m:
                continue
            fechas = resolver(m.group(1))
            hecho = _limpiar(m.group(2))
            if not fechas or len(hecho) < 3:
                continue
            for f in fechas:
                eventos.append(dict(
                    fecha=f, titulo=hecho, eje=eje, seccion=eje,
                    seccion_titulo=eje_titulo, fuente="11-timelines-por-categoria",
                    linea=n, cita="", fichas=[],
                    destino="capitulos/11-timelines-por-categoria.html",
                ))
        actual = actual if linea.strip() else None
    return eventos


def _clave(e):
    """Para deduplicar: mismo año de inicio y mismo arranque de título."""
    return (e["fecha"].earliest, re.sub(r"\W+", "", e["titulo"].lower())[:26])


def todos():
    """Eventos de las dos fuentes, deduplicados. Gana el timeline maestro:
    está curado y trae eje, sección y a veces cita."""
    acc = {}
    for e in leer_tematicas() + leer_maestro():
        acc[_clave(e)] = e
    eventos = sorted(acc.values(), key=lambda e: (e["fecha"].earliest, e["fecha"].latest))
    for i, e in enumerate(eventos):
        e["id"] = f"ev{i:03d}"
    return eventos


def main():
    import collections
    evs = todos()
    maestro, tema = leer_maestro(), leer_tematicas()
    print(f"maestro: {len(maestro)} · temáticas: {len(tema)} · "
          f"deduplicados: {len(evs)}\n")

    print("por eje:")
    for eje, n in collections.Counter(e["eje"] for e in evs).most_common():
        print(f"  {eje:14s} {n:3d}")

    print("\npor extensión temporal (el ancho en pantalla):")
    ext = collections.Counter()
    for e in evs:
        d = e["fecha"].extension
        ext["puntual (1 año)" if d == 0 else
            "≤ 5 años" if d <= 5 else
            "≤ 20 años" if d <= 20 else
            "≤ 100 años" if d <= 100 else "> 100 años"] += 1
    for k, n in ext.most_common():
        print(f"  {k:18s} {n:3d}")

    aprox = [e for e in evs if e["fecha"].aproximada]
    print(f"\naproximadas: {len(aprox)} · con ficha vinculada: "
          f"{sum(1 for e in evs if e['fichas'])} · con cita: "
          f"{sum(1 for e in evs if e['cita'])}")
    print(f"rango: {evs[0]['fecha'].earliest} .. {max(e['fecha'].latest for e in evs)}")

    print("\nmuestra:")
    for e in evs[:3] + evs[len(evs) // 2:len(evs) // 2 + 2] + evs[-2:]:
        print(f"  {e['fecha'].edtf:12s} [{e['eje']:11s}] {e['titulo'][:64]}")


if __name__ == "__main__":
    main()
