1. Elegiría **(c) bibliografía post-1991**, no páginas ni series.

Es el mayor retorno porque corrige simultáneamente tres fallas: las explicaciones causales heredadas, los sujetos/objetos que esa historiografía no veía y el tramo 1990-2026. Poner página a Cortés Conde o Torre y de Riz mejora la auditabilidad de lo ya dicho, pero vuelve localizable una interpretación que puede estar superada. Las series primarias controlan números, pero no resuelven inferencias como “la restricción externa es la variable maestra” o “1952-55 fue una corrección”. Para un Proyecto de ChatGPT, el daño dominante no es que el modelo no pueda hallar una página: es que responderá con seguridad causal usando un mapa disciplinar viejo.

Trade-off: se pierde precisión inmediata de cada cifra. Pero es preferible una síntesis que diga “dato pendiente de verificación” antes que una que presente como consenso actual una explicación de 1991.

2. No hay una convención única y universal para “esto decía la bibliografía disponible / esto sostiene hoy la disciplina”. Lo más cercano es el aparato de una **edición crítica anotada**: texto base preservado, con notas editoriales que distinguen fuente, alcance y actualización. No alcanza una advertencia general en `12-fuentes`: el modelo no garantiza recuperarla junto con cada afirmación.

Propongo una marca por afirmación relevante:

> **Base del corpus (fecha):** Torre y de Riz (1991) sostienen X.  
> **Actualización editorial (fecha y fuente):** la bibliografía posterior Y/Z mantiene, limita o disputa X.  
> **Estado:** vigente / revisado / debatido / no verificado.  
> **Alcance:** qué no permite concluir.

No debe reescribir la prosa ni fingir que Cambridge dijo lo que no dijo. Es trazabilidad: conserva la genealogía de la afirmación y evita que una actualización silenciosa se haga pasar por fuente original.

3. **Series: no existe una fuente argentina única, oficial y homogénea para 1810-2026.** La regla debe ser “una serie por régimen estadístico”, con metadatos de cobertura, definición, base, universo y ruptura; nunca una línea continua inventada.

