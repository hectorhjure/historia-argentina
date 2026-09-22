#!/usr/bin/env python3
"""
Regenera los índices derivados de las fichas desde su propio frontmatter.

    python3 sitio/indices.py

Por qué existe: `dossier/fichas/README.md` y `chatgpt-project/15-fichas-de-evidencia.md`
duplicaban a mano el estado y la confianza de 66 fichas. Cada corrección dejaba
tres versiones y la que se leía —el índice— era la que quedaba vieja. Es la
"deriva entre corpus y derivados" que la revisión adversarial señaló como la
fragilidad más grave del proyecto.

Ahora hay una sola fuente de verdad: el frontmatter de cada ficha. Todo lo demás
se deriva, y `sitio/qa.py` falla si los derivados no están al día.
"""

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FICHAS = RAIZ / "dossier" / "fichas"

# El prefijo del id decide la sección. El orden es el del dossier.
SECCIONES = [
    ("ECO", "Economía"), ("EST", "Estado y territorio"),
    ("POL", "Política e instituciones"), ("VIO", "Violencia y derechos humanos"),
    ("IDE", "Ideologías"), ("SOC", "Sociedad, educación y salud"),
    ("MUJ", "Mujeres"), ("CUL", "Cultura"), ("INT", "Intereses cruzados"),
    ("MET", "Método y límites"),
]

CABECERA = """# Fichas de evidencia

**Capa recuperable del dossier.** Cada ficha es **autocontenida**: lleva su fuente, su estado de verificación y su límite adentro.

> **Este índice se genera** desde el frontmatter de las fichas (`python3 sitio/indices.py`). No editarlo a mano: se sobreescribe. Los valores de `estado`, `confianza` y `tipo` están definidos en [`RUBRICA.md`](RUBRICA.md) con criterios falsables.

## Cómo usar este archivo

1. **Citá la fuente** que la ficha declara, no "el dossier".
2. **Si dice `Estado: provisional` o `Confianza: baja`, declará el límite.** No es opcional.
3. **Si el tipo incluye `debatido`, presentá el debate**, no una de las posiciones.
4. **Toda cifra se cita con período, universo y fuente**, o no se cita.
5. **`confianza` mide el respaldo, no el consenso.** Una afirmación puede ser `debatido` y `alta` a la vez: el hecho está documentado, su interpretación se discute.
"""


def frontmatter(texto):
    crudo = texto.split("---\n")[1]
    datos, clave = {}, None
    for linea in crudo.split("\n"):
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
            # Clave sin valor en la misma línea: abre una lista con guiones.
            # Sin esta rama, los ítems `  - ...` que siguen se descartan en
            # silencio y `fuentes` queda vacío.
            datos[clave] = []
    return datos


