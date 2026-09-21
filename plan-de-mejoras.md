# Plan de mejoras del dossier — propuesta consolidada

> **Estado de ejecución al 21/09/2026.** Hecho: Fase 0 (correcciones), Fase 3 (Estado y territorio), Fase 1 (60 fichas), y la Fase 2 en su dimensión estadística. Pendiente: la actualización bibliográfica post-1991 **más allá del capítulo indígena** —que era la prioridad única del veredicto de la Ronda 2— más los módulos pospuestos y el resto del benchmark. Detalle al final del documento, §12.

Resultado de tres rondas de debate adversarial con Codex CLI (21/09/2026). Trazabilidad completa en `debate/`.

---

## TL;DR

1. **El dossier no tiene un problema de extensión: tiene un problema de arquitectura.** Está escrito como texto para leer y se va a usar como base para recuperar. Esas dos cosas piden formas distintas.
2. **El error que invalida todo lo demás** (*killer mistake*, consenso de las tres rondas): que ChatGPT devuelva una afirmación causal o cuantitativa **sin poder recuperar junto a ella su procedencia y su límite**. Un dossier con mejor historia indígena, regional y comparada no sirve si el sistema sigue extrayendo "la restricción externa explica casi todas las crisis" como hecho asentado.
3. **Mi plan inicial estaba mal ordenado y una de sus piezas era directamente dañina.** Proponía series CSV largas (1810-2026) como primer paso: eso es un artefacto falso, porque mezcla regímenes estadísticos incompatibles.
4. **La ausencia más grave no es la que yo creía.** Puse federalismo fiscal; el debate estableció que es la **perspectiva indígena-territorial**, porque no agrega un tema sino que corrige el punto de partida causal de todo el relato — y el dossier ya contiene la evidencia que lo prueba sin haberla usado.
5. **Tres prioridades, no doce**: fichas recuperables → reescritura de 1990-2026 → reescritura del núcleo 1852-1916. Todo lo demás espera.

---

## 1. Tesis revisada: qué es y qué no es este dossier

**Es** un instrumento de trabajo para un lector exigente no profesional, que responde a un encargo explícito (resumen ejecutivo, ideologías, revoluciones, economía, cultura, personajes con luces y sombras, intereses cruzados, educación, salud, mujeres, timelines).

**No es** —y no debe pretender ser— una monografía académica. De ahí se siguen dos consecuencias que el debate confirmó:

- La grilla "luces y sombras" de `06-personajes` **se sostiene**, porque es el encargo, aunque Codex tenga razón en que fuerza balances que la historia no siempre debe hacer. Lo que se corrige es aplicarla de forma no uniforme: donde no hay balance que hacer (Videla), el formato debe romperse explícitamente, como regla del capítulo y no como excepción suelta.
- Las tesis sintéticas ("los tres nudos", "las ocho regularidades") **no se borran pero cambian de género**: pasan de leyes a preguntas abiertas con evidencia a favor y en contra. Sin capa de síntesis el dossier deja de ser recuperable; con capa de síntesis dogmática, deja de ser confiable.

---

## 2. Decisiones consolidadas — qué cambió respecto del plan inicial

