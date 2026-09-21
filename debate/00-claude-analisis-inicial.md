# R0 — Análisis crítico inicial del dossier (Claude)

Objeto del debate: **el dossier de `dossier/` (13 archivos, ~37.800 palabras) y el plan para mejorarlo.** No se debate la historia argentina: se debate si este artefacto sirve para lo que el usuario quiere —alimentar un Proyecto de ChatGPT de investigación histórica— y qué habría que hacerle, en qué orden.

---

## TL;DR

1. El dossier es **fuerte en 1880-1990 y débil en todo lo demás**. Eso no es un defecto de redacción: es la forma del corpus disponible (Cambridge History of Latin America, ediciones 1986 y 1991).
2. Su problema más grave **no es lo que dice sino lo que no puede decir**: cero fuentes primarias, cero historiografía posterior a 1991, y un tercio del período democrático (1990-2026) apoyado en prensa.
3. El sesgo regional porteño-pampeano está **declarado pero no corregido**. Declararlo fue honesto; dejarlo así lo vuelve estructural.
4. El formato es prosa larga. Para el uso real —recuperación conversacional en un Proyecto de ChatGPT— **probablemente el formato esté mal elegido**.
5. Mi hipótesis de prioridad: **primero verificabilidad, después cobertura**. Un dossier con menos temas y fuentes citables vale más que uno con más temas y afirmaciones sin anclaje.

---

## 1. Auditoría de cobertura

### 1.1. Cronológica

| Tramo | Profundidad | Base |
|---|---|---|
| Precolonial | **Casi nula** (una fila de timeline) | Manual del CNBA, capítulo introductorio |
| Colonia 1536-1776 | Baja | CNBA + Giberti |
| 1776-1852 | Media | Romero + CNBA |
| 1852-1880 | Buena | Romero + Rosa (ensayo) |
| **1880-1916** | **Excelente** | Cortés Conde + Gallo |
| **1916-1946** | **Excelente** | Rock ×2 |
| **1946-1990** | **Excelente** | Torre y de Riz |
| **1990-2026** | **Débil** | Prensa + conocimiento general |

**Lectura:** el dossier tiene una joroba de calidad de 110 años y dos colas flojas. 1990-2026 son 36 años —más que todo el período 1880-1916— tratados con una fracción del rigor.

### 1.2. Temática

**Cubierto con solvencia:** política institucional, economía macro, ideologías, violencia política, educación, salud, mujeres, intereses económicos cruzados.

**Ausente o testimonial** (verificado por conteo sobre los 13 archivos):
- **Federalismo fiscal y coparticipación: 1 mención.** Es, probablemente, la institución que más explica la política argentina del último medio siglo, y no está.
- **Informalidad laboral: 3 menciones.** Es la variable que rompe la promesa universalista de salud y previsión, y el dossier la nombra sin desarrollarla.
- Sistema previsional: 6 menciones, sin capítulo.
- Historia ambiental: prácticamente nula (desmonte, agua, minería, soja, clima).
- Historia urbana y de la vivienda: nula (conurbano, villas, acceso al suelo).
- Ciencia y tecnología como política pública: nombres sueltos (Houssay, Leloir, CONICET), ningún proceso (nuclear, satelital, biotecnología, software).
- Justicia como actor institucional: aparece solo como víctima de purgas.
- Migraciones posteriores a 1950: limítrofes, coreanas, chinas, senegalesas, venezolanas.
- Religiosidad: la Iglesia católica está bien tratada; el crecimiento evangélico y la secularización reciente, no.
- Seguridad, policías, narcotráfico.
- Demografía como proceso (transición, fecundidad, envejecimiento).
- Historia empresarial concreta (Bunge y Born, Techint, Pérez Companc, Clarín, YPF como organización).
- Capacidad estatal / burocracia.

### 1.3. Regional
El sesgo está declarado en `12-fuentes-y-limitaciones.md` §2 como "el más grave", y sigue intacto. Patagonia: 8 menciones en 37.800 palabras. No hay un solo proceso regional contado desde su propia lógica: ni el azúcar tucumano, ni La Forestal y el tanino chaqueño, ni la yerba misionera, ni el modelo vitivinícola mendocino y su régimen de agua, ni la lana y el petróleo patagónicos.

### 1.4. Sujetos sociales
Bien: élites, clases medias, obreros industriales urbanos, mujeres (parcial).
Mal o ausentes: campesinado y peones rurales, trabajadores informales, pueblos indígenas después de 1885, afroargentinos después de la independencia, migrantes limítrofes, infancias, personas mayores.

---

## 2. Auditoría de fuentes — el problema de fondo