def leer():
    fichas = []
    for p in sorted(FICHAS.glob("*.md")):
        if p.stem in ("README", "RUBRICA"):
            continue
        t = p.read_text()
        fm = frontmatter(t)
        cuerpo = t.split("---\n", 2)[2]
        m = re.search(r"\*\*Afirmación\.\*\*\s*(.+?)(?:\n\n|$)", cuerpo, re.S)
        fm["_id"] = p.stem
        fm["_cuerpo"] = cuerpo
        fm["_afirmacion"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        fichas.append(fm)
    return fichas


def recuentos(fichas):
    def cuenta(clave, transformar=lambda v: [v]):
        acc = {}
        for f in fichas:
            for v in transformar(f.get(clave, "")):
                if v:
                    acc[v] = acc.get(v, 0) + 1
        return dict(sorted(acc.items(), key=lambda kv: -kv[1]))

    return (cuenta("estado"),
            cuenta("confianza", lambda v: [str(v).split()[0]] if v else []),
            cuenta("tipo", lambda v: v if isinstance(v, list) else [v]))


def tabla_recuentos(est, conf, tip):
    filas = ["| Estado | n | | Confianza | n | | Tipo | n |",
             "|---|--:|---|---|--:|---|---|--:|"]
    claves = max(len(est), len(conf), len(tip))
    le, lc, lt = list(est.items()), list(conf.items()), list(tip.items())
    for i in range(claves):
        e = f"{le[i][0]} | {le[i][1]}" if i < len(le) else " | "
        c = f"{lc[i][0]} | {lc[i][1]}" if i < len(lc) else " | "
        t = f"{lt[i][0]} | {lt[i][1]}" if i < len(lt) else " | "
        filas.append(f"| {e} | | {c} | | {t} |")
    return "\n".join(filas)


def generar_readme(fichas):
    est, conf, tip = recuentos(fichas)
    partes = [CABECERA, "", tabla_recuentos(est, conf, tip), ""]
    for prefijo, titulo in SECCIONES:
        grupo = [f for f in fichas if f["_id"].startswith(prefijo)]
        if not grupo:
            continue
        partes.append(f"\n## {titulo}\n")
        partes.append("| Ficha | Período | Estado | Conf. | Tipo | Afirmación |")
        partes.append("|---|---|---|---|---|---|")
        for f in grupo:
            af = f["_afirmacion"]
            if len(af) > 150:
                af = af[:147].rstrip() + "…"
            tipos = f.get("tipo", [])
            tipos = ", ".join(tipos) if isinstance(tipos, list) else str(tipos)
            partes.append(
                f"| [`{f['_id']}`]({f['_id']}.md) | {f.get('periodo','')} | "
                f"{f.get('estado','')} | {f.get('confianza','')} | {tipos} | {af} |")
    return "\n".join(partes) + "\n"


def generar_consolidado(fichas):
    """El archivo único que sube al Proyecto de ChatGPT (límite de 25 archivos)."""
    est, conf, tip = recuentos(fichas)
    partes = [f"# Fichas de evidencia — {len(fichas)} afirmaciones portantes", "",
              "**Capa recuperable del dossier.** Cada ficha es **autocontenida**: "
              "lleva su fuente, su estado de verificación y su límite adentro.", "",
              "> **Generado** desde el frontmatter de las fichas. Los valores de "
              "`estado`, `confianza` y `tipo` siguen una rúbrica con criterios "
              "falsables; `confianza` mide el respaldo, no el consenso, así que una "
              "afirmación puede ser `debatido` y `alta` a la vez.", "",
              tabla_recuentos(est, conf, tip), ""]
    for prefijo, titulo in SECCIONES:
        grupo = [f for f in fichas if f["_id"].startswith(prefijo)]
        if not grupo:
            continue
        partes.append(f"\n---\n\n# {titulo}\n")
        for f in grupo:
            tipos = f.get("tipo", [])
            tipos = ", ".join(tipos) if isinstance(tipos, list) else str(tipos)
            fuentes = f.get("fuentes", [])
            fuentes = " · ".join(fuentes) if isinstance(fuentes, list) else str(fuentes)
            mono = f.get("monografia", "")
            partes.append(f"\n## {f['_id']}\n")
            partes.append(
                f"> **Período:** {f.get('periodo','')} · **Temas:** "
                f"{', '.join(f.get('temas',[])) if isinstance(f.get('temas'),list) else f.get('temas','')} · "
                f"**Tipo:** {tipos} · **Estado:** {f.get('estado','')} · "
                f"**Confianza:** {f.get('confianza','')}\n>\n"
                f"> **Fuentes:** {fuentes}"
                + (f"\n>\n> **Desarrollo completo:** monografía en el archivo 17" if mono else ""))
            partes.append(f["_cuerpo"].strip())
    return "\n".join(partes) + "\n"


def main():
    fichas = leer()
    salidas = {
        FICHAS / "README.md": generar_readme(fichas),
        RAIZ / "chatgpt-project" / "15-fichas-de-evidencia.md": generar_consolidado(fichas),
    }
    cambios = []
    for ruta, contenido in salidas.items():
        antes = ruta.read_text() if ruta.exists() else ""
        if antes != contenido:
            cambios.append(ruta.relative_to(RAIZ))
        ruta.write_text(contenido)

    if "--verificar" in sys.argv:
        if cambios:
            sys.exit("Índices desactualizados: " + ", ".join(map(str, cambios))
                     + "\nCorré: python3 sitio/indices.py")
        print("✓ índices al día")
    else:
        print(f"✓ {len(fichas)} fichas · "
              + (f"regenerados: {', '.join(map(str, cambios))}" if cambios
                 else "sin cambios"))


if __name__ == "__main__":
    main()
