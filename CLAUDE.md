# Instrucciones del repositorio

Corpus de historia argentina en cuatro capas, publicado como sitio estático en
https://hectorhjure.github.io/historia-argentina/

Este archivo es para quien trabaje el repo con un agente. Lo que sigue no son
preferencias de estilo: cada regla existe porque algo falló sin ella.

---

## Reglas que no se negocian

**1. Se edita el markdown, nunca el HTML.** `docs/` es salida del generador y está
en `.gitignore`. Un cambio hecho ahí se pierde en el próximo build.

**2. Antes de empujar, corré la suite entera.** Si algo falla, el despliegue se
aborta igual — mejor enterarse en local:

```bash
python3 sitio/build.py      # genera docs/ (necesita pandoc)
python3 sitio/qa.py         # 11 familias de chequeos
python3 sitio/a11y.py       # accesibilidad y contraste WCAG
python3 sitio/edtf.py       # pruebas del conversor de fechas
python3 sitio/indices.py    # regenera los índices derivados
```

**3. Toda afirmación declara su fuente.** «Según el dossier» no es una fuente: el
dossier es una síntesis de fuentes. Las fichas llevan la suya adentro.

**4. Toda cifra lleva período, universo y fuente, o no se cita.** Está en
`dossier/14-regimenes-estadisticos.md` con las tres prohibiciones concretas. Las
series argentinas **no se encadenan**: las bases del PIB cambian siete veces, la
EPH cambia en 2003, la pobreza no se publicó en 2014-2015.

**5. Las marcas de incertidumbre no se suavizan.** Las ⚠, los `[CIRC]`, los «no
verificada» y los `confianza: baja` son el producto, no un defecto de
presentación. Si un cambio obligara a sacrificar una fuente o una advertencia,
preguntá antes: la respuesta conocida es dejarlo privado.

**6. Un chequeo nuevo se prueba rompiendo lo que vigila.** Un chequeo que nunca
dispara es indistinguible de uno que pasa. En este repo, cuatro chequeos recién
escritos daban verde por estar mirando la cosa equivocada — incluido uno cuyo
parser descartaba en silencio todas las fuentes y ya había vaciado un archivo
publicado. Romper, verificar que falla, restaurar, verificar que pasa.

**7. Cuando un chequeo falle, sospechá primero del chequeo.** De 19 hallazgos de
la auditoría de accesibilidad, 15 eran bugs del auditor.

---

## Decisiones cerradas — no reabrir sin motivo nuevo

Se discutieron en dos debates adversariales contra Codex (`debate/` y
`debate-experiencia/`). Reabrirlas cuesta días y ya tienen respuesta.

| Decisión | Por qué |
|---|---|
| **Sin capa de datos paralela.** La línea de tiempo se deriva de la prosa en tiempo de build | Un `eventos.json` a mano es «una segunda autoridad editorial, peor auditada que el Markdown». Sin derivado no hay deriva |
| **EDTF Level 1** para fechas, no un vocabulario propio | La Library of Congress ya resolvió el problema, y deja el corpus interoperable con Wikidata |
| **Sin framework.** Vainilla hasta ~500 nodos mutables; `d3-scale`/`d3-array` sueltos entre 500 y 2.000 | Las interacciones son triviales. El sitio no tiene toolchain y eso es durabilidad, no pobreza |
| **Sin mapa** | CShapes cubre 1886-2017 y el problema argentino interesante es 1810-1885. Un mapa moderno con hechos de 1813 *afirma* una territorialidad que no existía, y contradice `13-estado-y-territorio` |
| **Sin flechas causales** en la línea de tiempo | Sólo existirían si el corpus declarara relaciones causales explícitas. Hoy casi no lo hace |
| **Sin franja de densidad documental** | Mediría lo que se cargó acá, no lo que quedó en los archivos. Puede volver como *ledger de cobertura* con denominador declarado |
| **Sin cortes transversales** («¿qué pasaba en 1913?») | Cada año es una monografía de comparabilidad en cuatro dominios |
| **Sin facsímiles**, sólo transcripciones | Licencias sin verificar. La transcripción además suele ser más legible |
| **Pasos discretos, no scroll secuestrado** | Para historia densa el problema no es avanzar: es detenerse, releer y citar |
| **Un recorrido va aguas abajo de evidencia terminada** | No se narra lo que no se investigó. Por eso el primero fue Valle: ya tenía monografía |

## El error que haría irrelevante todo lo demás

> **Publicar algo que haga sentir como hecho una inferencia narrativa.**

Si los bloques «inferimos» y «no sabemos» se vuelven decorativos, la experiencia
convierte lagunas del archivo en certeza afectiva. Es exactamente la operación
que produjo ochenta años de «supuestas verdades» sobre María Remedios del Valle,
y repetirla en el sitio que la denuncia sería el fracaso más completo.

`sitio/qa.py` lo defiende con dos chequeos: bloques epistémicos obligatorios y no
triviales, y **deriva narrativa** —todo anclaje factual de la prosa de un
recorrido tiene que aparecer en la monografía de la que deriva—.

---

## Dónde vive cada cosa

| | |
|---|---|
| `dossier/00`-`14` | Síntesis, 15 capítulos |
| `dossier/fichas/` | 66 fichas de evidencia + `RUBRICA.md` con los criterios falsables |
| `monografias/` | Profundidad con aparato de archivo |
| `recorridos/` | Capa narrativa, el documento como objeto central |
| `sitio/` | Generador, QA, accesibilidad, conversor EDTF |
| `chatgpt-project/` | Paquete de 19 archivos para el Proyecto de ChatGPT |
| `debate/`, `debate-experiencia/` | Traza de los debates contra Codex |

**Al tocar fichas o capítulos**, `chatgpt-project/` se regenera con
`sitio/indices.py`, pero **subirlo al Proyecto de ChatGPT es manual y lo hace
Héctor**. Decile siempre qué archivos conviene resubir.

## Lo que sólo puede hacer Héctor

- **Correr el benchmark** de `benchmark-40.md` en su Proyecto de ChatGPT.
- **La prueba de lectura auditable** (fase 5): 12 lectores, umbral 9/12.
- **Resubir archivos** al Proyecto de ChatGPT.