| Variable | Fuente reproducible recomendada | Trampas de comparación |
|---|---|---|
| Población | [INDEC, censos y archivo](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7); para armonizaciones intercensales, [CELADE/CEPAL](https://statistics.cepal.org/portal/databank/index.html?area_id=240&indicator_id=2194&lang=es) | Censo no equivale a estimación intercensal; cambios territoriales, omisión y proyecciones revisadas tras cada censo. No usar población censada y proyectada como si fueran la misma medición. |
| PIB | [INDEC, Cuentas Nacionales](https://sitioanterior.indec.gob.ar/nivel3_default.asp?id_tema_1=3&id_tema_2=9); [documentación del empalme](https://biblioteca.indec.gob.ar/bases/minde/pbi_80-05_Metodologia.pdf); para comparación internacional, [CEPALSTAT](https://statistics.cepal.org/portal/databank/index.html?area_id=240&indicator_id=2194&lang=es) | Bases 1935, 1950, 1960, 1970, 1986, 1993 y 2004; cobertura, precios relativos y métodos cambian. El empalme por tasas conserva variaciones, no hace idénticos los niveles ni la composición sectorial. Antes de las cuentas nacionales, Ferreres es reconstrucción privada, no “dato primario”. |
| Inflación | [INDEC, archivo de IPC](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7); [BCRA, series descargables](https://www.bcra.gob.ar/consultas-personalizadas-de-series-estadisticas/) | IPC GBA no es IPC nacional; cambios de canasta/base exigen empalme documentado. INDEC informa reservas expresas para series enero de 2007-diciembre de 2015 salvo revisión explícita. No usar IPC oficial intervenido como deflactor “limpio”. |
| Salario real | Nominal: [INDEC Índice de Salarios](https://sitioanterior.indec.gob.ar/nivel4_default.asp?id_tema_1=3&id_tema_2=38&id_tema_3=111); largo plazo: reconstrucciones académicas, por ejemplo [Williamson/CEPAL](https://cdi.mecon.gob.ar/bases/doc/cepal/perspec/33.pdf) | INDEC publica registrado desde noviembre de 2015 y no registrado desde octubre de 2016; no hay “salario real argentino” homogéneo de dos siglos. Cambian ocupación, sector, jornada, cobertura, canasta deflactora y región. |
| Desempleo | [INDEC, EPH histórica](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7) y [metodología 2003](https://www.indec.gob.ar/ftp/cuadros/sociedad/Metodologia_EPHContinua.pdf) | EPH puntual 1974-2003 versus continua desde 2003: cuestionario, frecuencia, muestra y captación del empleo cambiaron. Es población de aglomerados urbanos, no “Argentina”; además cambia cobertura de 28 a 31 aglomerados en 2006. |
| Pobreza | [INDEC, metodología y archivo](https://sitioanterior.indec.gob.ar/nivel4_default.asp?id_tema_1=4&id_tema_2=27&id_tema_3=64) | Es incidencia por ingresos en aglomerados EPH, no nacional ni rural. Rupturas: EPH continua en 2003; ampliación 2006; no publicar 2014-2015; reanudación en 2016. Nunca graficar 2001, 2006, 2013 y 2016 como serie plenamente comparable sin nota de canasta, precios e ingresos. |
| Alfabetización | Tablas originales de cada [censo INDEC](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7) | El propio dossier reconoce el problema: 1869 “mayores de 6” y 2010 “mayores de 10”. Cambian umbral, pregunta, tratamiento de no respuesta y universo. Sólo comparar tras recalcular denominadores equivalentes. |
| Mortalidad infantil | [DEIS](https://www.argentina.gob.ar/salud/deis) y sus [publicaciones/anuarios](https://www.argentina.gob.ar/node/231499) | Numerador y nacidos vivos registrados: cobertura y calidad del registro varían históricamente y por provincia. Formularios vigentes desde 2001 introducen otra ruptura documental. La tasa es útil, pero no prueba por sí sola que una política puntual causó un descenso. |

4. Otros casos donde el texto **tiene evidencia más disruptiva que su conclusión**:

- `04-economia` §2.4 registra que en 1914 la producción local cubría 91% de alimentos, 88% de textiles y 33% de metalurgia, pero concluye sólo “no era un país sin industria”. La conclusión más fuerte es que la industrialización argentina no comienza en 1930 ni con el peronismo: la ISI reconfigura una industrialización previa. Su periodización posterior la minimiza.

- `05-cultura` §2.2 muestra que 51,4% de las mutuales porteñas eran multinacionales y que anarquistas/sindicalistas sostuvieron instituciones cooperativas. Sin embargo, el esquema central sigue siendo élites/Estado/inmigración. Esa evidencia permite una conclusión más fuerte: la integración no fue sólo política estatal; hubo infraestructura asociativa autogestionada y transétnica.

- `07-intereses-cruzados` §2 documenta que Justo aceptó la Corporación de Transportes pero no obligó el ingreso de colectiveros ni autorizó tarifas; Rock concluye que venció a los ingleses. Eso es más que un “matiz contra la caricatura”: invalida el mecanismo general “presión externa → decisión estatal”. Hace falta distinguir presión, concesión formal, implementación y resultado.

5. Hay contaminación efectiva, aunque no siempre atribuible sólo a esos autores.

- En `06-personajes` §Sarmiento se afirma que la crítica de Jauretche es “**la más aguda**” y “el debate cultural argentino por excelencia”. Ya no es Jauretche como objeto; es una jerarquización del dossier sin evidencia comparativa ni historiografía que la sostenga.

- En `05-cultura` §2.1, desde la zoncera “Dice *La Nación*… dice *La Prensa*” se desliza a “el poder de la prensa comercial para fijar el sentido común”. Gallo respalda relevancia de la prensa; no prueba la teoría jauretcheana de captura del sentido común.

- `10-mujeres` §1.1 usa a Pigna para afirmar que el mestizaje, “en su forma dominante”, fue apropiación sexual. La nota posterior advierte correctamente que es divulgación, pero la tesis queda en voz del dossier sin volver a cronistas ni a la historiografía nombrada. La advertencia no neutraliza una afirmación ya formulada como hecho.

Rosa está mejor contenido: la tesis del complot británico aparece explícitamente como tesis revisionista y es discutida.

6. Claude diagnostica correctamente un problema, pero lo nombra mal. No falta una **teoría única del cambio**; imponerla sería peor en una síntesis. Falta una **gramática causal explícita**. Pluralismo explicativo es correcto si cada pasaje indica mecanismo, escala y evidencia: “shock externo”, “regla institucional”, “coalición social”, “decisión contingente” o combinación, y evita saltar de correlación a causa. Hoy `03-revoluciones` puede pasar de caída de ingresos estatales a desbande político y golpe como si fuera una demostración cerrada. El defecto no es eclecticismo; es que el lector —y ChatGPT— no ve dónde termina el dato y empieza la inferencia.

**VEREDICTO RONDA 2**

- Intervención prioritaria única: **bibliografía post-1991 anotando cada tesis heredada con un aparato de actualización editorial**.
- Mayor discrepancia con Claude: no hace falta una teoría del cambio unificadora; hace falta declarar mecanismos causales y su grado de prueba.
