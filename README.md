# Historia argentina y del mundo — base de investigación

Este directorio prepara materiales para el Proyecto de ChatGPT **Historia argentina y del mundo**.

No contiene copias de libros. `fuentes-iniciales.md` es un catálogo de títulos disponibles localmente y de cómo usarlos críticamente.

**Sitio publicado:** https://hectorhjure.github.io/historia-argentina/

## Cómo se publica

El sitio se reconstruye solo en cada push a `main` (`.github/workflows/publicar.yml`).
**No hay paso manual y `docs/` no se versiona:** la versión publicada de este corpus ya
quedó desactualizada una vez, y el modo de evitar que vuelva a pasar es que nadie tenga
que acordarse de reconstruirla.

Para trabajar en local:

```bash
python3 sitio/build.py     # genera docs/ (requiere pandoc)
python3 sitio/qa.py        # balance de etiquetas, enlaces rotos, cifras, huérfanas
python3 -m http.server -d docs 8000
```

`sitio/qa.py` también corre en CI y **aborta el despliegue si falla**. Encontró dos bugs
antes de que se publicara nada: 55 tablas sin contenedor de scroll y 86 enlaces rotos
al pie.

Se edita **el markdown**, nunca el HTML. Las referencias cruzadas se escriben como
`` `10-mujeres.md` `` o `` `VID-1774-VALLE-01` `` y el generador las convierte en
enlaces reales en ambos sentidos.

## Contenido

### Método y catálogo de fuentes
- `instrucciones-del-proyecto.md`: rol, método y formato de respuesta. **Copiar su contenido en las instrucciones del Proyecto.**
- `fuentes-iniciales.md`: catálogo de los libros disponibles localmente y precauciones de uso.
- `indice-fuentes-web.md`: archivos, bibliotecas, repositorios académicos y datos públicos.
- `timeline-mujeres-argentina.md`: línea de tiempo inicial de mujeres y colectivos influyentes.

### `dossier/` — análisis de síntesis (generado a partir del corpus local + investigación web)

| Archivo | Contenido |
|---|---|
| `00-resumen-ejecutivo.md` | Tesis central, los tres nudos recurrentes, periodización en 8 etapas, las 5 discusiones historiográficas clave |
| `01-timeline-alto-nivel.md` | Línea de tiempo maestra, 1516-2026 |
| `02-ideologias.md` | Liberalismo, federalismo, anarquismo, socialismo, nacionalismo, peronismo, desarrollismo, neoliberalismo, libertarismo |
| `03-revoluciones.md` | Tipología y anatomía comparada de revoluciones, golpes, insurrecciones y guerrillas |
| `04-economia.md` | Series con fuente, puntos de quiebre y ocho regularidades estructurales |
| `05-cultura.md` | Prensa, literatura, música, cine, fútbol, ciencia, memoria |
| `06-personajes.md` | 24 figuras con luces, sombras, mitos y polémicas |
| `07-intereses-cruzados.md` | Capital británico y norteamericano, FF.AA., Iglesia, sindicatos, agro, frigoríficos, prensa, FMI |
| `08-educacion.md` | De la Ley 1420 a la crisis de aprendizajes |
| `09-salud.md` | Del higienismo a la fragmentación del sistema |
| `10-mujeres.md` | Mujeres y disidencias: procesos, no solo figuras |
| `11-timelines-por-categoria.md` | Nueve cronologías temáticas (economía, ideas, instituciones, violencia, educación, salud, cultura, mujeres, mundo) |
| `12-fuentes-y-limitaciones.md` | Corpus usado, sesgos declarados, vacíos y los 12 documentos que faltan |
| `13-estado-y-territorio.md` | Estado, territorio y pueblos originarios (1878-2022): campos, repartos, deportaciones y el debate sobre la categoría de genocidio |
| `14-regimenes-estadisticos.md` | Reglas para usar cifras argentinas: rupturas de series y auditoría de los números del propio dossier |
| `fichas/` | **66 fichas de evidencia**: una por afirmación portante, autocontenida, con fuente, estado y límite embebidos |

### `sitio/` — generador