| # | Plan v0 (mío) | Decisión final | Por qué cambió |
|---|---|---|---|
| 1 | Verificabilidad primero (páginas + series) | **Procedencia y límite embebidos por afirmación** | El daño dominante no es una página no encontrable: es una explicación de 1991 recuperada como consenso actual |
| 2 | CSV de series largas 1810-2026 | **Descartado.** En su lugar: catálogo de regímenes estadísticos con sus rupturas | Una serie continua de PIB o pobreza argentina es metodológicamente engañosa: mezcla universos, canastas y coberturas |
| 3 | Ausencia prioritaria: federalismo fiscal | **Perspectiva indígena-territorial** | Cambia la causalidad de origen, no solo la explicación del último medio siglo |
| 4 | Capítulo nuevo sobre el tema que falta | **Reescritura del núcleo 1852-1916**, no apéndice temático | Añadir un capítulo indígena deja intacta la tesis que hay que corregir |
| 5 | Cuatro dossiers regionales | **Pospuesto** | Agrega volumen antes de hacer confiable lo que ya existe |
| 6 | Comparación internacional amplia | **Pospuesta**, y acotada a Australia cuando se haga | Un comparador bien elegido; seis países es decoración |
| 7 | "Falta teoría del cambio" | **Gramática causal explícita** (mecanismo, escala, grado de prueba) | El pluralismo explicativo es correcto en una síntesis; lo que falta es marcar dónde termina el dato y empieza la inferencia |
| 8 | 1990-2026: "reforzar fuentes" | **Reescritura afirmación por afirmación** | No hay bibliografía vieja que actualizar: falta columna vertebral académica y documental |

---

## 3. Arquitectura acordada: dos capas

**Capa 1 — Prosa (la que ya existe).** Explica, contextualiza, discute. Se lee secuencialmente. Se conserva.

**Capa 2 — Fichas de evidencia (nueva).** `dossier/fichas/`, una ficha por **afirmación consultable**, no por dato suelto. 120-220 palabras. Arranque: **80-100 fichas portantes**; ampliar después según consultas reales.

```md
---
id: ECO-2001-CRISIS-01
periodo: 1998-2003
temas: [economía, deuda, pobreza, política]
tipo: [hecho | interpretación | debatido]
estado: actualizado | debatido | provisional
confianza: alta | media | baja
fuentes:
  - autor/institución, año, título, URL, página o tabla
actualizado_hasta: 2026-09
prosa_relacionada: [04-economia#8, 01-timeline#VIII]
---

**Afirmación.** …
**Evidencia y mecanismo.** …
**Qué está debatido o no permite concluir.** …
**Respuesta breve sugerida.** …
```

**Por qué esto y no repetir advertencias en la prosa.** Se evaluaron las dos opciones. Repetir cajas de advertencia es barato pero falla: recarga la lectura, envejece mal y un recuperador puede igualmente cortar antes de la caja. Rediseñar la unidad recuperable cuesta más al inicio pero hace que **la cautela viaje pegada a la afirmación**. Es la única solución al *killer mistake*.

**Criterio de "afirmación portante"** (para no anotar 37.800 palabras, que sería inviable y contraproducente): son portantes las que cumplen al menos una condición —aparecen en `00-resumen-ejecutivo`, se citan en más de un capítulo, o el texto las marca en negrita como conclusión—. Eso da del orden de 60-90 afirmaciones, no miles.

---

## 4. Las tres prioridades

### P1 · Registro de afirmaciones portantes + fichas recuperables
Antes de actualizar nada hay que saber **qué se afirma, con qué fuente y con qué estatus**. Incluye un trabajo previo barato y necesario: **atribución nítida** —separar qué dice el corpus de qué digo yo—, que hoy es borrosa en decenas de pasajes. No confundir con paginar exhaustivamente: basta fuente y localizador de las 80-100 afirmaciones que organizan el dossier.

### P2 · Reescritura de 1990-2026, fuente por fuente
Es el tramo de mayor uso probable y el peor sostenido: 36 años con prensa y conocimiento general. Cada afirmación pasa a fuente institucional o académica: INDEC (estadísticas sociales y cuentas nacionales), BCRA (series monetarias), CEPALSTAT (comparables), Boletín Oficial e InfoLEG (normas).

### P3 · Reescritura del núcleo 1852-1916 desde Estado territorial y conquista
**Integrar, no anexar.** Conquista, expropiación, distribución de la tierra, subordinación laboral y persistencia de violencia estatal dentro de la explicación del orden agroexportador.

