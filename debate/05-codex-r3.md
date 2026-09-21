Claude acierta en que hay que decidir, pero sobredimensiona una oposición: el problema no es “actualizar el corpus viejo” versus “reescribir 1990-2026”. Ambos necesitan la misma unidad básica: una afirmación que lleve pegadas su fuente, fecha, alcance y límite.

## 1. Formato: conservar prosa, añadir una capa de fichas de evidencia

La prosa larga debe quedarse: responde al encargo de síntesis, controversias y personajes. Pero no debe ser la única capa para el Proyecto.

Crear `dossier/fichas/`, una ficha Markdown por **afirmación consultable**, no por dato aislado. Tamaño: 120–220 palabras; una tesis, evento o estimación por ficha. Arranque: 80–100 fichas portantes; luego ampliar sólo según consultas reales.

Formato exacto:

```md
---
id: ECO-2001-CRISIS-01
periodo: 1998-2003
temas: [economía, deuda, pobreza, política]
tipo: [hecho, interpretación]
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

Las fichas no duplican todo el dossier: lo indexan, acotan inferencias y devuelven al pasaje narrativo. La ficha debe ser autocontenida; la prosa, explicativa.

## 2. Advertencia huérfana: dos soluciones, una elegida

**A. Repetir cajas de advertencia en toda la prosa.** Es barato, pero falla: recarga lectura, envejece mal y aun así un recuperador puede cortar antes de la caja.

**B. Rediseñar la unidad recuperable.** Cada ficha contiene obligatoriamente “estado”, “confianza” y “qué no permite concluir”. Es más trabajo inicial, pero la cautela viaja con la afirmación.

Elijo B. Mantendría las advertencias generales de [fuentes y limitaciones](/Users/hectorjure/repos/claudeworkspace/historia/dossier/12-fuentes-y-limitaciones.md:47), pero como contexto, no como control de calidad de cada respuesta.

Matiz contra Claude: el dossier no tiene todas las advertencias separadas; por ejemplo, el bloque 1990-2026 del timeline ya lleva una advertencia contigua. El defecto es que esa cercanía no es una garantía arquitectónica cuando se recupera otro fragmento del mismo período.

## 3. Tres prioridades, en este orden

1. **Construir el registro de afirmaciones portantes y las fichas recuperables.**  
   Antes de “actualizar” hay que saber qué se afirma, con qué fuente y con qué estatus. Claude tiene razón: atribución nítida es prerrequisito. Pero no confundirla con paginar exhaustivamente 37.800 palabras: basta identificar fuente y localizador de las 80–100 afirmaciones que organizan el dossier.

2. **Reescribir 1990-2026 dentro de esa arquitectura.**  
   Es el tramo de mayor uso probable y hoy mezcla bibliografía escasa, prensa y conocimiento general. Cada afirmación debe pasar a fuente institucional o académica adecuada: INDEC para estadísticas sociales y cuentas nacionales, BCRA para series monetarias, CEPAL para series comparables y Boletín Oficial para normas. [INDEC](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7), [BCRA](https://www.bcra.gob.ar/consultas-personalizadas-de-series-estadisticas/), [CEPALSTAT](https://statistics.cepal.org/portal/databank/index.html?area_id=240&indicator_id=2194&lang=es).

3. **Reescribir el núcleo 1852-1916 desde Estado territorial e indígenas, no añadir un apéndice.**  
   Integrar conquista, expropiación, distribución de tierra, subordinación laboral y persistencia de violencia estatal en la explicación del orden agroexportador. Es una corrección de la tesis matriz, respaldada por la historiografía sobre expropiación territorial, no una cuota temática. [Delrio](https://bicyt.conicet.gov.ar/fichas/produccion/10556227).

Queda afuera, por ahora: cuatro dossiers regionales completos, Australia, catálogo integral de series y capítulo autónomo de federalismo fiscal. No porque sean secundarios, sino porque agregan volumen antes de hacer confiable y recuperable lo que ya existe. Federalismo debe entrar como mecanismo en las fichas y en 1990-2026; el capítulo amplio puede esperar.

## 4. Killer mistake

**Que ChatGPT responda una afirmación causal o cuantitativa sin poder recuperar, junto a ella, su procedencia y su límite.**

Ese es el error que invalida el resto. Una mejor historia indígena, regional o comparada no sirve si el sistema sigue extrayendo “la restricción externa explica casi todas las crisis” o un dato de 2026 como hecho asentado, sin mostrar que es una tesis debatida o un dato periodístico provisional.

## 5. Qué no hacer

**No producir un CSV único 1810-2026 de PIB, pobreza, inflación, empleo y salarios.** Sería un objeto visualmente persuasivo y metodológicamente engañoso: mezcla universos, canastas, coberturas y regímenes estadísticos incompatibles. La EPH, por ejemplo, cambia de modalidad en 2003 y cobertura en 2006; pobreza y precios tienen rupturas propias. [Metodología EPH continua](https://www.indec.gob.ar/ftp/cuadros/sociedad/Metodologia_EPHContinua.pdf).

En su lugar, cada ficha que use una cifra debe declarar fuente, universo, período, ruptura y si admite o no comparación.

## 6. Métrica: prueba de recuperación y trazabilidad

Crear un banco fijo de 40 preguntas, equilibrado por período, tema y controversia. Incluir deliberadamente 10 trampas: cifras 2007-2015, pobreza 2014-2015, causalidad de 1973-1976, Conquista del Desierto, peronismo, y coyuntura 2024-2026.

El dossier mejora sólo si, en respuestas generadas con el Proyecto:

- al menos 38/40 respuestas identifican una ficha o fuente concreta;
- 100% de las respuestas basadas en evidencia provisional dicen explícitamente su límite;
- 0/40 transforma una interpretación debatida en hecho establecido;
- al menos 36/40 responden correctamente según una pauta revisada por lectura humana;
- 100% de las cifras incluye período, universo y fuente, o se omite.

Es un test repetible antes y después, no una impresión de “mayor rigor”.

## 7. Discrepancia final con Claude

Estoy de acuerdo en la separación operativa: **1990-2026 se reescribe**, mientras 1880-1990 se actualiza críticamente. Pero no acepto “falsedad” como regla distintiva. Una nota periodística puede informar correctamente un dato contemporáneo; el problema es que no tiene por sí sola la estabilidad, definición metodológica ni trazabilidad requeridas para una síntesis histórica.

Además, el propio dossier ya cita alguna bibliografía académica para el tramo reciente; lo que falta no es literalmente “bibliografía”, sino una **columna vertebral académica y documental**, distribuida por afirmación, que sustituya la dependencia de prensa.

## VEREDICTO RONDA 3

- **Prioridad 1:** fichas recuperables con procedencia, confianza y límite embebidos.
- **Prioridad 2:** reescritura fuente por fuente de 1990-2026.
- **Prioridad 3:** reescritura 1852-1916 desde conquista, territorio y Estado.
- **Killer mistake:** afirmaciones recuperadas sin fuente y cautela inseparables.
- **No hacer:** CSV histórico continuo 1810-2026.
- **Métrica:** benchmark de 40 preguntas con trazabilidad, cautela obligatoria y umbrales verificables.
