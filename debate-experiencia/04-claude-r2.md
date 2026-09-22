# R2 · Réplica de Claude

## La franja de densidad está muerta y tenés razón

Era mi mejor idea de la R1 y el golpe es limpio:

> no mide el archivo; mide lo que esta persona eligió y pudo cargar como evento

Es el mismo error que la franja pretendía denunciar, un nivel más arriba. Yo iba a publicar una tira cuantificada, con aura científica, cuyo denominador real era **mi propia carga incompleta**, y rotularla "densidad documental" — es decir, presentar una cobertura parcial como medición del pasado. En un corpus que tiene un capítulo dedicado a prohibir exactamente esa operación con las series del INDEC, habría sido la página más hipócrita del sitio.

Acepto tu reformulación completa: vuelve, si vuelve, como **ledger de cobertura editorial**, con denominador declarado —qué se buscó, con qué estrategia, qué cuenta como evento, quién codificó, qué quedó afuera— y fuera de la v1. Para la v1, una nota metodológica honesta vale más que una visualización que miente con elegancia.

## Concedido sin pelear

**Cortes transversales fuera de la v1.** Tu argumento es de costo, no de imposibilidad: cada año es una pequeña monografía de comparabilidad en cuatro dominios. Y tu rescate —"1913: cuatro ventanas, no una fotografía total", con tarjetas independientes y la ausencia ocupando espacio real— es el diseño correcto para cuando se haga. Lo guardo textual.

**Un recorrido bueno, no tres flacos. Valle primero.** De acuerdo.

**Y tenés razón en el título, que es más importante de lo que parece.** "La heroína olvidada" resuelve moralmente lo que el recorrido debería hacer pensar. **"Quién puede quedar en la historia"** deja la pregunta abierta, que es lo que el material exige: el problema de Valle no es que la olvidaron, es que el archivo la registró con el apellido de quien la esclavizó y después con el de Rosas, y que la fecha que hoy es feriado nacional es su baja administrativa.

**Pasos discretos.** Aceptado, con tu especificación: botones grandes y persistentes, progreso textual ("4 de 9"), índice de estaciones, **URL compartible por estación** —ese detalle es el que hace citable el recorrido— y scroll sólo dentro de cada estación. Swipe como atajo señalado, nunca como único avance.

**El "dossier de escena" es mejor que lo que yo propuse.** Un documento como objeto central, primera persona documental y no ficcional, con lo que se sabe, lo que se infiere y lo que no puede saberse marcado. Sitúa más que cualquier panorama y cuesta menos prosa. Lo adopto como **unidad estructural del recorrido**, no como estación ocasional.

---

## Donde corrijo un supuesto que los dos dábamos por bueno

En R0 escribí que un recorrido cuesta como una monografía, y vos lo aceptaste y construiste tu decisión de v1 sobre eso. **Es falso, y descubrirlo reordena el plan.**

Mirá lo que la monografía de Valle ya contiene, transcripto y con procedencia verificada:

| Documento | Ya está en el corpus |
|---|---|
| Partida de bautismo, 22/11/1774 | Transcripta completa |
| Acuerdos del Extinguido Cabildo, 7/9/1807 | Transcripto completo |
| Tarifa de pensiones por "clase y calidad", 18/7/1807 | Transcripto completo |
| Memorias de Lamadrid, versión 1895 | Transcripta |
| Memorias de Lamadrid, versión 1855 | Transcripta |
| Declaración de Hipólito Videla, 17/1/1827 | Transcripta |
| Declaración de Maga Pérez, 2023 | Transcripta |

**Son siete dossiers de escena ya escritos.** El recorrido no es prosa nueva: es **re-puesta en escena de prosa existente** como estaciones, con la conexión narrativa y las preguntas. El costo real del primero está más cerca de 600 palabras nuevas que de 2.500.

Y de ahí sale la consecuencia que importa: **el segundo recorrido sí cuesta caro, porque Azurduy no tiene monografía.** Es decir:

> **Un recorrido es siempre aguas abajo de una monografía. Nunca en paralelo.**

Ese es el mecanismo anticanibalización que pediste, y es mejor que enlazar bien, porque es **económico y no depende de la disciplina de nadie**: no se puede producir un recorrido sin haber hecho antes el trabajo de archivo. Si el proyecto quiere más recorridos, está obligado a escribir más monografías. La capa narrativa deja de competir con la de evidencia y se convierte en su incentivo.

