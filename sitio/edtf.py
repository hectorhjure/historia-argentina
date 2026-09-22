#!/usr/bin/env python3
"""
Conversión de la notación histórica en español a EDTF Level 1.

EDTF (Extended Date/Time Format, ISO 8601-2) es el estándar de la Library of
Congress para fechas imprecisas: https://www.loc.gov/standards/datetime/edtf.html

Por qué importa acá: una línea de tiempo que dibuja «c. 1766» como un punto
miente con la misma lógica con la que miente una serie de PIB empalmada. El
corpus prohíbe lo segundo en `14-regimenes-estadisticos.md`; esto evita lo
primero. Cada fecha se convierte en un intervalo `[earliest, latest]` y el
ancho en pantalla es la incertidumbre.

Se adopta el estándar en vez de inventar un vocabulario propio, y de paso el
corpus queda interoperable con Wikidata y con cualquier archivo serio.

    python3 sitio/edtf.py        # corre la batería de pruebas
"""

import re

ROMANOS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def _romano(s):
    s = s.upper().strip()
    if not s or any(c not in ROMANOS for c in s):
        return None
    total, previo = 0, 0
    for c in reversed(s):
        v = ROMANOS[c]
        total = total - v if v < previo else total + v
        previo = max(previo, v)
    return total


class Fecha:
    """Una fecha histórica resuelta a intervalo.

    edtf      — cadena canónica EDTF Level 1
    earliest  — primer año posible (int, negativo para a.C.)
    latest    — último año posible
    aproximada— el «~» de EDTF: el valor es cercano, no exacto
    incierta  — el «?» de EDTF: la atribución misma se pone en duda
    """

    __slots__ = ("edtf", "earliest", "latest", "aproximada", "incierta", "crudo")

    def __init__(self, edtf, earliest, latest, aproximada=False, incierta=False, crudo=""):
        self.edtf, self.earliest, self.latest = edtf, earliest, latest
        self.aproximada, self.incierta, self.crudo = aproximada, incierta, crudo

    @property
    def extension(self):
        return self.latest - self.earliest

    @property
    def puntual(self):
        return self.extension == 0 and not self.aproximada and not self.incierta

    def __repr__(self):
        return (f"Fecha({self.edtf!r}, {self.earliest}..{self.latest}"
                f"{', ~' if self.aproximada else ''}{', ?' if self.incierta else ''})")


def separar(celda):
    """Una celda puede contener varias fechas: «1536 / 1580», «1829-1832 / 1835-1852».
    Devuelve la lista de fragmentos. No parte los rangos con guion."""
    celda = celda.replace("**", "").strip()
    partes = [p.strip() for p in re.split(r"\s+/\s+|\s+y\s+", celda) if p.strip()]
    return partes or [celda]


