# Propuesta: la capa de experiencia

> Producto de tres rondas de debate adversarial con Codex CLI. Traza completa en [`debate-experiencia/`](debate-experiencia/).
> Veredicto: **GO, con una v1 chica y cerrada.**

---

## 1. TL;DR

- **Se construye**, pero mucho menos de lo que yo propuse al principio. De tres formatos quedó **uno y medio**: una línea de tiempo acotada y **un solo recorrido**.
- **La idea que yo consideraba la mejor —una franja que mostrara la densidad documental del archivo— está muerta.** Medía mi propia carga de datos, no el archivo, y presentarla como medición del pasado habría sido la página más hipócrita del sitio.
- **El formato ganador no es scrollytelling: es el «dossier de escena».** Un documento de archivo como objeto central. Lo propuso Codex y es mejor que lo mío.
- **El primer recorrido es casi gratis** y eso decidió todo: la monografía de Valle ya tiene **siete documentos transcriptos** que funcionan como estaciones. El trabajo nuevo son ~600 palabras de enlace, no 2.500.
- **Killer mistake identificado:** publicar un recorrido que haga *sentir* como hecho una inferencia narrativa. Si las etiquetas de incertidumbre son decorativas, da igual que todo lo demás sea impecable.

## 2. Tesis revisada

**Qué es:** una entrada narrativa al corpus que deja al lector **más capaz de distinguir prueba de interpretación**, no más persuadido.

**Qué no es:** una experiencia inmersiva que compita con la lectura. Ni una vitrina de efectos. Ni un tercer micrositio suelto.

El criterio de admisión, tomado de David Sleight (ProPublica) y convertido en test: **un recorrido se construye sólo si necesita pausa, comparación o cambio en el tiempo.** Si no los necesita, es un capítulo y se lee como capítulo.

