Voy a contrastar la propuesta contra estándares y proyectos reales de modelado temporal/cartográfico, y separaré límites técnicos verificables de preferencias.
web search: 
web search: EDTF Level 2 uncertain approximate unspecified dates specification ISO 8601-2 ...
web search: 
web search: Recogito documentation temporal annotation uncertain dates ...
codex
Claude acierta al desconfiar de la “serie continua” pero su modelo de eventos todavía mezcla cosas que deben quedar separadas.

## 1. `eventos.json`: habilitador, sí; pero su esquema es temerario

Un evento discreto no es ontológicamente una serie empalmada. “Hubo una batalla en Ayohuma” puede tener una identidad documental y múltiples afirmaciones sobre ella. Una serie histórica falsa nace al tratar observaciones hechas bajo universos/regímenes incompatibles como mediciones de la misma variable.

El criterio no es “evento vs. serie”, sino éste:

- **Estructura legítima:** transcribe una afirmación ya existente, conserva su alcance, cita una evidencia específica y no obliga a completar campos desconocidos.
- **Estructura fabricada:** convierte una interpretación en atributo obligatorio, normaliza una localización inexistente, colapsa versiones rivales o infiere relaciones para que la visualización funcione.

El JSON de Claude hace tres fabricaciones potenciales:

1. `lat/lon` afirma una localización puntual. Una batalla, una campaña, una redada o una huelga puede tener área, itinerario, lugar disputado o simplemente un topónimo histórico no geocodificable.
2. `mecanismo` y `prueba` obligatorios confunden el hecho con una **afirmación causal sobre el hecho**. Si la gramática causal sólo está aplicada a un pasaje, volverla requerida no la “escala”: produce clasificación retrospectiva masiva.
3. `fichas` no basta como procedencia. Una ficha puede sostener fecha, otra actor, otra consecuencia, y ninguna la coordenada.

Propongo dos capas, no un `eventos.json` monolítico:

```yaml
# entidades/eventos/Ayohuma.yml
id: EVT-1813-AYOHUMA
tipo: batalla
rotulo: Batalla de Ayohuma
tiempo:
  edtf: "1813-11-14"
  display: "14 nov. 1813"
afirmaciones:
  - id: CLM-AYO-FECHA
    predicado: fecha
    valor: "1813-11-14"
    evidencia: [FIC-...]
    estado_epistemico: documentado
  - id: CLM-AYO-LUGAR
    predicado: lugar
    valor: PLC-AYOHUMA
    evidencia: [FIC-...]
```

Las relaciones causales deben ser objetos aparte (`CLM-X-CAUSA-Y`), con su evidencia, alcance y calificación. El build puede derivar un índice liviano para la línea de tiempo. Así, el dato de publicación es reproducible y el modelo de investigación no reescribe el corpus.

Además faltan: `source_locator` (página/folio/URL y cita exacta), versión/fecha de revisión, autor de la codificación, calendario, intervalo y alternativas incompatibles. Sin eso, el JSON se convierte en una segunda autoridad editorial, peor auditada que Markdown.

## 2. `precision` es insuficiente y no es novedoso

Representar fechas imprecisas como intervalos visualmente anchos es correcto, pero no nuevo. Es exactamente la semántica de intervalos temporales y no debería expresarse como un enum propio de cinco valores.

