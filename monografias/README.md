# Monografías — la tercera capa

## Por qué existe

El dossier tiene un problema declarado en `../dossier/12-fuentes-y-limitaciones.md`: **hay historias que en una síntesis quedan reducidas a una fila de tabla, y son justamente las que más se perdieron**. Una fila de tabla puede decir "María Remedios del Valle, afroargentina, combatió, terminó mendigando". No puede decir que su apellido es el de la mujer que la tuvo esclavizada, que después figuró en las listas militares con el apellido de Rosas, y que la fecha que hoy es feriado nacional es en realidad su fecha de baja del ejército y no la de su muerte, que nadie encontró.

Esas tres cosas no caben en una fila. Y sin ellas, la fila es una versión empobrecida que además repite errores.

## Las tres capas

| Capa | Dónde | Unidad | Pregunta que responde |
|---|---|---|---|
| **1 · Síntesis** | `../dossier/00` a `14` | Capítulo | ¿Qué pasó y cómo se discute? |
| **2 · Evidencia** | `../dossier/fichas/` | Ficha autocontenida | ¿Cuál es la prueba y cuál es su límite? |
| **3 · Profundidad** | `monografias/` (acá) | Monografía | ¿Cómo lo sabemos, documento por documento? |

Las capas no se sustituyen. Se leen en orden inverso según la necesidad: el dossier para entender, la ficha para citar, la monografía para discutir.

## Tipología

Tres tipos, con prefijo en el id:

- **`VID-`** — **Vidas.** Una persona. No es una biografía completa: es la reconstrucción crítica de lo que el archivo permite afirmar sobre ella.
- **`EPI-`** — **Episodios.** Un hecho o una secuencia corta (una batalla, una huelga, un juicio, una ley).
- **`PRO-`** — **Procesos.** Un arco largo (la formación de un mercado de tierras, la construcción del sistema de salud pública, el borramiento estadístico de la población afrodescendiente).

Formato del id: `TIPO-AÑO-CLAVE-NN`. El año es el de anclaje, no necesariamente el de nacimiento o inicio.

## Reglas de la capa

**1. Extensión.** Entre 3.000 y 6.000 palabras. Menos que eso es una ficha larga; más, un capítulo mal ubicado.

**2. Aparato propio.** Toda monografía cierra con su lista de fuentes clasificadas por tipo (archivo / académica / divulgación / prensa / normativa) y con una sección **«Qué falta investigar»**. Si no puede escribirse esa sección, la monografía no está lista.

**3. Marcado de inferencia.** Regla tomada de Florencia Guzmán, que la formula mejor que nadie: *cualquier investigación histórica admite inferencias e incluso imaginación, pero siempre deberían enunciarse como tales* («supongo», «infiero», «habría sido»). En estas monografías la inferencia se marca **siempre**, y se distingue de lo documentado con la gramática causal de `../dossier/12-fuentes-y-limitaciones.md` §2 ter.

**4. Enlace bidireccional obligatorio.** El frontmatter declara `desde_dossier:` (qué pasajes apuntan acá) y `fichas:` (qué fichas sostiene o genera). El pasaje del dossier lleva el marcador `▸` con el enlace relativo. Un enlace en un solo sentido es un error de la capa, no un detalle.

**5. La monografía puede contradecir al dossier —y cuando lo hace, manda.** Es el punto que justifica toda la arquitectura. Profundizar sirve para encontrar errores de la síntesis, no solo para agregar color. Toda monografía que corrige algo abre con una sección **«Qué corrige del dossier»**, y la corrección se aplica al capítulo y a la ficha en el mismo movimiento. Si la monografía queda con una corrección sin aplicar aguas arriba, la capa falló.

**6. Sin hagiografía inversa.** `../dossier/10-mujeres.md` §202 ya lo advierte: recuperar figuras borradas es reparación historiográfica y hay que hacerlo con rigor. Una monografía que solo eleva no sirve: tiene que poder decir qué no se sabe y qué se inventó.

## Cómo entra en el Proyecto de ChatGPT

El plan Plus admite 25 archivos y `../chatgpt-project/` usa 18. Las monografías **no suben de a una**: se consolidan en paquetes temáticos (`17-monografias-mujeres.md`, `18-monografias-...`), igual que las 66 fichas se consolidaron en `15-fichas-de-evidencia.md`. La recuperación sigue funcionando porque ChatGPT recupera fragmentos, no archivos, y cada monografía es autocontenida y abre con su encabezado completo.

Capacidad: **7 paquetes libres**. A razón de 3-5 monografías por paquete, el techo está en torno a 25-35 monografías sin tocar el límite del plan.

## Índice

| Id | Título | Tipo | Estado |
|---|---|---|---|
| [`VID-1774-VALLE-01`](VID-1774-VALLE-01-maria-remedios-del-valle.md) | María Remedios del Valle | Vida | Completa |

## Cola de trabajo

> La lista de prioridades del proyecto entero está en el [README del repositorio](https://github.com/hectorhjure/historia-argentina#próximos-pasos). Ésta es sólo el orden interno de esta capa.

Por orden de rendimiento esperado —es decir, de cuánto corrigen al dossier, no de cuán atractivas son:

1. **`VID-1780-AZURDUY-01` — Juana Azurduy.** Mismo problema que Del Valle y peor resuelto: el dossier repite el relato de mando militar sin discutir qué documenta y qué no. Es la comparación natural.
2. **`PRO-1810-MARIAS-01` — Las Marías.** La categoría de Guzmán aplicada al conjunto: mujeres afrodescendientes y de sectores populares en las guerras de independencia. Convierte la monografía individual en historia social y desactiva el efecto «excepción».
3. **`PRO-1778-BORRAMIENTO-01` — El borramiento estadístico de la población afroargentina.** El dossier lo afirma en `10-mujeres.md` §1.3 («no es un hecho demográfico puro») sin demostrarlo. Se demuestra con censos.
4. **`VID-1818-MANSO-01` — Juana Manso.** Cruza `08-educacion.md` y `10-mujeres.md`, y hay fuentes directas abundantes.
5. **`EPI-1919-SEMANA-01` — La Semana Trágica.** Ya obligó a una corrección de cifras en tres capítulos; merece el desarrollo que la corrección dejó pendiente.