Tu mecanismo de trazabilidad —bloque "Qué sostiene esta escena" por estación, "Aparece en estos recorridos" en cada ficha, botón "volver a explorar" preservando eje y período, y prohibición de duplicar prosa— lo adopto entero. Los dos mecanismos son complementarios: el tuyo hace auditable la narración, el mío impide que exista sin evidencia detrás.

## Donde sostengo: la línea de tiempo sale en la v1

Decís que la línea "puede salir como índice/orientación mínimo, pero no como el producto inaugural". Estamos de acuerdo en el alcance y quiero fijarlo, porque hay un límite que no podés ver desde tu lado del debate: **el usuario pidió explícitamente "una línea de tiempo más fuerte".** Si la v1 entrega un solo recorrido, no entregamos "dos caras de una misma moneda": entregamos un tercer micrositio suelto.

La línea de tiempo cumple tres funciones que ningún recorrido cubre:
1. **Es la columna de navegación** que conecta las dos caras: desde un punto se salta al capítulo, a la ficha o al recorrido que lo atraviesa.
2. **Es donde el ancho EDTF hace su trabajo.** Es el único lugar del sitio donde la incertidumbre temporal se ve en vez de leerse.
3. **Es lo que hace que el recorrido no flote.** Una estación de 1813 tiene sentido distinto si el lector ve qué había alrededor.

Alcance v1, acotado: 1516-2026, eventos con procedencia obligatoria, ancho por EDTF, filtros por eje, **sin franja de densidad, sin mapa, sin flechas causales.**

## Tu riesgo editorial lo convierto en un chequeo de build

Tu punto 7 es el más importante del debate entero:

> la inmersión amplifica sesgo porque reduce fricción: el lector siente continuidad y causalidad antes de evaluarlas

Y el corpus es especialmente vulnerable porque **ya declara estar narrado como historia de decadencia**, y declara que eso es una elección interpretativa. Un recorrido con transiciones fluidas y una línea que cae convierte esa elección en destino.

Tus medidas las tomo todas. Y agrego una que las vuelve exigibles en vez de buenas intenciones: **un linter de vocabulario teleológico en `sitio/qa.py`**, que falla el despliegue. Lista inicial: *condujo inevitablemente · estaba destinado · fracaso anunciado · desde entonces nunca · el fin de · la decadencia argentina · no pudo sino*. El corpus ya tiene un control de calidad que aborta la publicación por una tabla sin scroll; que aborte también por prosa determinista es la misma idea aplicada donde más importa.

La tarjeta **"otra lectura posible"** pasa a ser obligatoria por recorrido, no opcional, y con desacuerdo historiográfico real —el corpus tiene cinco debates identificados en `00-resumen-ejecutivo.md`— no falso balance.

## Duda honesta que no resolvimos

Los facsímiles. El dossier de escena pide **ver** el documento, y ahí hay un problema de licencia que ninguno de los dos verificó: la partida de 1774 está en FamilySearch, que exige cuenta y restringe redistribución. Los *Acuerdos del Extinguido Cabildo* son volúmenes publicados del siglo XIX, presumiblemente dominio público, pero **presumiblemente no es verificado**. Si no hay facsímil, ¿el dossier de escena funciona sólo con transcripción tipografiada? Creo que sí, y que incluso puede ser mejor —la transcripción es legible y el facsímil suele no serlo— pero es una pregunta abierta de diseño, no una certeza.

---

## Preguntas para R3 (cierre: go/no-go, riesgos, plan, killer mistake)

1. **Go / no-go.** Con todo lo acordado: ¿esto se construye o el esfuerzo rinde más en escribir la segunda monografía? Respondé una cosa.
2. Si es go: ¿cuál es el **alcance mínimo publicable** que ya vale la pena, y qué queda explícitamente para después?
3. ¿Cuál es el **killer mistake** de este proyecto: el error que, si se comete, hace que todo lo demás no importe?
4. Ordená los **tres riesgos principales** por probabilidad × impacto, con mitigación concreta para cada uno.
5. ¿Cómo se mide el éxito? Quiero **una métrica norte**, no un tablero.
6. ¿Qué parte del plan acordado sigue pareciéndote mal y estás aceptando por concesión y no por convicción? Decilo ahora.
