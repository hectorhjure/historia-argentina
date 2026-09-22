# R0 · Análisis inicial: la capa de experiencia

## TL;DR

1. **La investigación encontró algo que contradice el pedido.** La literatura sobre scrollytelling reporta que los lectores *sienten* que se concentran más sin aprender más detalles. Para un corpus cuyo valor entero es la precisión, ese es el peor intercambio posible. La propuesta tiene que estar diseñada contra ese riesgo, no ignorarlo.
2. **El cuello de botella no es tecnológico: es de datos y de prosa.** No existe capa de eventos estructurados —las cronologías son prosa— y un recorrido narrativo bueno cuesta lo mismo que una monografía. El código es la parte fácil y barata.
3. **La idea más fuerte que tengo es representar la incertidumbre temporal como ancho físico.** Un hecho fechado al día es una marca; uno fechado a la década es una banda. Se ve la textura del archivo de un golpe de vista. No conozco a nadie que lo haga.
4. **Recomiendo no meter framework.** El sitio actual son 87 páginas estáticas, ~250 líneas de CSS y ~200 de JS vainilla. Eso va a seguir compilando en cinco años. SvelteKit + D3 agregarían toolchain, lockfile y ~150 KB por interacciones que son triviales.
5. **El modo de fracaso real:** construir una cáscara hermosa con tres recorridos de demostración que nunca crecen, mientras la capa de consulta —que funciona— se queda sin monografías nuevas.

---

## 1. El problema de diseño, formulado con precisión

El corpus vale por dos cosas: **cada afirmación declara su fuente** y **31 puntos declaran que no se sabe**. Todo el aparato —fichas autocontenidas, marcado `[DOC]`/`[INF]`/`[CIRC]`, prohibición de encadenar series estadísticas, panel de incertidumbre— existe para que nadie use este material creyendo que es más firme de lo que es.

La narración inmersiva tiene la propiedad inversa. Su falla característica, documentada, es **producir sensación de comprensión sin comprensión**:

> Producers of scrollytelling should be aware that even if people express they can focus more, they may be describing an overall feeling of engagement rather than actually focusing and learning specific details.
> — *The Impact of Scrollytelling on the Reading Experience of Long-Form Journalism*, ACM 2023

Y la épica narrativa empuja exactamente hacia lo que `14-regimenes-estadisticos.md` prohíbe: la línea continua, la cifra sin universo, la causa sin grado de prueba. Una animación que dibuja el PIB argentino de 1810 a 2026 como una curva suave es hermosa y es una mentira que el propio corpus tipifica como "artefacto falso".

**Por lo tanto el criterio de éxito no es "que sea lindo e inmersivo".** Es: *que un lector que recorra la experiencia salga sabiendo qué está probado, qué es interpretación y qué no se sabe* —y que lo sepa **mejor** que leyendo el capítulo, no peor.

Si la capa de experiencia no supera esa prueba, no hay que construirla. El sitio de consulta ya funciona.

## 2. Qué NO hacer, con fundamento

De la literatura, tres descartes concretos:

- **Scrolljacking.** Kosara lo tipifica como error grave. El scroll se sincroniza (si el dedo se detiene, la animación se detiene) o no se toca.
- **Parallax.** Dispara trastornos vestibulares: vértigo, náusea, migraña. Máximo un efecto sutil, con alternativa sin movimiento.
- **Túnel.** Si para llegar a otra parte del sitio hay que atravesar la historia entera, el lector se va.

Y un descarte propio: **nada de "modo inmersivo" que reemplace la lectura**. Las dos caras coexisten; ninguna es la versión degradada de la otra.

El criterio positivo más útil que encontré es de David Sleight (ProPublica), y funciona como test, no como estilo:

> Si necesitamos crear un momento de pausa, o si el objetivo es permitir comparaciones y/o mostrar cambios en el tiempo, puede ser muy útil.

**Test de admisión:** un recorrido se construye sólo si necesita pausa, comparación o cambio en el tiempo. Si no, es un capítulo y se lee como capítulo.

## 3. La propuesta

### Capa 0 · `datos/` — lo que habilita todo (y hoy no existe)

Eventos estructurados, con la misma disciplina que las fichas. El campo decisivo:

```json
{
  "id": "1813-11-14-ayohuma",
  "fecha": "1813-11-14",
  "precision": "dia",
  "titulo": "Derrota de Ayohuma",
  "ejes": ["militar", "genero", "afrodescendientes"],
  "lugar": { "nombre": "Ayohuma, Alto Perú", "lat": -18.9, "lon": -65.9 },
  "mecanismo": "SHOCK",
  "prueba": "documentado",
  "fichas": ["MUJ-1774-VALLE-01"],
  "capitulos": ["03-revoluciones"],
  "monografias": ["VID-1774-VALLE-01"]
}
```

`precision` toma `dia | mes | año | decada | disputada`. **Es el campo que evita repetir el error del CSV descartado.** Una línea de tiempo que dibuja "c. 1766" como un punto miente con la misma lógica con la que miente una serie de PIB empalmada.