| Archivo | Qué hace |
|---|---|
| `build.py` | Ensambla las 89 páginas desde el markdown |
| `edtf.py` | Convierte la notación histórica en español (`s. XVI-XVII`, `c. 1766`, `1976-83`) a [EDTF Level 1](https://www.loc.gov/standards/datetime/edtf.html), el estándar de la Library of Congress para fechas imprecisas. Trae su propia batería de pruebas |
| `eventos.py` | Extrae los hechos de la línea de tiempo **leyendo la prosa del dossier**. No hay base de datos aparte: los capítulos son la única fuente de verdad, así que la línea no puede contradecirlos |
| `linea.py` | Dibuja el mapa temporal en SVG y la lista cronológica |
| `indices.py` | Regenera el índice de fichas y el consolidado de ChatGPT desde el frontmatter |
| `qa.py` | Nueve familias de chequeos que **abortan el despliegue** |

### `monografias/` — capa de profundidad

Tercera capa. Los capítulos explican, las fichas prueban, las monografías **desarrollan en profundidad un tema por vez con aparato de archivo propio**: 3.000-6.000 palabras, marcado explícito de inferencia ([DOC] / [INF] / [CIRC]), enlace bidireccional con el capítulo y la ficha correspondientes.

**La regla que la justifica:** cuando una monografía contradice al dossier, **manda la monografía** y la corrección se aplica al capítulo en el mismo movimiento. Profundizar sirve para encontrar errores de la síntesis, no solo para agregar color.

| Id | Título | Tipo | Qué corrigió |
|---|---|---|---|
| `VID-1774-VALLE-01` | María Remedios del Valle | Vida | Fecha y lugar de nacimiento, condición de esclavitud, la atribución del título "Madre de la Patria" a Belgrano (sin documento) y la naturaleza del 8 de noviembre (fecha de baja del ejército, no de muerte) |

Reglas completas, tipología y cola de trabajo en [`monografias/README.md`](monografias/README.md).

## Cómo usarlo en ChatGPT

Usá la carpeta **`chatgpt-project/`**. Está armada exactamente para eso: **19 archivos**, dentro del límite de 25 del plan Plus.

1. **Subí los 19 archivos** de `chatgpt-project/` al Proyecto. Nada más — no subas `dossier/fichas/` (son 66 archivos sueltos, ya vienen consolidados en `15-fichas-de-evidencia.md`; las monografías van consolidadas en `17-monografias.md`), ni `plan-de-mejoras.md`, ni `benchmark-40.md`, ni `debate/`: son documentos *sobre* el dossier y contaminarían la recuperación.
2. **Copiá `INSTRUCCIONES-pegar-en-el-proyecto.md`** en el campo de instrucciones personalizadas del Proyecto. Es lo más importante: ahí están las reglas sobre cifras, sobre el tramo 1990-2026 y sobre cómo usar las fichas.
3. Empezá cualquier consulta pidiendo que distinga hecho establecido / interpretación / punto debatido.

| Carpeta | Qué es | ¿Subir? |
|---|---|---|
| `chatgpt-project/` | Paquete listo, 19 archivos | **Sí, esto** |
| `dossier/` | Fuente de verdad, 15 capítulos + 66 fichas sueltas | No (duplicado) |
| `monografias/` | Fuente de verdad de la capa 3 | No (va consolidada en `17`) |
| `debate/`, `plan-de-mejoras.md`, `benchmark-40.md` | Meta-documentos sobre el dossier | No |

> `chatgpt-project/` se regenera desde `dossier/`. Si editás un capítulo, editalo en `dossier/` y volvé a copiar.

## Control de calidad

El dossier fue sometido a una **revisión adversarial con Codex CLI** (21/09/2026) configurada para buscar únicamente errores: 6 observaciones críticas, 17 importantes y 6 menores. Las correcciones aplicadas y las observaciones que quedaron abiertas están registradas en `dossier/12-fuentes-y-limitaciones.md`, §5 bis.

## Plan de mejoras — estado de ejecución

`plan-de-mejoras.md` consolida tres rondas de debate adversarial con Codex CLI (21/09/2026). Trazabilidad en `debate/` (R0 a R3).

| Fase | Estado |
|---|---|
| **0 · Correcciones del texto existente** | ✅ Hecha. Contaminación de ensayistas, contradicción de la periodización industrial, cadena de cuatro pasos en intereses cruzados, cinco sesgos no declarados, regularidades → preguntas abiertas |
| **3 · Reescritura desde Estado territorial y conquista** | ✅ Hecha. Nuevo `13-estado-y-territorio.md` con historiografía de acceso abierto posterior a 1991, más reescritura de la tesis en 00, 01, 04, 06 y 11 |
| **2 · 1990-2026 fuente por fuente** | 🟡 Parcial. Cifras con estatus de verificación explícito y nuevo `14-regimenes-estadisticos.md`. **Falta** trabajo directo sobre las bases de INDEC y BCRA |
| **1 · Fichas recuperables** | ✅ Hecha (primera iteración). 66 fichas en `dossier/fichas/`; el plan prevé 80-100 |
| **4 · Capa de monografías** | 🟡 En marcha. Arquitectura definida y primera monografía completa (`VID-1774-VALLE-01`), que ya corrigió cuatro afirmaciones del dossier. Cola de 5 monografías priorizada en `monografias/README.md` |
| **Métrica** | ⬜ Pendiente: `benchmark-40.md` no se corrió. Requiere el Proyecto de ChatGPT |

> **Nota de secuencia.** El plan ponía las fichas primero. Se ejecutaron al final, a propósito: como en esta pasada se reescribieron capítulos enteros, extraerlas antes habría significado rehacerlas. Reflejan el texto ya corregido.

## Advertencias de uso

- El corpus académico local (Cambridge History of Latin America, Romero, manual del CNBA) **termina alrededor de 1990-1995**. Todo lo posterior en el dossier se apoya en fuentes web y está marcado como tal.
- Jauretche, José María Rosa, Pigna y Andahazi se usan como **objeto de estudio y fuente de preguntas**, no como prueba de afirmaciones controvertidas.
- El dossier **no consultó ninguna fuente primaria**. Ver `dossier/12-fuentes-y-limitaciones.md`, §4, para la lista priorizada de documentos a incorporar.

## Próximo dossier propuesto

**Argentina, 1880–1945:** Estado, modelo agroexportador, radicalismo, crisis de 1930 y peronismo temprano — ahora con documentos de época (censos, diarios de sesiones, prensa) y bibliografía académica posterior a 1990.