> **Por qué esto es corrección y no cuota temática.** En `04-economia` §2.2 el dossier ya cita a Cortés Conde mostrando que la Conquista del Desierto **no fue consecuencia del auge sino condición de su posibilidad** —los precios caían y la única forma de sostener rentabilidad era incorporar tierra sin costo—. Escrito eso, el dossier siguió narrando 1880 como "Estado + mercado mundial + inmigración" y archivó la campaña militar en el casillero de "violencia institucional". **Probó la tesis fuerte y la guardó en el capítulo equivocado.** Napalpí (1924) y Rincón Bomba (1947) quedan como episodios sueltos por la misma razón.

### Lo que queda afuera, y por qué está bien
Cuatro dossiers regionales, módulo comparado con Australia, catálogo integral de series y capítulo autónomo de federalismo fiscal. **No son secundarios: agregan volumen antes de hacer confiable y recuperable lo que ya existe.** El federalismo entra mientras tanto como *mecanismo* dentro de las fichas y de 1990-2026; el capítulo amplio puede esperar.

---

## 5. Correcciones puntuales, baratas y de alto retorno

Se hacen sobre el texto actual, sin esperar a P1-P3.

**A · Contaminación de ensayistas** (tres pasajes identificados, todos válidos):
- `06-personajes` §Sarmiento: "la crítica más aguda que se le ha hecho" es una jerarquización sin evidencia comparativa. Eliminar.
- `05-cultura` §2.1: se desliza desde Gallo (relevancia de la prensa) hacia la tesis jauretcheana de captura del sentido común. Separar.
- `10-mujeres` §1.1: la afirmación sobre el mestizaje se formula en voz del dossier y la advertencia llega después. **Patrón a buscar sistemáticamente: la advertencia posterior no neutraliza la afirmación anterior.**

**B · Conclusiones sub-extraídas** (el texto tiene evidencia más fuerte que la conclusión que saca):
- `04-economia` §2.4 — que en 1914 la producción local cubriera 91% de alimentos y 88% de textiles no sostiene solo "no era un país sin industria": sostiene que **la industrialización argentina no empieza en 1930 ni con el peronismo, y que la ISI reconfigura una industrialización previa**. Como el dossier después periodiza "1930-1943: intervencionismo conservador" como si ahí naciera la industria, esto es una **contradicción interna**, no una omisión.
- `05-cultura` §2.2 — el 51,4% de mutuales multinacionales permite concluir que la integración no fue solo política estatal: hubo infraestructura asociativa autogestionada y transétnica.
- `07-intereses-cruzados` §2 — que Justo aceptara formalmente la Corporación de Transportes y luego no la implementara **invalida el mecanismo general "presión externa → decisión estatal"**. Hay que distinguir cuatro pasos: presión / concesión formal / implementación / resultado. Obliga a revisar varios casos del capítulo.

**C · Sesgos no declarados** (agregar a `12-fuentes` §2):
1. **Teleología del declive.** El más grave, porque es estructural: "los tres 1880 que terminan en crisis", "cada golpe produjo lo contrario", "ocho regularidades" seleccionan ciclos de fracaso y los convierten en la forma de la historia. El dossier declara en su primera página que "por qué fracasó Argentina" es una formulación tramposa, y después escribe 37.000 palabras dentro de ella.
2. **Nacionalismo metodológico.** `07-intereses-cruzados` hace "presiones sobre Argentina", con Argentina como sujeto y el resto como entorno, en vez de historia transnacional.
3. **Estatismo presidencialista.** El país actúa mediante presidentes, FF.AA., partidos y macroeconomía; municipios, provincias, cooperativas, empresas y hogares aparecen como efectos.
4. **Sesgo de ciudadanía formal.** Derechos y trabajo se miden desde legislación y empleo registrado.
5. **Sesgo de lengua y circulación.** Corpus íntegramente en español o traducido; sin literatura anglosajona reciente ni producción brasileña sobre el Cono Sur.

---

## 6. Complementariedad: qué bibliografía incorporar

