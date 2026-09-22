# R1 · Réplica de Claude

## Lo que concedo sin pelear

**1. EDTF, no un enum inventado.** Tenía razón y es el tipo de error que más me molesta: iba a fabricar un vocabulario de cinco valores para un problema que la Library of Congress ya resolvió. [EDTF / ISO 8601-2](https://www.loc.gov/standards/datetime/edtf.html) expresa precisión, partes no especificadas (`181X`), aproximación (`1766~`), incertidumbre (`1847?`), ambas (`%`) e intervalos abiertos (`../1830`). Adopto **EDTF Level 1 como valor canónico** más `earliest`/`latest` derivados para layout. Beneficio que no había visto: es interoperable con Wikidata y con cualquier archivo serio, así que el corpus deja de ser un silo.

**2. `disputada` no es una precisión, es epistemología.** Corrección limpia. Dos fechas rivales son **dos afirmaciones fechadas con fuente cada una**, renderizadas en carriles etiquetados, no una banda ambigua que promedia el desacuerdo. Lo segundo es exactamente el pecado que el corpus le reprocha a las series empalmadas.

**3. `lat/lon` fabrica una puntualidad que no existe.** Concedido. Una batalla tiene área, una campaña tiene itinerario, una deportación tiene origen y destino, y algunos topónimos históricos no son geocodificables. Obligar coordenada es obligar invención.

**4. `mecanismo` y `prueba` no son atributos del hecho.** Este es el mejor golpe de la ronda. Confundí el hecho con una afirmación causal sobre el hecho. La causalidad es una **arista con su propia evidencia**, nunca una propiedad del nodo. Y volver obligatoria una gramática causal que está aplicada a 1 de 15 capítulos no la escala: produce clasificación retrospectiva masiva, que es fabricación con otro nombre.

**5. Validación antes de visualización.** Acepto la inversión de prioridades: JSON Schema y un build que **falle** valen más que la primera visualización. Sin eso hay cuatro versiones contradictorias de cada corrección y el proyecto se degrada solo.

**6. El mapa sale de la v1.** Tu evidencia lo cierra: [CShapes 2.0](https://icr.ethz.ch/data/cshapes/) cubre 1886-2017 y el problema argentino interesante es 1810-1885; OpenHistoricalMap es CC0 pero su completitud hay que auditarla por recorte. Un mapa base moderno con pines de 1813 **afirma** una territorialidad actual, y en un corpus que tiene un capítulo entero sobre Estado y territorio eso no es un detalle estético: contradice la tesis del capítulo.

---

## Donde sostengo, con argumento

### El modelo de claims es correcto en teoría y letal en la práctica

Tu esquema —evento con `afirmaciones[]`, cada una con predicado, valor, evidencia y estado epistémico— es la modelización correcta. Es también, para este proyecto, la vía más segura a que la capa de datos **no exista nunca**.

Contá el trabajo: un evento con 4 predicados (fecha, lugar, actores, consecuencia) son 4 claims con 4 `source_locator` verificados. Ochenta eventos son 320 claims. Con una persona, eso no es una v1: es un año. Y el corpus ya tiene un precedente exacto de este fracaso —la gramática causal, declarada con todo rigor y aplicada a **un solo pasaje** porque el costo por unidad era demasiado alto.

**El test que propongo para el esquema: ¿permite publicar 80 eventos con procedencia real en un fin de semana?** El tuyo no. Y un esquema que nadie puede poblar tiene exactamente el mismo valor epistémico que no tener datos, con más deuda.

Contrapropuesta, que toma tus correcciones sin el costo:

```yaml
# datos/eventos/1813-11-14-ayohuma.yml
id: EVT-1813-AYOHUMA
rotulo: Derrota de Ayohuma
tipo: batalla
tiempo:
  edtf: "1813-11-14"          # canónico
  earliest: 1813-11-14        # derivado por el build
  latest: 1813-11-14
lugar:
  tipo: area                  # punto | area | itinerario | no_localizable
  topónimo: "Ayohuma, Alto Perú (actual Bolivia)"
  geo: null                   # ausente es un valor legítimo, no un hueco
ejes: [militar, genero, afrodescendientes]
procedencia:                  # NO opcional. Sin esto el evento no compila.
  - ficha: MUJ-1774-VALLE-01
    sostiene: [fecha, participacion]
  - capitulo: 03-revoluciones
    sostiene: [resultado]
estado: documentado           # del EVENTO: que ocurrió y cuándo. Nada más.
```

Tres diferencias con tu modelo, y las tres son concesiones a tu crítica dentro de un presupuesto realizable:

- **`procedencia[]` con `sostiene[]`** captura tu punto real —que una ficha sostiene la fecha y otra el actor— sin promover cada predicado a objeto de primera clase. Es tu idea al 70% del valor y al 15% del costo.
- **`estado` califica sólo la existencia y fecha del evento.** No hay `mecanismo` ni afirmación causal en el nodo. Las relaciones van aparte, en `datos/relaciones.yml`, y **sólo existen cuando hay un claim causal explícito en el corpus**. Hoy eso significa: casi ninguna. Correcto. La línea de tiempo no dibuja flechas que nadie escribió.
- **`geo: null` es un valor válido y frecuente.** El renderer tiene que funcionar con la mayoría de los eventos sin coordenada. Si no funciona, el renderer está mal, no los datos.

`source_locator` con página o folio lo acepto **para eventos cuya procedencia sea archivo directo**, no para los que se apoyan en una ficha que ya lo declara. Duplicar el locator es duplicar la autoridad, que es justo lo que querés evitar.

### SVG del servidor sí soporta filtros y zoom

Decís que "SVG generado por `build.py`" contradice filtros y zoom. Con tu propio umbral, no:

- **Filtrar** = alternar atributos/clases sobre nodos ya presentes en el DOM. Es exactamente el patrón que ya usa el explorador de 66 fichas: renderizado en servidor, JS sólo oculta. Funciona sin JS y lo indexan los buscadores.
- **Zoom** = animar `viewBox`. Una propiedad, aceleración nativa, sin redibujar nada.
- Con ~500 marcas —tu propio piso— ninguna de las dos necesita renderer incremental.

Coincidimos más de lo que parece: **por debajo de 500 nodos mutables, nada; entre 500 y 2.000, `d3-scale` y `d3-array` sueltos.** Acepto el umbral y lo adopto como regla escrita en vez de criterio estético. Y acepto tu matiz: D3 se justifica por **ticks temporales adaptativos y layout de colisión de etiquetas**, que son problemas reales, no por dibujar círculos.

---

## Lo que aporto nuevo: tu mejor crítica se puede convertir en la mejor función

Tu punto sobre granularidad es el más fuerte del debate y lo subvendiste como problema de reglas:

> Sin reglas de descomposición y deduplicación, la línea premia lo fácilmente fechable —élites, decretos, batallas— y hace parecer que lo social, indígena, afroargentino y laboral "no ocurrió".

Es peor de lo que decís: `12-fuentes-y-limitaciones.md` **ya declara ese sesgo** entre sus once, y `10-mujeres.md` §0 explica el mecanismo (el registro estatal fue diseñado por y para varones propietarios). Una línea de tiempo ingenua no introduciría un sesgo nuevo: **reproduciría, con autoridad visual y sin advertencia, el sesgo que el corpus denuncia por escrito.** Sería la peor página del sitio.

Pero las reglas de descomposición no alcanzan, porque el sesgo no está en mi criterio de carga: está en el archivo. Por más prolijo que sea, va a haber cuarenta hechos militares fechables al día y seis laborales fechables a la década. **La única salida honesta es hacer el sesgo visible en vez de compensarlo a mano.**

Propuesta: **franja de densidad documental.** Bajo la línea de tiempo, una tira por eje que muestra cuántos hechos hay por década y con qué precisión. El lector ve, sin leer metodología, que el eje militar está poblado y fechado al día mientras el laboral está ralo y fechado a la década. Y un texto corto que diga por qué: *esto no mide qué pasó, mide qué quedó registrado y quién lo registró.*

Eso convierte la vitrina en argumento. Es la versión gráfica del panel de incertidumbre y **es la función que justifica todo el proyecto**: la única línea de tiempo de historia argentina que muestra los huecos del archivo en vez de taparlos.

## Una deuda tuya que acepto y escalo

> `alta/media/baja` sólo es defendible si tiene una rúbrica pública y revisable; de otro modo es la impresión editorial disfrazada de metadato.

Tenés razón y el problema es más grande que el sitio: **66 fichas publicadas declaran `confianza` sin rúbrica publicada.** No es deuda de la capa de experiencia, es deuda del corpus, y la capa de experiencia la vuelve visible porque va a usar ese campo para filtrar. Hay que escribir la rúbrica y auditar las 66 contra ella. Lo agrego al plan.

---

## Preguntas para R2 (foco: UX, editorial y producto — no vuelvas a arquitectura)

1. De los tres formatos, ¿cuál descartás para la v1 y por qué? Quiero que elijas uno, no que los ordenes.
2. El "corte transversal" (¿qué pasaba en 1913?) es lo que el usuario pidió más literalmente y lo que más riesgo tiene de mentir: junta economía, cultura y salud en una pantalla cuando el corpus prohíbe encadenar sus cifras. ¿Se puede hacer honesto, o hay que matarlo?
3. Los recorridos cuestan como una monografía cada uno. Con una sola persona escribiendo: ¿tres recorridos flacos o uno bueno? ¿Y cuál primero?
4. ¿Cómo evitás que la capa narrativa canibalice la de consulta en vez de alimentarla? Quiero un mecanismo, no una intención.
5. Pasos discretos con clic (Kosara) vs. scroll sincronizado: ¿qué elegirías para un lector en móvil, que va a ser la mayoría?
6. Si tuvieras que matar una sola cosa de toda la propuesta para que el resto salga bien, ¿qué matás?
