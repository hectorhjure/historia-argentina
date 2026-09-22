1. **GO.** Construir la capa de experiencia, pero sólo esta v1 cerrada. Una segunda monografía aumenta corpus; esta v1 prueba si el corpus puede leerse, verificarse y navegarse como experiencia. Además reutiliza trabajo ya hecho: no compite con Azurduy si se prohíbe investigación nueva para lanzar.

2. **Alcance mínimo publicable**

Entra:

- Rúbrica pública de confianza y auditoría completa de las 66 fichas.
- Schema, validador y build bloqueante; linter teleológico con excepciones justificadas y versionadas.
- Línea temporal del corpus, 1516–2026: eventos con procedencia, intervalos EDTF visibles, filtro por eje y enlaces a capítulos/fichas/recorrido.
- Un único recorrido: *Quién puede quedar en la historia*.
- Siete estaciones basadas en los siete documentos ya transcriptos; sólo texto de enlace, preguntas y señalización epistémica nuevos.
- En cada estación: “sabemos / inferimos / no sabemos”, “Qué sostiene esta escena”, citas y enlace de retorno.
- URL por estación, índice, progreso, controles de teclado y uso móvil razonable.
- En fichas vinculadas: “Aparece en estos recorridos”.
- Sin facsímiles salvo licencia y procedencia verificadas; transcripción citada es suficiente.

Queda afuera explícitamente:

- Azurduy y cualquier segundo recorrido.
- Mapa, causalidad visual, densidad documental, cortes transversales.
- Búsqueda semántica, cuentas, comentarios, analítica, framework.
- Investigación de archivo nueva para esta entrega.

3. **Killer mistake**

Publicar un recorrido que haga sentir como hecho una inferencia narrativa.

Si las etiquetas “inferimos” e “incognoscible” son decorativas, la experiencia convierte lagunas del archivo y decisiones del autor en certeza afectiva. En ese caso, da igual que el esquema, la línea y los enlaces sean impecables: el proyecto traiciona su promesa historiográfica.

4. **Riesgos principales, en orden**

1. **Deriva de alcance — probabilidad alta, impacto alto.**  
   Mitigación: contrato de release versionado con exactamente una ruta, siete estaciones y cero ítems “nice to have”. Todo pedido nuevo va a `post-v1`; no hay excepción durante implementación.

2. **Conectores narrativos que exceden la evidencia — probabilidad media, impacto muy alto.**  
   Mitigación: matriz por estación, revisada antes de publicar: cada oración nueva debe clasificarse como hecho, inferencia o pregunta; cada hecho/inferencia debe apuntar a una ficha o documento. Cero celdas sin respaldo es criterio de aceptación.

3. **La línea temporal aparenta completitud nacional — probabilidad media, impacto alto.**  
   Mitigación: titularla y describirla siempre como “línea temporal del corpus”, publicar su regla de selección y hacer que cada punto tenga procedencia. Un vacío visual nunca debe leerse como “no pasó nada”.

5. **Métrica norte**

**Tasa de lectura auditable:** proporción de 12 lectores de prueba que, sin ayuda, completan una estación compartible, distinguen correctamente un hecho de una inferencia/incógnita y abren el respaldo de una afirmación central.

Umbral: **9 de 12**. Si no se alcanza tras una iteración de corrección, se mata la expansión de recorridos y se vuelve a mejorar evidencia/monografías. No requiere tracking: prueba breve, voluntaria y manual.

6. **Mi desacuerdo restante**

No acepto la tarjeta “otra lectura posible” como ritual universal. Obligatoria por diseño puede producir desacuerdo ornamental o trasladar una controversia irrelevante a una escena. La regla correcta es más exigente: un recorrido sólo publica si tiene una alternativa historiográfica real, pertinente y respaldada; si no la tiene, no se fabrica una tarjeta para cumplir plantilla. Para Valle, si el desacuerdo identificado es pertinente, entra.

7. **“Recorrido aguas abajo de monografía”**

Es una buena disciplina de producción, pero no un mecanismo suficiente. Se romperá legítimamente con recorridos transversales como “Las Marías”: no deberían exigir una monografía única, porque su pregunta compara archivos y trayectorias.

La regla durable es:

> Cada estación debe estar aguas abajo de evidencia editorial ya terminada; todo argumento de conexión entre estaciones debe tener su propio respaldo explícito.

Una monografía es una forma excelente de cumplirlo, no la única. Para un recorrido transversal, el requisito sería: fichas y evidencia completas por estación, manifiesto de selección y respaldo para cada comparación. Si falta eso, no se publica.

8. **Plan de ejecución**

| Fase | Entregable | Criterio de aceptación |
|---|---|---|
| 0. Contrato | Manifiesto v1 congelado | Una ruta, siete documentos, lista de eventos, fuera-de-alcance firmado en repo |
| 1. Integridad | Rúbrica, auditoría, validación y linter | 66/66 fichas auditadas; build limpio; todas las excepciones del linter justificadas |
| 2. Línea | Línea temporal navegable | 100% de eventos con EDTF, procedencia y destino; filtros funcionales; sin puntos sin fuente |
| 3. Recorrido | Siete dossiers de escena | URLs directas, progreso e índice; matriz de trazabilidad completa; retorno conserva estado |
| 4. Revisión | QA editorial y accesibilidad | Navegación por teclado, móvil, enlaces rotos cero, licencias verificadas o facsímiles retirados |
| 5. Prueba | 12 lecturas auditables | Métrica norte ≥ 9/12; una única iteración de corrección antes de decidir expansión |

**VEREDICTO FINAL**

- **GO:** construir una v1 pequeña y cerrada ahora.
- **Producto mínimo:** línea temporal trazable + un recorrido de siete estaciones sobre Valle.
- **No negociar:** rúbrica auditada, trazabilidad por afirmación y límites de alcance.
- **Killer mistake:** usar inmersión para disfrazar inferencia de evidencia.
- **Decisión posterior:** sólo expandir si la tasa de lectura auditable alcanza 9/12.