Y el criterio de éxito no es estético. La investigación encontró que los lectores de scrollytelling *sienten* que se concentran más sin aprender más detalles ([ACM 2023](https://dl.acm.org/doi/fullHtml/10.1145/3605655.3605683)). Para un corpus cuyo valor entero es la precisión, ese es el peor intercambio posible. Entonces: **si la experiencia no hace que el lector entienda mejor los límites de lo que lee, no se publica.**

## 3. Qué cambió en el debate

| Mi propuesta inicial | Decisión final | Por qué |
|---|---|---|
| Enum propio `precision: dia\|mes\|año\|decada\|disputada` | **EDTF Level 1** ([ISO 8601-2](https://www.loc.gov/standards/datetime/edtf.html)): `1813-11-14`, `181X`, `1766~`, `../1830` | Iba a inventar un vocabulario para un problema que la Library of Congress ya resolvió. Además vuelve el corpus interoperable con Wikidata |
| `disputada` como valor de precisión | Dos afirmaciones fechadas, con fuente cada una, en carriles etiquetados | «Disputada» es epistemología, no resolución temporal. Promediar el desacuerdo es el pecado de las series empalmadas |
| `lat/lon` en cada evento | `geo` opcional y **habitualmente `null`** | Una batalla tiene área, una campaña itinerario, y hay topónimos no geocodificables. Obligar coordenada es obligar invención |
| `mecanismo` y `prueba` como campos del evento | Causalidad como **arista con evidencia propia**, sólo si hay claim explícito en el corpus | Confundía el hecho con una afirmación causal sobre el hecho. Hoy eso significa: casi ninguna flecha. Correcto |
| Tres formatos en la v1 | **Uno y medio**: línea acotada + un recorrido | Cortes transversales fuera: cada año es una monografía de comparabilidad en cuatro dominios |
| Franja de densidad documental | **Matada.** Vuelve, si vuelve, como *ledger de cobertura editorial* con denominador declarado | No medía el archivo: medía lo que yo pude cargar |
| Mapa SVG propio | **Fuera de la v1** | [CShapes 2.0](https://icr.ethz.ch/data/cshapes/) cubre 1886-2017 y el problema argentino interesante es 1810-1885. Un mapa moderno con pines de 1813 *afirma* una territorialidad actual — y contradice el capítulo `13-estado-y-territorio` |
| Scrollytelling con pasos discretos | **Dossier de escena**: el documento como objeto central | Sitúa más que cualquier panorama y cuesta menos prosa nueva |
| «Un recorrido cuesta como una monografía» | Falso para el primero, cierto para el segundo | Los siete documentos de Valle ya están transcriptos |
| Tarjeta «otra lectura posible» obligatoria | **Obligatoria sólo si el desacuerdo es real y pertinente** | Codex: obligarla produce desacuerdo ornamental. No se fabrica una controversia para cumplir plantilla |

## 4. Diseño

### 4.1 Capa de datos (`datos/`)

Un archivo YAML por evento. Procedencia obligatoria: **sin ella el evento no compila.**

```yaml
id: EVT-1813-AYOHUMA
rotulo: Derrota de Ayohuma
tiempo:
  edtf: "1813-11-14"        # canónico
  earliest: 1813-11-14      # derivados por el build, para layout
  latest: 1813-11-14
lugar:
  tipo: area                # punto | area | itinerario | no_localizable
  toponimo: "Ayohuma, Alto Perú (actual Bolivia)"
  geo: null                 # ausente es un valor legítimo
ejes: [militar, genero, afrodescendientes]
procedencia:
  - ficha: MUJ-1774-VALLE-01
    sostiene: [fecha, participacion]
  - capitulo: 03-revoluciones
    sostiene: [resultado]
estado: documentado         # califica SÓLO que ocurrió y cuándo
```

`procedencia[].sostiene[]` captura que una ficha sostiene la fecha y otra el actor, sin promover cada predicado a objeto de primera clase — el modelo completo de *claims* es correcto en teoría y garantiza que la capa nunca se pueble.

**Test del esquema:** ¿permite cargar 80 eventos con procedencia real en un fin de semana? Si no, es demasiado esquema.

### 4.2 Línea de tiempo del corpus

**Se llama «línea de tiempo del corpus», nunca «de la historia argentina».** No es un detalle de copy: un vacío visual no debe leerse como «no pasó nada».

1516-2026. Ancho por EDTF: un hecho fechado al día es una marca fina, uno fechado a la década es una banda, la aproximación se distingue por textura. Filtros por eje. Cada punto enlaza a capítulo, ficha o recorrido. Publica su regla de selección.

**Sin** franja de densidad, **sin** mapa, **sin** flechas causales.

### 4.3 El recorrido: «Quién puede quedar en la historia»

No «la heroína olvidada» — esa fórmula resuelve moralmente lo que el recorrido debe hacer pensar.

Siete estaciones, una por documento ya transcripto:

| # | Documento | Qué pone en juego |
|---|---|---|
| 1 | Partida de bautismo, 22/11/1774 | Nacer esclavizada. Y que la identificación sea **inferencia**, no hecho |
| 2 | Acuerdos del Cabildo, 7/9/1807 | Ya sabía pedir. El apellido es el de su propietaria |
| 3 | Tarifa de pensiones, 18/7/1807 | 12 pesos para blancos, 6 para «indios, morenos y pardos», *según la clase y la calidad* |
| 4 | Lamadrid, versión 1895 | La escena sin nombre |
| 5 | Lamadrid, versión 1855 | La misma escena, recordada distinto. La vacilación es lo que la hace creíble |
| 6 | Declaración de Videla, 17/1/1827 | El nombre sin la escena. Así se prueba algo con archivo fragmentario |
| 7 | Maga Pérez, 2023 | El monumento quemado. La historia del s. XIX y la política del s. XXI tocándose |

Cada estación lleva, fijo y antes del relato: **«sabemos / inferimos / no sabemos»** y **«Qué sostiene esta escena»** con enlaces y estado de evidencia.

Pasos discretos con botones grandes, progreso textual («4 de 7»), índice, teclado y **URL propia por estación** — es lo que la vuelve citable. Scroll sólo dentro de cada estación, nunca gobernando el argumento.

Sin facsímiles salvo licencia verificada: la transcripción citada alcanza, y suele ser más legible.

### 4.4 Tecnología

**Nada nuevo.** Ni framework, ni npm, ni D3. Umbrales acordados, escritos como regla y no como gusto:

| Nodos mutables | Herramienta |
|---|---|
| hasta ~500 | SVG nativo, `viewBox`, eventos delegados. Nada más |
| 500-2.000 | `d3-scale` y `d3-array` **sueltos** (ticks adaptativos, colisión de etiquetas) |
| +2.000 redibujando en pan/zoom | Canvas para marcas, SVG/HTML para foco y accesibilidad |
| Estado compartido complejo entre 3+ vistas | Recién ahí, framework |

Presupuesto duro: **< 60 KB de JS** por página, LCP < 2,5 s en 4G. `prefers-reduced-motion` respetado con alternativa completa sin movimiento. Cero parallax: dispara trastornos vestibulares. Cero scrolljacking.

### 4.5 Los dos mecanismos que conectan las caras

**Trazabilidad (Codex):** bloque «Qué sostiene esta escena» por estación · «Aparece en estos recorridos» en cada ficha, con la función que cumple allí · botón «volver a explorar» que **conserva eje y período**, no lleva al inicio · **prohibido duplicar prosa**: el recorrido compone y enlaza, la ficha sigue siendo la autoridad.

**Economía de producción (versión final, corregida por Codex):**

> **Cada estación debe estar aguas abajo de evidencia editorial ya terminada, y todo argumento de conexión entre estaciones debe tener su propio respaldo explícito.**

Mi formulación original —«un recorrido es aguas abajo de una monografía»— era más elegante y estaba mal: un recorrido transversal como «Las Marías» compara archivos y trayectorias, y exigirle una monografía única lo bloquearía sin razón. La versión final conserva el efecto: **no se puede producir narración sin haber hecho antes el trabajo de evidencia.** La capa narrativa deja de competir con la de evidencia y se vuelve su incentivo.

### 4.6 Controles contra el sesgo de decadencia

El corpus **ya declara** estar narrado como historia de decadencia y declara que eso es una elección interpretativa. Y la inmersión amplifica ese sesgo porque reduce fricción: *el lector siente continuidad y causalidad antes de evaluarlas.*

- **Linter de vocabulario teleológico en `sitio/qa.py`, que aborta el despliegue.** Lista inicial: *condujo inevitablemente · estaba destinado · fracaso anunciado · desde entonces nunca · no pudo sino · la decadencia argentina*. Excepciones justificadas y versionadas en el repo.
- Rotular el marco: *este recorrido adopta una interpretación; no es la única periodización posible.*
- Separar tipográficamente hecho, selección y voz editorial.
- Nada de visuales de caída continua para procesos desiguales, regionales o disputados.
- «Otra lectura posible» **si el desacuerdo es real y pertinente.** Si no lo hay, no se fabrica.

## 5. Riesgos

| # | Riesgo | P × I | Mitigación verificable |
|---|---|---|---|
| 1 | **Deriva de alcance** | alta × alto | Contrato de release versionado en el repo: **una ruta, siete estaciones, cero *nice to have*.** Todo pedido nuevo va a `post-v1`, sin excepción durante la implementación |
| 2 | **Conectores narrativos que exceden la evidencia** | media × **muy alto** | Matriz por estación revisada antes de publicar: cada oración nueva clasificada como hecho, inferencia o pregunta, y cada hecho/inferencia apuntando a ficha o documento. **Cero celdas sin respaldo** es criterio de aceptación |
| 3 | **La línea aparenta completitud nacional** | media × alto | Llamarla siempre «línea de tiempo del corpus», publicar la regla de selección, procedencia en todos los puntos |

Y la fragilidad que ninguno había listado: **deriva entre corpus y derivados.** Markdown, fichas, eventos, recorridos y páginas compiladas: cada corrección puede dejar cuatro versiones contradictorias. El build debe fallar si un id citado no existe, si falta procedencia, o si una ficha cambió sin regenerar el índice. **Eso vale más que la primera visualización, y va primero.**

## 6. No negociables vs. flexibles

**No negociables:** rúbrica de confianza publicada y las 66 fichas auditadas contra ella · procedencia obligatoria por evento · trazabilidad por afirmación · el build falla ante id inexistente o evidencia faltante · límites de alcance.

**Flexibles:** el diseño visual de la línea · cuántos ejes de filtro · el orden de las estaciones · que haya o no facsímiles.

## 7. Plan de ejecución

| Fase | Entregable | Criterio de aceptación |
|---|---|---|
| **0 · Contrato** | Manifiesto v1 congelado | Una ruta, siete documentos, lista de eventos y fuera-de-alcance, firmados en el repo |
| **1 · Integridad** | Rúbrica de confianza, auditoría, JSON Schema, validador, linter | **66/66 fichas auditadas**; build limpio; excepciones del linter justificadas |
| **2 · Línea** | Línea de tiempo navegable | 100% de eventos con EDTF, procedencia y destino; filtros funcionales; **cero puntos sin fuente** |
| **3 · Recorrido** | Siete dossiers de escena | URL por estación, progreso e índice; matriz de trazabilidad completa; el retorno conserva estado |
| **4 · Revisión** | QA editorial y de accesibilidad | Teclado, móvil, cero enlaces rotos, licencias verificadas o facsímiles retirados |
| **5 · Prueba** | 12 lecturas auditables | Métrica norte ≥ 9/12; **una sola** iteración de corrección antes de decidir expansión |

**La fase 1 no es burocracia previa: es donde está el valor.** Hoy 66 fichas publicadas declaran confianza `alta/media/baja` **sin rúbrica publicada** — es impresión editorial disfrazada de metadato. La capa de experiencia lo vuelve visible porque va a filtrar por ese campo. Se paga esa deuda o no se construye nada.

## 8. Métrica norte

**Tasa de lectura auditable.** De 12 lectores de prueba, cuántos —sin ayuda— completan una estación, **distinguen correctamente un hecho de una inferencia o una incógnita**, y abren el respaldo de una afirmación central.

**Umbral: 9 de 12.** Si no se alcanza tras una iteración de corrección, **se mata la expansión de recorridos** y el esfuerzo vuelve a evidencia y monografías.

No necesita analytics: es una prueba breve, voluntaria y manual. El sitio es estático y no trackea a nadie.

## 9. Killer mistake

> **Publicar un recorrido que haga sentir como hecho una inferencia narrativa.**

Si las etiquetas «inferimos» y «no sabemos» son decorativas, la experiencia convierte lagunas del archivo y decisiones del autor en certeza afectiva. En ese caso da igual que el esquema, la línea y los enlaces sean impecables: **el proyecto traiciona exactamente lo que lo hacía valioso.**

Es también, y no por casualidad, el riesgo que la monografía de Valle documenta en su propio objeto: ochenta años de «supuestas verdades» sobre ella se construyeron así, llenando huecos del archivo con datos verosímiles que nadie verificó. Repetir esa operación en el sitio que la denuncia sería el fracaso más completo posible.

## 10. Anexos

- [`debate-experiencia/00-claude-analisis-inicial.md`](debate-experiencia/00-claude-analisis-inicial.md)
- [`debate-experiencia/01-codex-r1.md`](debate-experiencia/01-codex-r1.md) — arquitectura de datos y tecnología
- [`debate-experiencia/02-claude-r1.md`](debate-experiencia/02-claude-r1.md)
- [`debate-experiencia/03-codex-r2.md`](debate-experiencia/03-codex-r2.md) — UX, editorial y producto
- [`debate-experiencia/04-claude-r2.md`](debate-experiencia/04-claude-r2.md)
- [`debate-experiencia/05-codex-r3.md`](debate-experiencia/05-codex-r3.md) — cierre y veredicto

### Fuentes de la investigación de UX

- [The Impact of Scrollytelling on the Reading Experience of Long-Form Journalism](https://dl.acm.org/doi/fullHtml/10.1145/3605655.3605683) — ACM 2023
- [The Past, Present, and Future of Scrollytelling](https://nightingaledvs.com/the-past-present-and-future-of-scrollytelling/) — Nightingale
- [Extended Date/Time Format (EDTF)](https://www.loc.gov/standards/datetime/edtf.html) — Library of Congress
- [Wikidata: Help:Dates](https://www.wikidata.org/wiki/Help:Dates) · [CIDOC-CRM 7.2.4](https://cidoc-crm.org/)
- [CShapes 2.0](https://icr.ethz.ch/data/cshapes/) · [OpenHistoricalMap](https://www.openhistoricalmap.org/) · [Natural Earth](https://www.naturalearthdata.com/)
- [NN/g: Mobile usability](https://www.nngroup.com/articles/mobile-usability-2nd-study/) · [NN/g: Mobile content](https://www.nngroup.com/articles/mobile-content/)
- [Narrative Visualization: Telling Stories with Data](http://vis.stanford.edu/files/2010-Narrative-InfoVis.pdf) — Segel & Heer, Stanford
