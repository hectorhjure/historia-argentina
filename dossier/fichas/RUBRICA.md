# Rúbrica de confianza y estado

> **Por qué existe este archivo.** Durante 66 fichas, el campo `confianza: alta|media|baja` se asignó sin criterio publicado. En un debate adversarial se lo describió, con razón, como *«impresión editorial disfrazada de metadato»*. Una auditoría lo confirmó: entre `alta` y `baja` había una diferencia media de 0,5 fuentes y 0,5 lecturas directas. El gradiente era ruido.
>
> Esta rúbrica define los tres campos con criterios **falsables**, para que cualquiera pueda discutir una asignación concreta señalando qué criterio no se cumple.

---

## Los tres campos son ejes independientes

Es el error conceptual que esta rúbrica corrige primero. No son grados de una misma escala.

| Campo | Pregunta que responde | No responde |
|---|---|---|
| **`tipo`** | ¿Qué clase de afirmación es? | Si es cierta |
| **`estado`** | ¿En qué situación editorial está la ficha? | Cuán fuerte es la prueba |
| **`confianza`** | ¿Cuán fuerte es el respaldo documental? | Si hay consenso |

**Consecuencia que hay que entender antes de leer una ficha:** una afirmación puede ser `tipo: debatido` y `confianza: alta` sin contradicción. Que Perón haya convocado o no al 17 de octubre está historiográficamente disputado; que la movilización ocurrió el 17 de octubre de 1945 está documentado. **La confianza mide el respaldo, no el acuerdo.**

---

## 1 · `confianza` — fuerza del respaldo

### `alta` — requiere **todas** estas condiciones

1. La afirmación se apoya en **al menos una fuente leída en directo**, o en una **fuente primaria institucional** (texto de ley, serie del INDEC o BCRA, documento de archivo, sentencia judicial, censo).
2. Esa fuente es **investigación académica, documento primario o estadística oficial** — no divulgación ni ensayo interpretativo.
3. **No se conoce fuente de calidad comparable que la contradiga.** Si existe, la ficha es `media` y el desacuerdo va declarado.
4. Si involucra cifras: **período, universo y fuente están declarados** (regla de `14-regimenes-estadisticos.md`).

### `media` — **cualquiera** de estas

1. Se apoya en **una sola fuente académica** leída en directo, sin contraste con otra.
2. La fuente principal se conoce **por reseñas o referencia secundaria** y no en directo.
3. Se apoya en **divulgación con buen uso de fuentes**, no verificada contra primarias.
4. Involucra cifras con universo declarado pero **no verificadas contra la base institucional**.
5. Hay una fuente de calidad comparable que la contradice, y el desacuerdo está declarado.

### `baja` — **cualquiera** de estas

1. La fuente principal es **ensayo o divulgación sin aparato verificable**.
2. **Ninguna fuente fue leída en directo** y ninguna es institucional.
3. Es una **autoevaluación del corpus** sobre sí mismo, no verificada externamente.
4. Involucra cifras **sin universo declarado**, o provenientes de prensa.

### Caso especial: `tipo: metodológica`

Para afirmaciones **sobre el corpus mismo**, el corpus es la fuente primaria, de modo que el criterio 1 de `alta` se satisface por definición: nadie tiene mejor acceso a los límites del dossier que el dossier.

**Esto obliga a una distinción que se había perdido.** La confianza de una afirmación metodológica califica **la meta-afirmación, no el contenido que describe**. «El tramo 1990-2026 es el peor fundado del corpus» es una afirmación de **confianza alta**: se sabe con certeza. Que el tramo *descrito* sea flojo es justamente lo que la afirmación afirma. Marcarla `baja` mezcla los dos niveles y esconde la advertencia del lector que filtra por confianza — que es exactamente el lector que más necesita verla.

Excepción: cuando la afirmación metodológica **ordena o compara el campo** en vez de describir el corpus (por ejemplo, «esta es la ausencia más grave»), es una interpretación y se evalúa con los criterios generales.

### Valores compuestos

Se permiten cuando una ficha tiene respaldo desigual según la dimensión, en la forma:

```yaml
confianza: alta sobre el aparato documental · baja sobre la biografía
```

**Regla de filtrado: gobierna el valor más bajo.** Una ficha compuesta se comporta como `baja` en cualquier filtro o consulta automática. Si eso resulta demasiado severo, la ficha hay que partirla en dos, no ablandar la regla.

---

## 2 · `estado` — situación editorial de la ficha

| Valor | Criterio |
|---|---|
| **`actualizado`** | Revisada contra sus fuentes en la última pasada de corrección del corpus, y su `actualizado_hasta` corresponde |
| **`provisional`** | Escrita pero **no verificada**, o pendiente de una fuente que se identificó y no se consiguió. Lleva el límite declarado en el cuerpo |

`debatido` **ya no es un valor de `estado`.** Es una propiedad de la afirmación, no de la ficha, y por lo tanto vive en `tipo`. Mezclarlos producía la incoherencia de que una ficha revisada y al día apareciera como si estuviera sin terminar.

---

## 3 · `tipo` — clase de afirmación

| Valor | Qué es |
|---|---|
| **`hecho`** | Ocurrió, con fecha y evidencia |
| **`interpretación`** | Lectura de un hecho o de un conjunto. Atribuible a un autor identificado |
| **`debatido`** | La historiografía sostiene posiciones incompatibles. **Obliga a presentar el debate, no una posición** |
| **`corrección`** | Corrige algo que el propio corpus afirmaba antes, o que circula como verdad establecida |
| **`metodológica`** | Afirmación sobre el corpus mismo: sus límites, sesgos o reglas |

---

## 4 · Cómo discutir una asignación

Señalá **el criterio numerado que no se cumple**. Por ejemplo: *«`ECO-1880-CRECIMIENTO-01` está en `alta` pero incumple el criterio 3: Cortés Conde y Gerchunoff difieren en la tasa»*. Eso es una objeción verificable y se resuelve mirando las fuentes.

Lo que esta rúbrica hace imposible es discutir «me parece que esa confianza está alta». Ese era el problema.

## 5 · Validación automática

`sitio/qa.py` verifica en cada publicación que:

- todo valor de `confianza`, `estado` y `tipo` pertenezca al vocabulario de esta rúbrica;
- ninguna ficha declare `confianza: alta` **sin fuente leída en directo ni fuente institucional** (criterio 1 de `alta`);
- ninguna ficha `tipo: debatido` presente una sola posición;
- ninguna ficha con cifras omita período, universo o fuente.

**Falla el despliegue.** Una rúbrica que no se verifica vuelve a ser impresión editorial en un plazo corto.