`mecanismo` y `prueba` reusan la gramática causal de `12-fuentes-y-limitaciones.md` §2 ter, que hoy está aplicada a un solo pasaje. La capa de datos la vuelve obligatoria: no se puede cargar un evento sin declarar grado de prueba.

**Esto es lo que hace que sean dos caras de una misma moneda y no dos sitios.** Ambas leen el mismo sustrato.

### Capa de experiencia · tres formatos, no uno

**A · Línea de tiempo con incertidumbre visible.** SVG, 1516-2026, zoom por escalas. Cada evento se dibuja según su `precision`: marca fina si es al día, banda si es a la década, banda rayada si está disputada. Filtros por eje y por grado de prueba. *El lector ve dónde el archivo es firme y dónde se deshilacha, sin leer una palabra sobre metodología.*

**B · Recorridos.** Secuencias curadas de 8-15 eventos con prosa de enlace. Pasos **discretos** con avance por clic/teclado —siguiendo a Kosara: si la historia va en pasos, la interacción va en pasos— no scroll secuestrado. Candidatos naturales, porque el corpus ya tiene el material: *Las Marías* · *La invención del Estado (1852-1880)* · *Cuatro golpes y una constitución* · *El borramiento de la población afroargentina*.

**C · Cortes transversales — "¿Qué pasaba en 1913?"** El formato que sitúa al lector, que es lo que se pidió. Un año, y alrededor: quién gobernaba, qué compraba un salario, qué se publicaba, qué se escuchaba, de qué se moría la gente, qué se estaba construyendo.
**Con una regla que lo salva o lo hunde:** cada celda declara universo y fuente, y **las celdas sin dato dicen "no hay dato comparable" en vez de interpolar.** Los huecos son el contenido: muestran dónde el archivo argentino se adelgaza. Un corte de 1913 va a estar lleno; uno de 1830, casi vacío. Eso *enseña* algo verdadero.

### Tecnología · la recomendación impopular

**Nada nuevo.** Ni SvelteKit, ni D3, ni npm.

Las interacciones que necesito son: un scrubber temporal, render filtrado de eventos y navegación por pasos. Las escalas son año→píxel. D3 resuelve problemas que no tengo.

- SVG generado por el mismo `build.py`
- `IntersectionObserver` para disparar pasos (nunca `scroll` listeners)
- Animaciones CSS con `animation-timeline: view()` donde haya soporte, degradando a estático
- `prefers-reduced-motion` respetado con alternativa completa sin movimiento
- Mapa: **SVG propio, no Leaflet/MapLibre.** No depende de que un proveedor de tiles siga siendo gratis, pesa una fracción y se puede tematizar con las mismas variables CSS
- Presupuesto duro: **< 60 KB de JS** en cualquier página, LCP < 2,5 s en 4G

El sitio actual no tiene toolchain. Eso no es pobreza, es durabilidad.

## 4. Lo que yo mismo veo débil

Honestamente, y para que Codex ataque esto y no hombres de paja:

1. **El costo real es editorial, no técnico.** Un recorrido bueno son 1.500-2.500 palabras de prosa nueva más la curaduría de sus eventos: el esfuerzo de una monografía. Tres recorridos = tres monografías que no se escribieron. **No tengo resuelto si eso es la mejor asignación del esfuerzo.**
2. **La capa de datos puede ser un artefacto falso.** Extraer eventos de prosa e imponerles `lat/lon`, `mecanismo` y `prueba` es exactamente el tipo de operación que produjo el CSV que hubo que descartar. `precision` mitiga la fecha, no el resto.
3. **No sé si el corte transversal tiene datos suficientes.** Para 1913 seguro. Para 1830 puede quedar tan vacío que sea inútil en vez de elocuente. No lo verifiqué.
4. **Tres formatos es probablemente uno de más** para una primera versión, y no tengo claro cuál sacrificar.
5. **Riesgo de abandono:** una cáscara hermosa con tres recorridos que nunca crecen es peor que no tenerla, porque compite por atención con la capa que sí funciona.

## 5. Preguntas para Codex (R1 · arquitectura y datos)

1. ¿La capa `datos/eventos.json` es habilitadora o es el CSV descartado con otro nombre? Si es lo segundo, ¿cuál es la alternativa que da línea de tiempo real sin fabricar estructura?
2. ¿`precision` alcanza para no mentir, o hace falta además representar la incertidumbre de **atribución causal** y de **magnitud**? ¿Cómo, sin volverlo ilegible?
3. Vainilla vs. framework: ¿en qué punto concreto de complejidad se rompe mi recomendación? Dame el umbral, no la opinión.
4. ¿Mapa SVG propio o tiles? Argentina cambió de fronteras y de jurisdicciones muchas veces; un mapa moderno con eventos del siglo XIX es un anacronismo. ¿Cómo se resuelve eso sin cartografía histórica propia?
5. De los tres formatos (línea de tiempo / recorridos / cortes transversales), ¿cuál tiene mejor relación valor-esfuerzo para la v1, y cuál descartarías?
6. ¿Cómo se mide que la experiencia **no** degradó la comprensión? Quiero un test, no una intuición.
