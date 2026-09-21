# Regímenes estadísticos argentinos — cómo usar las cifras sin mentir

> **Qué es este capítulo y por qué reemplaza a otra cosa.** El plan original preveía construir series históricas largas en CSV (población, PIB, inflación, salario real, pobreza, desempleo, alfabetización, mortalidad infantil) desde 1810 hasta hoy. **Eso se descartó.** Una serie continua de PIB o de pobreza argentina es un artefacto falso: mezcla universos, canastas, coberturas geográficas y definiciones incompatibles. Lo que sigue es lo que hay que hacer en su lugar.

**Regla única:** *una serie por régimen estadístico, nunca una línea continua inventada.* Toda cifra que se cite debe declarar **período, universo y fuente**. Si no se pueden declarar, la cifra no se usa.

---

## 1. La tabla de trampas

| Variable | Dónde está el dato | Qué rompe la comparación larga |
|---|---|---|
| **Población** | [INDEC, información de archivo](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7); armonizaciones de [CELADE/CEPAL](https://statistics.cepal.org/portal/databank/) | Censo ≠ estimación intercensal. Cambios de límites territoriales, omisión censal, y proyecciones que se revisan **retroactivamente** después de cada censo. No mezclar población censada con proyectada |
| **PIB** | [INDEC, Cuentas Nacionales](https://sitioanterior.indec.gob.ar/nivel3_default.asp?id_tema_1=3&id_tema_2=9); [documentación del empalme](https://biblioteca.indec.gob.ar/bases/minde/pbi_80-05_Metodologia.pdf); [CEPALSTAT](https://statistics.cepal.org/portal/databank/) para comparación internacional | Bases **1935, 1950, 1960, 1970, 1986, 1993 y 2004**. El empalme por tasas conserva las variaciones pero **no** los niveles ni la composición sectorial. Antes de las cuentas nacionales, **Ferreres es una reconstrucción privada, no un dato primario** |
| **Inflación** | [INDEC, archivo de IPC](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7); [BCRA, series descargables](https://www.bcra.gob.ar/consultas-personalizadas-de-series-estadisticas/) | IPC GBA ≠ IPC nacional. Cambios de canasta y de base. **El propio INDEC informa reservas expresas sobre la serie enero 2007 – diciembre 2015**: no usarla como deflactor |
| **Salario real** | [INDEC, Índice de Salarios](https://sitioanterior.indec.gob.ar/nivel4_default.asp?id_tema_1=3&id_tema_2=38&id_tema_3=111) | Registrado desde nov. 2015, no registrado desde oct. 2016. Cambian ocupación, sector, jornada, cobertura, canasta deflactora y región. **No existe un "salario real argentino" homogéneo de dos siglos** |
| **Desempleo** | [INDEC, EPH](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7); [metodología EPH continua](https://www.indec.gob.ar/ftp/cuadros/sociedad/Metodologia_EPHContinua.pdf) | **EPH puntual (1974-2003) vs. EPH continua (desde 2003)**: cambian cuestionario, frecuencia, muestra y captación del empleo. Cobertura de **28 a 31 aglomerados en 2006**. Y es población de **aglomerados urbanos**, no "Argentina" |
| **Pobreza** | [INDEC, metodología y archivo](https://sitioanterior.indec.gob.ar/nivel4_default.asp?id_tema_1=4&id_tema_2=27&id_tema_3=64); [serie comparable de CEDLAS-UNLP](https://www.cedlas.econo.unlp.edu.ar/) | Incidencia **por ingresos en aglomerados EPH**: no es nacional ni rural. Rupturas: EPH continua (2003), ampliación (2006), **no publicada en 2014-2015**, reanudada en 2016 |
| **Alfabetización** | Tablas originales de cada [censo](https://www.indec.gob.ar/indec/web/Institucional-Indec-InformacionDeArchivo-7) | 1869 mide "mayores de 6"; 2010, "mayores de 10". Cambian umbral, pregunta y tratamiento de la no respuesta. Ya señalado en `08-educacion.md` §2.4 |
| **Mortalidad infantil** | [DEIS](https://www.argentina.gob.ar/salud/deis) y anuarios | Cobertura y calidad del registro varían por época y por provincia. Formularios vigentes desde 2001 = otra ruptura. Y una caída simultánea a una política no prueba que esa política la causó |

---

## 2. Cifras del dossier que esta tabla pone en cuestión

Auditoría de lo que el propio dossier afirma. **Estas correcciones ya están aplicadas en los capítulos correspondientes.**

| Cifra afirmada | Problema | Cómo queda |
|---|---|---|
| "Desempleo de ~6% (1991) a **18,4% (1995)**" | El pico de 1995 es de **EPH puntual, onda mayo, aglomerados urbanos**. No es comparable con mediciones posteriores a 2003 ni con cobertura de 31 aglomerados | Se conserva con universo declarado, y se prohíbe encadenarla con cifras post-2003 |
| "Pobreza **>50%** en 2002" | Depende del punto de medición y del conjunto de aglomerados. Las mediciones de 2002 dan del orden de **54% a 57,5%** según onda y cobertura | Se cita como rango con fuente y onda, no como número único |
| Serie reciente de pobreza | **Verificada (INDEC-EPH, 31 aglomerados):** 41,7% (2S 2023) · 52,9% (1S 2024) · 38,1% (2S 2024) · 31,6% (1S 2025) · **28,2% (2S 2025)**, el valor más bajo desde principios de 2018 | Se conserva con universo declarado. **No encadenar con 2002** sin señalar las rupturas de 2003, 2006 y 2014-2015 |
| "PIB **+~6% anual** 2003-2011" | Correcto para esa ventana, pero **el promedio 2000-2015 es ~2,7%** (Banco Mundial). La ventana elegida cambia el resultado por completo | Se declara la ventana y se aclara que elegirla es una decisión interpretativa |
| "PIB estancado (**+0,3% anual**) 2012-2015" y "per cápita **-7,1%**" | Provienen de fuente secundaria no verificada contra INDEC | Marcadas como **no verificadas** |
| "Inflación **~211%** en 2023" | **Verificada**: 211,4% según INDEC | Se conserva con fuente |
| Coyuntura 2024-2026 | Prensa | Marcada como periodística. Dato adicional verificado: la inflación anual cae a **117,8% en 2024** y a **84,5%** en la medición interanual de enero de 2025 |

---

## 3. Cómo citar una cifra en este dossier

Formato mínimo obligatorio:

> **Valor · período · universo · fuente.**
> *Ejemplo correcto:* "Desempleo 18,4% — onda mayo de 1995, aglomerados urbanos EPH puntual, INDEC."
> *Ejemplo incorrecto:* "El desempleo llegó al 18,4% en los 90."

Y tres prohibiciones:

1. **No encadenar** cifras de EPH puntual con EPH continua sin decirlo.
2. **No usar el IPC 2007-2015** como deflactor ni como dato de inflación sin la reserva del INDEC. Para 2010, el IPC-GBA oficial dio **10,9%** dic/dic mientras el IPC de siete provincias estimaba **~25,8%**: citar el primero sin el segundo y sin la reserva es desinformar.
2 bis. **No convertir la incidencia de pobreza de EPH en número absoluto de personas para todo el país.** La EPH cubre 31 aglomerados urbanos (~29 millones de habitantes), no los ~46 millones del país. El 28,2% del 2º semestre de 2025 equivale a ~8,5 millones de personas **en ese universo**; proyectarlo al total nacional produce cifras infladas que circulan en prensa.
3. **No graficar** pobreza 2001, 2006, 2013 y 2016 como una serie: faltan 2014-2015 y cambian canasta, precios y cobertura.

---

## 4. Lo que este capítulo **no** hace

No construye las series. Construye las **reglas** para usarlas y señala dónde están. Producir series efectivamente comparables —con empalmes documentados y denominadores recalculados— es trabajo de economista con acceso a las bases, no de síntesis histórica.

**Si alguna vez se hace ese trabajo**, el criterio de aceptación es: cada punto de la serie debe poder responder las cuatro preguntas del §3. Si un punto no puede, se omite el punto, no se interpola.