Surgida del debate, con los casos concretos que corrige cada una.

| Corrige | Obra | Qué cambia en el dossier |
|---|---|---|
| Orden de 1880 | **Walter Delrio**, *Memorias de expropiación*; **Briones y Delrio**; Lenton | La articulación Estado-mercado-inmigración también dependió de conquista, desposesión y reinscripción racial. El "éxito" 1880-1914 no precede a la desigualdad territorial: en parte se funda en ella |
| Peronismo | **Eduardo Elena**, *Dignifying Argentina* (2011); **Matthew Karush**, *Culture of Class* (2012) | Mi genealogía entre élites (catolicismo social → varguismo → Mussolini → Perón) se usa como causa suficiente de una identidad de masas. Falta ciudadanía, consumo, radio y cine — que el propio dossier describe en `05-cultura` y no usa para explicar 1945 |
| Economía peronista | **Claudio Belini**; **Marcelo Rougier**; **Gerchunoff** sobre 1948-55 | Impide tratar 1952-55 como apéndice estabilizador de un peronismo "auténtico" previo. No hubo directriz uniforme |
| 1973-76 | **Marina Franco**, *Un enemigo para la nación* (2012) | Obliga a sustituir la cadena causal breve (violencia → Triple A → golpe) por la producción jurídica y discursiva del "enemigo interno" **bajo gobierno constitucional**. Refuerza la asimetría en vez de diluirla |
| Memoria | **Emilio Crenzel**, *La historia política del Nunca Más* | El informe no es un marco estable: es un objeto con historia política propia |
| 1852-1880 | **Hilda Sábato**, *The Many and the Few* | Hubo ciudadanía, asociaciones, prensa y movilización competitiva antes de 1912. Toca directamente el "Nudo 1" del resumen ejecutivo |
| Federalismo | **Gibson y Calvo** (2000) sobre reformas menemistas y coaliciones territoriales; OPC sobre coparticipación desde 1935 | Explica por qué las reformas fueron políticamente sostenibles; corrige "el Estado se quiere capturar o destruir, rara vez construir" |
| Divergencia | **Bekerman, Dulcich y Gaite** sobre Argentina-Australia | Único comparador que vale: pregunta exacta —cuánto de la divergencia post-1930/45 se explica por shocks compartidos y cuánto por instituciones fiscales, coaliciones distributivas e inversión |

---

## 7. Regímenes estadísticos: las trampas concretas

Sustituye al CSV descartado. **Regla: una serie por régimen estadístico, nunca una línea continua.**

| Variable | Fuente | Ruptura que invalida la comparación larga |
|---|---|---|
| Población | INDEC censos; CELADE/CEPAL | Censo ≠ estimación intercensal; cambios territoriales; proyecciones revisadas tras cada censo |
| PIB | INDEC Cuentas Nacionales + documentación del empalme; CEPALSTAT | Bases 1935, 1950, 1960, 1970, 1986, 1993, 2004. El empalme por tasas conserva variaciones, **no** niveles ni composición sectorial. **Ferreres es reconstrucción privada, no dato primario** |
| Inflación | INDEC archivo IPC; BCRA series | IPC GBA ≠ IPC nacional. **INDEC informa reservas expresas para enero 2007 – diciembre 2015**: no usar como deflactor limpio |
| Salario real | INDEC Índice de Salarios; reconstrucciones académicas para largo plazo | Registrado desde nov. 2015, no registrado desde oct. 2016. **No existe un "salario real argentino" homogéneo de dos siglos** |
| Desempleo | INDEC EPH histórica + metodología 2003 | **EPH puntual 1974-2003 vs. continua desde 2003**; ampliación de 28 a 31 aglomerados en 2006. Es población de aglomerados urbanos, no "Argentina" |
| Pobreza | INDEC metodología y archivo | Incidencia por ingresos en aglomerados, no nacional ni rural. **No publicada 2014-2015**, reanudada en 2016 |
| Alfabetización | Tablas originales de cada censo | 1869 "mayores de 6" vs. 2010 "mayores de 10". Ya corregido en `08-educacion` §2.4: **generalizar ese patrón a las otras siete variables** |
| Mortalidad infantil | DEIS y anuarios | Cobertura del registro varía por época y provincia; formularios vigentes desde 2001 son otra ruptura |