def parsear(texto):
    """Convierte un fragmento de fecha en `Fecha`, o devuelve None si no entiende.

    Devolver None es deliberado: un evento cuya fecha no se puede resolver no se
    dibuja. Es preferible a inventarle una posición."""
    if not texto:
        return None
    crudo = texto
    t = texto.replace("**", "").strip().strip(".,;")

    aprox = bool(re.search(r"^[~≈]|^c\.\s|^ca\.\s|^hacia\s|^circa\s", t, re.I))
    incierta = "?" in t or t.startswith("¿")
    t = re.sub(r"^[~≈¿]|^c\.\s*|^ca\.\s*|^hacia\s+|^circa\s+", "", t, flags=re.I)
    t = t.replace("?", "").strip()

    ac = bool(re.search(r"a\.?\s?c\.?$|\ba\.?C\.?\b", t, re.I))
    t = re.sub(r"a\.?\s?c\.?$", "", t, flags=re.I).strip()

    def signo(n):
        return -n if ac else n

    # Siglos: «s. XVI», «s. XVI-XVII», «siglo XIX»
    m = re.match(r"^s(?:iglo)?\.?\s*([IVXLCDM]+)(?:\s*[-–]\s*([IVXLCDM]+))?$", t, re.I)
    if m:
        a = _romano(m.group(1))
        b = _romano(m.group(2)) if m.group(2) else a
        if a and b:
            ini, fin = (a - 1) * 100 + 1, b * 100
            if ac:
                ini, fin = -fin, -ini
            return Fecha(f"{ini}/{fin}", ini, fin, aprox, incierta, crudo)
        return None

    # Décadas: sólo con notación explícita («193X», «1930s», «años 30»).
    # Un año suelto NO es una década: «1810» es 1810, no 181X. Exigir la X o la
    # «s» final es lo que separa los dos casos.
    m = re.match(r"^(\d{3})X$", t, re.I) or re.match(r"^(\d{4})s$", t)
    if m:
        base = int(m.group(1)) * 10 if len(m.group(1)) == 3 else int(m.group(1))
        base -= base % 10
        ini, fin = signo(base), signo(base + 9)
        if ini > fin:
            ini, fin = fin, ini
        return Fecha(f"{abs(base) // 10 * (-1 if ac else 1)}X", ini, fin,
                     aprox, incierta, crudo)

    # Rango: «1806-1807», «1976-1983», «1613/1622» (la barra sin espacios
    # significa «uno u otro», que como intervalo es lo mismo).
    m = re.match(r"^(\d{1,5})\s*[-–—/]\s*(\d{1,5})$", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        # Año final abreviado: «1976-83» significa 1976-1983, no el año 83.
        # Se completa con el siglo del año inicial.
        if b < a and len(m.group(2)) <= 2:
            b = (a // 100) * 100 + b
            if b < a:
                b += 100
        if ac:
            a, b = min(-a, -b), max(-a, -b)
        if b < a:
            return None
        return Fecha(f"{a}/{b}", a, b, aprox, incierta, crudo)

    # Año con mes y día: «1813-11-14» ya es EDTF válido
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", t)
    if m:
        a = int(m.group(1))
        return Fecha(t, a, a, aprox, incierta, crudo)

    # Año suelto
    m = re.match(r"^(\d{1,5})$", t)
    if m:
        a = signo(int(m.group(1)))
        sufijo = ("~" if aprox else "") + ("?" if incierta else "")
        return Fecha(f"{a}{sufijo}", a, a, aprox, incierta, crudo)

    return None


def resolver(celda):
    """Todas las fechas de una celda, ya parseadas. Descarta las que no entiende."""
    return [f for f in (parsear(p) for p in separar(celda)) if f]


# --------------------------------------------------------------------- pruebas

PRUEBAS = [
    ("1516",              "1516",        1516,  1516, False, False),
    ("**1810**",          "1810",        1810,  1810, False, False),
    ("1806-1807",         "1806/1807",   1806,  1807, False, False),
    ("1976-1983",         "1976/1983",   1976,  1983, False, False),
    ("s. XVI-XVII",       "1501/1700",   1501,  1700, False, False),
    ("s. XIX",            "1801/1900",   1801,  1900, False, False),
    ("~9000 a.C.",        "-9000~",     -9000, -9000, True,  False),
    ("c. 1766",           "1766~",       1766,  1766, True,  False),
    ("¿1774?",            "1774?",       1774,  1774, False, True),
    ("1960s",             "196X",        1960,  1969, False, False),
    ("1813-11-14",        "1813-11-14",  1813,  1813, False, False),
    ("1613/1622",         "1613/1622",   1613,  1622, False, False),
    ("1976-83",           "1976/1983",   1976,  1983, False, False),
    ("no es una fecha",   None,          None,  None, None,  None),
]


def _probar():
    fallos = 0
    for entrada, edtf, ini, fin, aprox, inc in PRUEBAS:
        r = parsear(entrada)
        if edtf is None:
            ok = r is None
        else:
            ok = (r is not None and r.edtf == edtf and r.earliest == ini
                  and r.latest == fin and r.aproximada == aprox and r.incierta == inc)
        if not ok:
            fallos += 1
            print(f"  ✗ {entrada!r} -> {r!r}   esperado {edtf!r} {ini}..{fin}")
        else:
            print(f"  ✓ {entrada!r:22s} -> {edtf!r}")

    # celdas con varias fechas
    for celda, n in [("1536 / 1580", 2), ("1829-1832 / 1835-1852", 2), ("1810", 1)]:
        r = resolver(celda)
        if len(r) != n:
            fallos += 1
            print(f"  ✗ resolver({celda!r}) devolvió {len(r)}, esperaba {n}")
        else:
            print(f"  ✓ resolver({celda!r:24s}) -> {len(r)} fecha(s)")

    print(f"\n{'✓ EDTF ok' if not fallos else f'{fallos} fallo(s)'}")
    return fallos


def _probar_silencioso():
    """Devuelve la cantidad de fallos sin imprimir. Lo usa `sitio/qa.py`."""
    import io
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        return _probar()


if __name__ == "__main__":
    import sys
    sys.exit(1 if _probar() else 0)