1. **Cero fuentes primarias.** Ni un censo original, ni un diario de sesiones, ni un expediente, ni prensa de época. Todo lo primario llega citado por terceros.
2. **Desactualización historiográfica de 35-40 años.** El corpus académico es de 1986-1991. Queda afuera toda la renovación posterior: la historia social del peronismo, los estudios sobre la dictadura posteriores a los juicios de 2003, la nueva historia económica argentina, la historia de género profesionalizada, los estudios regionales.
3. **Asimetría de peso entre corrientes.** El dossier hace discutir a Cortés Conde con "la tesis clásica", pero la tesis clásica llega solo citada por su adversario. Nunca se lee a Bagú, Oddone o Scobie en directo.
4. **La divulgación pesa más de lo que debería** en el capítulo de mujeres, por ausencia de alternativa en el corpus.

---

## 3. Auditoría de método

**Lo que funciona:** la distinción hecho / interpretación / punto debatido; los sesgos declarados; las advertencias de método como dispositivo visible; el registro de la revisión adversarial previa (§5 bis).

**Lo que falta:**
- Citas sin página. "[Torre y de Riz, cap. 2]" no permite verificar.
- No hay bibliografía formal ni glosario ni índice onomástico.
- **No hay comparación internacional sistemática.** El dossier se pregunta por qué Argentina no sostuvo su éxito y nunca mira a Australia, Canadá, Uruguay, Chile, Italia o España. Sin contrafáctico comparado, la pregunta central no es contestable.
- No hay series de datos reproducibles: los números están embebidos en prosa, no en tablas exportables.

---

## 4. Auditoría de formato — la crítica que me hago a mí mismo

El usuario va a subir esto a un Proyecto de ChatGPT para hacerle preguntas. Escribí **prosa ensayística larga**, que es el formato óptimo para lectura humana secuencial y probablemente **subóptimo para recuperación conversacional**: los modelos recuperan mejor unidades cortas, autocontenidas y con metadatos.

Hipótesis a debatir: el dossier debería tener **dos capas** —la prosa que ya existe, para leer, y una capa de "hechos atómicos" con fuente, fecha y confianza, para que el modelo recupere—. No estoy seguro de que valga el costo.

---

## 5. Plan v0 — cinco paquetes, en este orden

**P1 · Verificabilidad (antes que cualquier contenido nuevo).**
Series históricas reproducibles en CSV (población, PIB, inflación, salario real, analfabetismo, mortalidad infantil, desempleo, pobreza) tomadas de INDEC, BCRA, DEIS y bases académicas reconocidas. Reemplazar las cifras en prosa por referencias a esas series. Añadir páginas a las citas del corpus.
*Por qué primero:* todo lo demás hereda la credibilidad de esta capa.

**P2 · Tapar el agujero 1990-2026.**
Sustituir prensa por bibliografía académica y datos oficiales. Es el tramo que el usuario más va a consultar y el peor sostenido.

**P3 · Descentrar: cuatro dossiers regionales.**
NOA, NEA, Cuyo, Patagonia, cada uno contado desde su propia economía política, no como apéndice pampeano.

**P4 · Capítulos nuevos de alta prioridad.**
Federalismo fiscal y coparticipación; trabajo e informalidad; Estado y capacidad estatal; ambiente y territorio; ciencia y tecnología. Cada uno con historiografía actual.

**P5 · Capa de recuperación.**
Índice de hechos atómicos con fuente y nivel de confianza + bibliografía + glosario + índice onomástico.

---

## 6. Decisiones explícitas que tomé y podrían estar mal

1. **Usé el corpus disponible en vez de decir "este corpus no alcanza".** Defendible por utilidad, cuestionable por rigor.
2. **Puse a Jauretche, Rosa y Pigna en el dossier** como objeto de estudio. Alternativa: excluirlos y perder el mapa del sentido común argentino.
3. **Escribí tesis fuertes y sintéticas** ("los tres nudos", "las ocho regularidades"). Son memorables y discutibles; la revisión anterior ya me obligó a degradar varias a hipótesis.
4. **Prioricé 1880-1990** porque ahí estaba el corpus, no porque sea lo más relevante para entender 2026.

---

## 7. Preguntas abiertas para Codex (R1)

1. ¿Mi orden de prioridades es el correcto, o hay que tapar 1990-2026 **antes** que construir la capa de verificabilidad?
2. ¿Cuál es el capítulo ausente cuya falta más distorsiona lo que el dossier **sí** dice? Mi candidato es federalismo fiscal. ¿Hay uno peor?
3. ¿La desactualización historiográfica de 35 años invalida conclusiones concretas del dossier, o solo lo empobrece? Quiero casos específicos, no la observación general.
4. ¿La comparación internacional es imprescindible o es un lujo académico para el uso que el usuario le va a dar?
5. ¿Qué perspectiva historiográfica ausente cambiaría más las conclusiones actuales?

---

**VEREDICTO RONDA 0 (Claude)**
- El dossier es útil y honesto sobre sus límites, pero su relación calidad/cobertura es muy desigual: excelente en 110 años, flojo en los 36 más recientes y ciego fuera de la pampa.
- El problema principal es de **verificabilidad**, no de extensión.
- Propongo orden P1 → P2 → P3 → P4 → P5, con la duda abierta de si P2 debería ir primero.