**Cifras del dossier actual que esta tabla pone en cuestión:** "desempleo 18,4% en 1995" y las de 2001-2003 no son de la misma medición; "pobreza >50%" de 2002 no forma serie con cifras posteriores.

---

## 8. Métrica norte única

**Banco fijo de 40 preguntas**, equilibrado por período, tema y controversia, con **10 trampas deliberadas**: cifras 2007-2015, pobreza 2014-2015, causalidad 1973-1976, Conquista del Desierto, peronismo, coyuntura 2024-2026.

El dossier mejoró solo si, respondiendo con el Proyecto:

| Umbral | Criterio |
|---|---|
| ≥ 38/40 | identifican una ficha o fuente concreta |
| 100% | de las respuestas basadas en evidencia provisional declaran su límite |
| 0/40 | convierte una interpretación debatida en hecho establecido |
| ≥ 36/40 | correctas según pauta revisada por lectura humana |
| 100% | de las cifras incluye período, universo y fuente — o se omite |

Es un test repetible antes y después, no una impresión de "más rigor". **El banco está escrito en `benchmark-40.md`** y se puede correr hoy contra el dossier actual para tener la línea de base.

---

## 9. No negociable vs. flexible

**No negociable**
- Procedencia y límite viajan pegados a cada afirmación portante.
- Ninguna serie estadística larga sin declarar su ruptura.
- La asimetría Estado / organizaciones armadas en 1973-1983 no se relativiza.
- La distinción hecho / interpretación / debatido se mantiene en las dos capas.

**Flexible**
- El orden de P2 y P3 puede invertirse si el uso real muestra más consultas sobre el siglo XIX.
- El número de fichas (80-100 es arranque, no meta).
- Los dossiers regionales, Australia y el capítulo de federalismo: deseables, no bloqueantes.

---

## 10. Riesgos

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| El aparato de fichas crece sin control y el dossier se vuelve inmanejable | Alta | Medio | Criterio de "afirmación portante" cerrado y tope de 100 fichas en la primera iteración |
| Se hace P3 (reescritura 1852-1916) y se rompe la coherencia con capítulos no tocados | Media | Alto | P3 después de P1: con el registro de afirmaciones se sabe qué más cae |
| 1990-2026 se reescribe con fuentes oficiales intervenidas (2007-2015) sin marcarlo | Media | Alto | La tabla de §7 es obligatoria antes de tocar ese tramo |
| El plan se ejecuta entero y tarde en vez de por partes | Alta | Medio | P1 produce valor aislado: aun sin P2 ni P3, las fichas ya arreglan el *killer mistake* |

---

## 11. Discrepancias que quedaron abiertas

**1. Alcance de la comparación con Australia.** Codex la considera módulo acotado, opcional. Yo sostengo que la pregunta de la divergencia **organiza el dossier entero** (`00-resumen-ejecutivo` §1): si la divergencia se explica mayormente por shocks compartidos, los "tres nudos" son ruido local. Queda sin resolver, y se pospone por costo, no por acuerdo.

**2. "Falsedad vs. obsolescencia".** Yo sostuve que una cifra de prensa de 2026 puede ser directamente falsa, mientras una explicación de 1991 solo es vieja. Codex lo matizó bien: el problema de la prensa no es la falsedad sino la **falta de estabilidad, definición metodológica y trazabilidad**. Acepto la corrección; la conclusión operativa (reescribir 1990-2026 con fuente institucional) no cambia.