- [EDTF de Library of Congress / ISO 8601-2](https://www.loc.gov/standards/datetime/edtf.html) ya expresa precisión, partes no especificadas (`201X`), aproximación (`~`), incertidumbre (`?`), ambas (`%`) e intervalos abiertos.
- [Wikidata](https://www.wikidata.org/wiki/Help:Dates) almacena precisión, modelo de calendario, límites temprano/tardío y calificaciones como “circa”, “presumiblemente” o “disputado”.
- [CIDOC-CRM](https://cidoc-crm.org/sites/default/files/cidoc_crm_version_7.2.4.pdf) modela el tiempo como extensión, no como instante, incluyendo límites máximos y mínimos.

Adoptaría **EDTF Level 1** como valor serializado canónico, más dos límites computables `earliest` / `latest` para layout. Ejemplos: `1813-11-14`, `1813-11`, `181X`, `1766~`, `../1830`. Para alternativas, no usaría `disputada` como precisión: son dos o más afirmaciones fechadas, cada una con fuente y estado. “Disputada” es epistemología, no resolución temporal.

La codificación visual debe distinguir:

- extensión temporal: ancho;
- aproximación/incertidumbre: textura o contorno;
- hipótesis alternativas: carriles superpuestos etiquetados, no una banda ambigua.

## 3. Falta incertidumbre causal y de magnitud, pero no debe vivir siempre en la marca

Una línea de tiempo debe responder “qué/cuándo”, no pretender condensar toda la epistemología en 12 píxeles.

- **Causalidad:** una arista `A → B`, nunca atributo de A; mostrarla sólo cuando el lector activa “relaciones”. Trazo sólido/documentado, discontinuo/plausible, punteado/conjetural; tooltip/enlace a la afirmación y evidencia. Una flecha no debe aparecer si no hay claim causal explícito.
- **Magnitud:** guardar `valor`, `unidad`, `universo`, `régimen`, `método`, `fuente`, `intervalo/denominador` y `comparabilidad`. Si falta alguno, no hay barra ni escala: hay una nota textual. Prohibido calcular una precisión numérica que la fuente no ofrece.
- **Estado epistemológico general:** pequeño indicador accesible, más texto equivalente; no color como único canal.

El riesgo que Claude no percibe: convertir “confianza” en una falsa probabilidad homogénea. `alta/media/baja` sólo es defendible si tiene una rúbrica pública y revisable; de otro modo es la impresión editorial disfrazada de metadato.

## 4. Tecnología: el umbral no es número de eventos, sino número de nodos mutables

Con 66 fichas y aun unos cientos de eventos, SVG + JavaScript vainilla es suficiente. Pero “SVG generado por `build.py`” contradice filtros y zoom: si la interacción cambia el estado, el cliente necesita datos y un renderer incremental, no sólo SVG estático.

Umbrales operativos razonables:

- Hasta **~500 marcas DOM activas**, filtros discretos y zoom por tramos: SVG nativo, `viewBox`, eventos delegados; nada de D3.
- **500–2.000 nodos mutables** o etiquetas con colisión dinámica: SVG aún posible, pero usar `d3-scale`, `d3-array` y quizá `d3-force` como módulos aislados se justifica. D3 no implica framework ni “todo D3”.
- Más de **~2.000–5.000 nodos visibles y redibujados durante pan/zoom**, o animación continua: Canvas para marcas, SVG/HTML para foco, etiquetas y accesibilidad. No es un límite universal, pero el coste decisivo es el DOM y sus listeners, no el total del JSON.
- Framework sólo cuando aparezcan **estado compartido complejo**: URL sincronizada con filtros/zoom/paso, paneles coordinados, preservación de estado entre rutas, carga parcial/caché y componentes reutilizados en tres o más vistas. Antes de eso, un reducer chico + `history.pushState` es más durable que SvelteKit.

D3 se justificaría concretamente para escala temporal robusta, ticks adaptativos y layout de colisiones; no para dibujar círculos. No justifica por sí solo npm si se copian tres funciones pequeñas y se las prueba.

## 5. Mapa: no usaría ni SVG propio “histórico” ni tiles en v1

Un mapa base contemporáneo más pines de 1813 no es una mera imprecisión: afirma una territorialidad y una jurisdicción actuales. Un SVG propio no corrige eso; sólo fija el error en el repositorio.

- [Natural Earth](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/) es excelente base actual, pero no solución histórica.
- [CShapes 2.0](https://icr.ethz.ch/data/cshapes/CShapes-2.0_Codebook.pdf) ofrece fronteras estatales históricas 1886–2017; por cobertura, no resuelve 1810–1885 ni divisiones subnacionales argentinas.
- [OpenHistoricalMap](https://www.openhistoricalmap.org/export?locale=en-GB) es CC0 salvo excepciones y puede exportarse, pero su completitud espacial y temporal debe auditarse por recorte: no puede ser autoridad silenciosa.
- El [GeoRef/IGN](https://www.argentina.gob.ar/georef/descarga-de-la-base-completa) es actual, útil sólo si se rotula explícitamente como referencia moderna.

Decisión: **mapa sólo para un recorrido cuyo argumento sea espacial y tenga cartografía histórica fuente-específica** (raster georreferenciado o polígonos versionados, con fecha, autor, proyección, licencia y advertencia de alcance). Para el resto, topónimos y una mini-región esquemática sin fronteras políticas. Tiles agregan proveedor, red y licencia sin resolver el problema historiográfico.

## 6. La fragilidad omitida

La más grave es la **deriva entre corpus y derivados**. Habrá Markdown, fichas, eventos, recorridos y páginas compiladas; cada corrección puede dejar cuatro versiones contradictorias. El build debe fallar si un ID citado no existe, si falta evidencia, si un evento publicado no tiene claim de fecha/lugar correspondiente, o si una ficha cambió y no se regeneró el índice. Añadir JSON Schema y validación al Python existente vale más que diseñar la primera visualización.

También falta una política de **granularidad**. ¿“Revolución de Mayo” es un evento, proceso, período o 30 eventos? Sin reglas de descomposición y deduplicación, la línea premia lo fácilmente fechable —élites, decretos, batallas— y hace parecer que lo social, indígena, afroargentino y laboral “no ocurrió”.

La prueba contra degradación debe ser comparativa: asignar lectores aleatoriamente a capítulo vs. experiencia; medir recuerdo factual, distinción DOC/INF/CIRC, calibración (“¿qué tan seguro estás?”), y transferencia ante una afirmación nueva. Criterio previo: la experiencia no puede ser inferior en exactitud ni en calibración, y debe mejorar navegación/retención para justificarse.

## VEREDICTO RONDA 1

- `eventos.json` es habilitador si deriva de claims trazables; es artefacto falso si obliga coordenadas, mecanismos o certezas.
- Reemplazar `precision` por EDTF + intervalos computables + afirmaciones alternativas.
- No introducir framework en v1; usar módulos D3 sólo al superar ~500 nodos mutables o necesitar layout/escala no trivial.
- Descartar el mapa como formato general de v1: los datasets disponibles no cubren el problema argentino temprano con la precisión requerida.
- La amenaza principal no es “tres formatos”: es una segunda base editorial sin procedencia, validación ni sincronización con el corpus.