**3. `06-personajes`.** Codex propone fusionarlo con los capítulos temáticos. Se conserva por encargo explícito del usuario. Registrado como desacuerdo, no como consenso.

---

## Anexos

- Debate completo: `debate/` (6 archivos, R0 a R3).
- Banco de 40 preguntas: `benchmark-40.md`.
- Dossier: `dossier/`.
- Revisión adversarial previa (correcciones ya aplicadas): `dossier/12-fuentes-y-limitaciones.md` §5 bis.


---

## 12. Estado de ejecución — actualizado

### ✅ Cerrado

| Trabajo | Resultado |
|---|---|
| **Fase 0** — correcciones | 3 pasajes de contaminación · 3 conclusiones sub-extraídas · 5 sesgos no declarados · cadena de cuatro pasos · regularidades → preguntas abiertas |
| **Fase 3** — Estado territorial | `13-estado-y-territorio.md` (Pérez y Nagy-Papazian leídos en directo) + reescritura de la tesis en 00, 01, 04, 06, 11 |
| **Fase 1** — fichas | **65 fichas** con procedencia, estado y límite embebidos |
| **Fase 2** — estadística | `14-regimenes-estadisticos.md` · cifras con estatus ✓/⚠ · serie de pobreza 2023-2025 · IPC 2010 con las dos mediciones · coyuntura 2026 oficial |
| **Bibliografía post-1991** — parcial | **Sábato leída en directo** (corrige el Nudo 1) · **Karush, Elena, Franco** incorporados vía reseñas, declarados como tales |
| **Gramática causal** | Regla de cuatro mecanismos y tres grados de prueba, aplicada al caso testigo de 1930 |
| **Benchmark** — 13 de 40 | 10 limpio, 3 flojo, 0 falla. Detectó un error propio (RUVTE) y dos vacíos de ficha, ya corregidos |

### 🔴 Lo único con prioridad real

**Volver a correr el benchmark.** Se corrieron 13 preguntas sobre una versión del dossier que ya cambió tres veces. **No sabemos si las correcciones funcionaron.** Todo lo demás es profundización de contenido abierta; esto es verificación, y es lo que dice si el trabajo sirvió.

Mínimo: preguntas 1 (Rosas), 13 (resumen) y una nueva sobre participación política antes de 1912.

### 🟡 Profundización abierta — sin orden obligatorio

| Trabajo | Estado real |
|---|---|
| **Crenzel, Belini/Rougier, Gibson y Calvo** | Identificados, no incorporados |
| **Delrio y Sábato en sus libros** | Sólo artículos y reseñas. Delrio no está en acceso abierto; *La política en las calles* está en préstamo en Internet Archive |
| **Gramática causal sistemática** | Aplicada a **un** pasaje. Los otros 14 capítulos siguen sin auditar la frontera dato/inferencia |
| **Atribución nítida en la prosa** | Hecha en las fichas, no en los capítulos |
| **1990-2026 político** | La estadística se arregló; el relato de Menem, 2001, kirchnerismo, Macri y Milei sigue en fuentes secundarias |
| **Fichas 65 → 80-100** | Ampliar según lo que el benchmark muestre débil, no por completitud |

### ⬜ Pospuesto por decisión del debate

Cuatro dossiers regionales · Australia · capítulo de federalismo fiscal · historia afroargentina posterior a la independencia · los diez temas de `dossier/12-fuentes-y-limitaciones.md` §5 bis.

---

## 13. Criterio de terminación

Cada ronda de trabajo abre huecos nuevos: es la naturaleza de una síntesis histórica y **no tiene final por acumulación**. El criterio de corte no es "cuando no falte nada" sino:

> **El dossier está terminado cuando el benchmark deja de encontrar fallas y cada nueva corrida sólo confirma lo anterior.**

Hoy se corrió una vez, sobre una versión vieja, y encontró tres cosas. Hasta que una corrida vuelva limpia, seguir agregando bibliografía es optimizar sin medir.
