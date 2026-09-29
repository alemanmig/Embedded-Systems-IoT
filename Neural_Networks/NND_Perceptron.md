# El Perceptrón: de las bases a la regla de aprendizaje

**Material de estudio**
**Referencia:** M. T. Hagan, H. B. Demuth, M. H. Beale, O. De Jesús — *Neural Network Design*, 2.ª ed., Capítulos 1 a 4.

---

## Objetivos de aprendizaje

Al terminar este material podrás:

1. Relacionar las partes de una neurona biológica con las de una neurona artificial.
2. Calcular la entrada neta y la salida de una neurona de una y de varias entradas.
3. Explicar qué hace la función de transferencia `hardlim`.
4. Interpretar geométricamente una neurona como una **frontera de decisión**.
5. Diseñar a mano un perceptrón para un problema sencillo.
6. Deducir y aplicar la **regla de aprendizaje del perceptrón**.
7. Reconocer cuándo el perceptrón puede resolver un problema y cuándo no.

---

## Índice

1. [La inspiración biológica](#1-la-inspiración-biológica)
2. [Neurona de una entrada](#2-neurona-de-una-entrada)
3. [La función de transferencia del perceptrón: hardlim](#3-la-función-de-transferencia-del-perceptrón-hardlim)
4. [Neurona de varias entradas](#4-neurona-de-varias-entradas)
5. [La idea clave: la frontera de decisión](#5-la-idea-clave-la-frontera-de-decisión)
6. [Diseño a mano: manzana / naranja](#6-diseño-a-mano-manzana--naranja)
7. [Aprendizaje supervisado](#7-aprendizaje-supervisado)
8. [Construcción de la regla de aprendizaje](#8-construcción-de-la-regla-de-aprendizaje)
9. [Aplicación a manzana / naranja](#9-aplicación-a-manzana--naranja)
10. [¿Siempre funciona?](#10-siempre-funciona)
11. [Resumen](#11-resumen)
12. [Ejercicios](#12-ejercicios)
13. [Soluciones](#13-soluciones)

---

## 1. La inspiración biológica

*Hagan, Cap. 1, "Biological Inspiration"*

Una neurona biológica tiene tres partes principales:

| Parte | Función |
|---|---|
| **Dendritas** | Reciben señales eléctricas de otras neuronas |
| **Cuerpo celular** | **Suma** las señales recibidas y, si superan un umbral, la neurona "dispara" |
| **Axón** | Lleva la señal de salida hacia otras neuronas |

El punto de contacto entre el axón de una neurona y la dendrita de otra se llama **sinapsis**. La *fuerza* de cada sinapsis determina cuánto influye una señal en la neurona que la recibe.

Según el libro, lo que define la función de una red neuronal biológica es cómo están conectadas sus neuronas y **la fuerza de cada sinapsis**. De ahí la idea central que toma la red artificial:

> **Aprender = modificar la fuerza de las conexiones.**

Todo lo que sigue es una versión matemática muy simplificada de esta idea.

### Un poco de historia

| Año | Aporte |
|---|---|
| 1943 | **McCulloch y Pitts**: primer modelo matemático de neurona (suma ponderada comparada con un umbral) |
| 1949 | **Hebb**: propone un mecanismo de aprendizaje en neuronas biológicas |
| 1958 | **Rosenblatt**: inventa el **perceptrón** y su regla de aprendizaje; primera aplicación práctica |
| 1969 | **Minsky y Papert**: demuestran las limitaciones del perceptrón; el interés en el campo cae |
| 1986 | **Rumelhart y McClelland**: popularizan la retropropagación para redes multicapa, que supera esas limitaciones |

---

## 2. Neurona de una entrada

*Hagan, Cap. 2, Fig. 2.1*

```
 p ──(w)──► Σ ──n──► f ──► a
            ▲
            │
       1 ──(b)
```

| Símbolo | Nombre | Equivalente biológico |
|---|---|---|
| `p` | Entrada | Señal que llega por la dendrita |
| `w` | Peso | Fuerza de la sinapsis |
| `b` | Bias (sesgo) | Umbral de disparo |
| `n` | Entrada neta | Lo que suma el cuerpo celular |
| `f` | Función de transferencia | La decisión de "disparar" |
| `a` | Salida | Señal en el axón |

La neurona hace dos cálculos:

```
n = w·p + b          (entrada neta)
a = f(n)             (salida)
```

### Ejemplo (Problema resuelto P2.1 del libro)

Datos: `p = 2`, `w = 2.3`, `b = −3`

```
n = (2.3)(2) + (−3) = 4.6 − 3 = 1.6
```

**¿Cuál es la salida?** Todavía no se sabe: depende de qué función `f` se elija.

### ¿Qué es el bias?

El bias es un **peso cuya entrada siempre vale 1**. Sirve para desplazar el umbral de disparo.

Sin bias, si la entrada es `p = 0`, la entrada neta siempre sería `n = 0`, sin importar el peso. El bias da a la neurona un grado de libertad extra.

> **Importante:** `w` y `b` son los **parámetros ajustables** de la neurona. La función `f` la elige el diseñador; `w` y `b` los ajusta una **regla de aprendizaje**.

---

## 3. La función de transferencia del perceptrón: `hardlim`

*Hagan, Cap. 2, Fig. 2.2 y Tabla 2.1*

El libro presenta varias funciones de transferencia. El perceptrón usa la **función escalón** (*hard limit*):

```
               ┌ 1   si n ≥ 0
hardlim(n) =   │
               └ 0   si n < 0
```

```
  a
  │
1 ┤      ┌──────────
  │      │
0 ┼──────┘
  └──────┼────────── n
         0
```

Existe también una versión **simétrica**, `hardlims`, que entrega +1 y −1:

```
               ┌ +1   si n ≥ 0
hardlims(n) =  │
               └ −1   si n < 0
```

**Continuando el ejemplo P2.1:** `a = hardlim(1.6) = 1`

### ¿Qué significa con una sola entrada?

La neurona "dispara" (`a = 1`) cuando:

```
w·p + b ≥ 0      →      p ≥ −b/w        (si w > 0)
```

Es decir, **una neurona de una entrada es un comparador contra un umbral** ubicado en `p = −b/w`:

```
  a
  │
1 ┤          ┌──────────
  │          │
0 ┼──────────┘
  └──────────┼────────── p
           −b/w
```

- El **bias** desplaza el escalón a izquierda o derecha.
- El **signo del peso** decide hacia qué lado "dispara".

Esto ya es un **clasificador de dos clases**: lo que queda a un lado del umbral es clase 1 y lo del otro lado, clase 0.

---

## 4. Neurona de varias entradas

*Hagan, Cap. 2, Fig. 2.5 y 2.6*

Con `R` entradas, cada una tiene su propio peso:

```
 p₁ ──(w₁,₁)──┐
 p₂ ──(w₁,₂)──┤
 p₃ ──(w₁,₃)──┼──► Σ ──n──► f ──► a
   ⋮          │    ▲
 p_R ─(w₁,R)──┘    │
              1 ──(b)
```

La entrada neta es (Ec. 2.3):

```
n = w₁,₁·p₁ + w₁,₂·p₂ + … + w₁,R·p_R + b
```

En **forma matricial** (Ec. 2.4 y 2.5):

```
n = W·p + b          a = f(W·p + b)
```

Donde:

```
        ┌ p₁ ┐
p =     │ p₂ │    vector columna de R × 1
        │ ⋮  │
        └ p_R┘

W = [ w₁,₁   w₁,₂   …   w₁,R ]    matriz de 1 × R (una sola neurona)
```

### Convención de índices

En `w₁,₂`:
- El **primer índice** indica la neurona **destino**.
- El **segundo índice** indica la entrada **origen**.

Aquí el primer índice siempre es 1 porque hay una sola neurona. La convención cobra sentido cuando hay varias.

### ¿Cuántas entradas y neuronas necesito?

El libro da una regla práctica (p. 2-19):

1. **Número de entradas** = número de variables del problema.
2. **Número de neuronas de salida** = número de salidas del problema.
3. **Función de transferencia de salida**: la dicta el tipo de salida que se necesita.

**Para el problema de las frutas:** hay 3 sensores (forma, textura y peso) y una sola decisión (manzana o naranja). Por lo tanto: **una neurona con tres entradas** y función `hardlim`.

---

## 5. La idea clave: la frontera de decisión

La neurona cambia de decisión justo donde `n = 0`. Esa condición define la **frontera de decisión**:

```
W·p + b = 0
```

| Número de entradas | La frontera es… |
|---|---|
| 1 | un **punto** (el umbral `−b/w`) |
| 2 | una **recta** que divide el plano |
| 3 | un **plano** que divide el espacio |
| R | un **hiperplano** |

### Ejemplo con dos entradas

`W = [1  1]`, `b = −1`

```
Frontera:  1·p₁ + 1·p₂ − 1 = 0     →     p₁ + p₂ = 1
```

```
     p₂
      │
    2 ┤  ╲
      │    ╲        a = 1
    1 ●      ╲
      │        ╲
      │  a = 0   ╲
    0 ┼──────────●──────── p₁
      0          1    2
```

**Comprobación con el punto `p = [2, 0]`:**

```
n = (1)(2) + (1)(0) − 1 = 1 ≥ 0     →     a = 1
```

El punto queda en la región `a = 1`, arriba de la recta. ✓

### Dos propiedades fundamentales

1. **El vector `W` es perpendicular a la frontera de decisión.**
2. **El vector `W` apunta hacia la región donde `a = 1`.**

```
     p₂
      │        ↗ W = [1, 1]
      │  ╲   ╱
      │    ╲╱
      │    ╱╲
      │      ╲
      └────────╲──── p₁
```

> **Esta es la base de todo el aprendizaje:**
> - Cambiar la **dirección de `W`** equivale a **girar** la frontera.
> - Cambiar **`b`** equivale a **desplazar** la frontera.

---

## 6. Diseño a mano: manzana / naranja

*Hagan, Cap. 3*

### El problema

Un distribuidor quiere separar fruta en una banda transportadora. Tres sensores miden cada fruta:

| Sensor | +1 | −1 |
|---|---|---|
| Forma | redonda | elíptica |
| Textura | lisa | rugosa |
| Peso | más de 1 libra | menos de 1 libra |

Los **prototipos** son:

```
naranja  p₁ = [1, −1, −1]      (redonda, rugosa, ligera)
manzana  p₂ = [1,  1, −1]      (redonda, lisa, ligera)
```

### El razonamiento

Compara los dos prototipos: **solo difieren en la textura** (segunda componente). Entonces basta una frontera que separe según la textura: el plano `p₂ = 0`.

Para obtener ese plano:

- `W` debe ser perpendicular al plano `p₂ = 0` → `W` apunta en la dirección del eje `p₂`.
- `W` debe apuntar hacia la manzana, que tiene `p₂ = +1`.
- El plano pasa por el origen → `b = 0`.

```
W = [0  1  0],     b = 0,     función hardlims
```

### Comprobación

```
naranja:  n = 0·(1) + 1·(−1) + 0·(−1) + 0 = −1    →   a = hardlims(−1) = −1  ✓
manzana:  n = 0·(1) + 1·(1)  + 0·(−1) + 0 = +1    →   a = hardlims(+1) = +1  ✓
```

**Una naranja "imperfecta"** (elíptica en lugar de redonda), `p = [−1, −1, −1]`:

```
n = 0·(−1) + 1·(−1) + 0·(−1) + 0 = −1    →   a = −1   (naranja) ✓
```

La red clasifica bien aunque el sensor de forma falle, porque la forma no interviene en la decisión.

### El límite del diseño a mano

Aquí se pudo diseñar a mano porque el problema es trivial: tres entradas, dos prototipos y una diferencia evidente.

Con muchas entradas, muchos ejemplos o datos que no se pueden visualizar, **diseñar a mano no es posible**. Se necesita que la red **aprenda los pesos por sí sola**.

---

## 7. Aprendizaje supervisado

*Hagan, Cap. 4*

En el aprendizaje **supervisado** se le da a la red un **conjunto de entrenamiento**: pares de entrada y salida deseada (*target*).

```
{p₁, t₁},  {p₂, t₂},  …,  {p_Q, t_Q}
```

El proceso es:

```
   ┌──────────────────────────────────────────┐
   │                                          │
   ▼                                          │
Presentar p  ──►  Calcular a  ──►  Comparar con t
                                        │
                           ¿a = t? ─── Sí ──► siguiente ejemplo
                                        │
                                        No
                                        ▼
                                Ajustar W y b ────┘
```

La pregunta es: **¿cómo se ajustan `W` y `b`?**

---

## 8. Construcción de la regla de aprendizaje

*Hagan, Cap. 4, "Constructing Learning Rules"*

Para poder dibujarlo usamos el ejemplo del libro: **dos entradas y sin bias**.

### Conjunto de entrenamiento

```
p₁ = [ 1,  2]    t₁ = 1
p₂ = [−1,  2]    t₂ = 0
p₃ = [ 0, −1]    t₃ = 0
```

```
            p₂
             │
   p₂ = ○    2    ● = p₁            ● = clase 1  (t = 1)
             │                      ○ = clase 0  (t = 0)
             1
             │
 ───────┼────0────┼─────── p₁
       −1    │    1
            −1 ○ = p₃
             │
```

**Pesos iniciales** (elegidos al azar): `W = [1.0, −0.8]`

### Paso 1 — se presenta `p₁`

```
n = (1.0)(1) + (−0.8)(2) = −0.6    →    a = hardlim(−0.6) = 0
```

Pero `t₁ = 1`. **Error.**

**Idea:** queremos que `W` apunte **más hacia `p₁`**. Una forma simple es sumarle `p₁`:

```
W = W + p₁ = [1.0, −0.8] + [1, 2] = [2.0, 1.2]
```

### Paso 2 — se presenta `p₂`

```
n = (2.0)(−1) + (1.2)(2) = 0.4    →    a = hardlim(0.4) = 1
```

Pero `t₂ = 0`. **Error.**

Ahora queremos que `W` se **aleje** de `p₂`, así que se lo **restamos**:

```
W = W − p₂ = [2.0, 1.2] − [−1, 2] = [3.0, −0.8]
```

### Paso 3 — se presenta `p₃`

```
n = (3.0)(0) + (−0.8)(−1) = 0.8    →    a = hardlim(0.8) = 1
```

Pero `t₃ = 0`. **Error.**

```
W = W − p₃ = [3.0, −0.8] − [0, −1] = [3.0, 0.2]
```

### Comprobación

| Entrada | n | a | t | |
|---|---|---|---|---|
| `p₁` | 3.0·1 + 0.2·2 = **3.4** | 1 | 1 | ✓ |
| `p₂` | 3.0·(−1) + 0.2·2 = **−2.6** | 0 | 0 | ✓ |
| `p₃` | 3.0·0 + 0.2·(−1) = **−0.2** | 0 | 0 | ✓ |

**Con tres correcciones, la red clasifica bien los tres puntos.**

### Las tres reglas

De los pasos anteriores salen tres casos:

| Caso | Acción | Efecto en `W` |
|---|---|---|
| `t = 1` y `a = 0` | `W_new = W_old + p` | Se acerca a `p` |
| `t = 0` y `a = 1` | `W_new = W_old − p` | Se aleja de `p` |
| `t = a` | `W_new = W_old` | Sin cambio |

### ¿Por qué funciona sumar `p`?

Si sumamos `p` a `W` y volvemos a presentar la **misma** entrada:

```
(W + p)·p = W·p + p·p = W·p + ‖p‖²
```

Como `‖p‖²` siempre es positivo, **la entrada neta aumenta**. Es decir, empuja la salida hacia 1, justo lo que se quería. Restar `p` hace lo contrario.

### Unificación: la regla del perceptrón

Definimos el **error**:

```
e = t − a
```

Como `t` y `a` solo valen 0 o 1, el error solo puede valer:

| t | a | e = t − a |
|---|---|---|
| 1 | 0 | **+1** |
| 0 | 1 | **−1** |
| 0 | 0 | **0** |
| 1 | 1 | **0** |

Con esto, los tres casos se escriben en **una sola regla**:

```
┌──────────────────────────────┐
│   e     = t − a              │
│   W_new = W_old + e·pᵀ       │
│   b_new = b_old + e          │
└──────────────────────────────┘
```

- `e = +1` → se suma `p`.
- `e = −1` → se resta `p`.
- `e = 0` → no hay cambio.

El **bias** se actualiza igual que un peso, porque es un peso cuya entrada siempre vale 1.

**Esta es la regla de aprendizaje del perceptrón de Rosenblatt** (Hagan, Ec. 4.34 y 4.35).

### Algoritmo completo

```
1. Inicializar W y b (valores pequeños al azar)
2. Repetir:
     errores = 0
     Para cada par {p, t} del conjunto de entrenamiento:
         a = hardlim(W·p + b)
         e = t − a
         Si e ≠ 0:
             W = W + e·pᵀ
             b = b + e
             errores = errores + 1
   hasta que errores = 0 en una pasada completa (época)
```

---

## 9. Aplicación a manzana / naranja

Ahora dejamos que la red **aprenda** en lugar de diseñarla a mano.

### Datos

- Función: `hardlim` → targets: **naranja = 0**, **manzana = 1**
- Pesos iniciales del libro: `W = [0.5, −1, −0.5]`, `b = 0.5`

```
p₁ = [1, −1, −1]  (naranja)   t₁ = 0
p₂ = [1,  1, −1]  (manzana)   t₂ = 1
```

### Cálculo detallado del paso 1

```
n = [0.5  −1  −0.5] · [1  −1  −1]ᵀ + 0.5
  = (0.5)(1) + (−1)(−1) + (−0.5)(−1) + 0.5
  = 0.5 + 1 + 0.5 + 0.5
  = 2.5

a = hardlim(2.5) = 1        pero t = 0   →   e = 0 − 1 = −1

W = [0.5  −1  −0.5] + (−1)·[1  −1  −1] = [−0.5   0   0.5]
b = 0.5 + (−1) = −0.5
```

### Traza completa

| Paso | Entrada | t | n | a | e | W nuevo | b nuevo |
|---|---|---|---|---|---|---|---|
| 1 | naranja | 0 | +2.5 | 1 | −1 | `[−0.5, 0, 0.5]` | −0.5 |
| 2 | manzana | 1 | −1.5 | 0 | +1 | `[0.5, 1, −0.5]` | +0.5 |
| 3 | naranja | 0 | +0.5 | 1 | −1 | `[−0.5, 2, 0.5]` | −0.5 |
| 4 | manzana | 1 | +0.5 | 1 | 0 | sin cambio | — |
| 5 | naranja | 0 | −3.5 | 0 | 0 | sin cambio | — |
| 6 | manzana | 1 | +0.5 | 1 | 0 | sin cambio | — |

En los pasos 5 y 6 se recorre una época completa **sin errores**: el entrenamiento termina.

### Solución aprendida

```
W = [−0.5,  2,  0.5],     b = −0.5
```

### Comparación con el diseño a mano

| | Diseño a mano (Cap. 3) | Aprendido (Cap. 4) |
|---|---|---|
| `W` | `[0, 1, 0]` | `[−0.5, 2, 0.5]` |
| `b` | `0` | `−0.5` |
| ¿Clasifica bien? | Sí | Sí |

Las dos soluciones son **distintas, pero ambas correctas**. Hay infinitas fronteras que separan los dos prototipos.

Observa algo importante: **el peso más grande (2) quedó en la textura**. La red "descubrió" por sí sola que la textura es la característica que distingue las frutas, sin que nadie se lo dijera.

---

## 10. ¿Siempre funciona?

### Sí, si el problema es linealmente separable

Un problema es **linealmente separable** si existe una recta (o un plano o un hiperplano) que deja todos los ejemplos de una clase de un lado y todos los de la otra clase del otro lado.

El **teorema de convergencia del perceptrón** (Hagan, sección 4-15) garantiza que, en ese caso, la regla encuentra una solución en un **número finito de pasos**.

### No, si el problema no es linealmente separable

El ejemplo clásico es la función **XOR**:

| p₁ | p₂ | XOR |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

```
   p₂
    │
  1 ●         ○          ● = 1
    │                    ○ = 0
    │
  0 ○─────────●── p₁
    0         1
```

**No existe ninguna recta** que separe los ● de los ○. El perceptrón nunca converge en este problema: sigue corrigiendo los pesos sin fin.

Esta es la limitación que señalaron **Minsky y Papert en 1969**, y la razón por la que después se necesitaron **redes multicapa** entrenadas con retropropagación (Hagan, Cap. 11).

### Otra observación

La regla se detiene en **la primera** solución que encuentra, no en la "mejor". La frontera puede quedar muy cerca de algún ejemplo, lo que hace a la red sensible al ruido.

---

## 11. Resumen

| Concepto | Ecuación o idea |
|---|---|
| Neurona | `a = hardlim(W·p + b)` |
| Entrada neta | `n = W·p + b` |
| Función de transferencia | `hardlim(n) = 1` si `n ≥ 0`, `0` si `n < 0` |
| Frontera de decisión | `W·p + b = 0` |
| Geometría | `W` es perpendicular a la frontera y apunta hacia `a = 1` |
| Error | `e = t − a` |
| Regla de aprendizaje | `W ← W + e·pᵀ`,   `b ← b + e` |
| Condición de éxito | Las clases deben ser **linealmente separables** |

---

## 12. Ejercicios

### Ejercicio 1 — Neurona de una entrada

En el ejemplo P2.1 (`w = 2.3`, `b = −3`):

a) ¿Qué valor de `p` hace que la neurona cambie de decisión?
b) ¿Cuál es la salida para `p = 1`? ¿Y para `p = 1.5`?

### Ejercicio 2 — Funciones de transferencia

Para la entrada neta `n = 1.6`, calcula la salida con:

a) `hardlim`
b) `hardlims`
c) La función lineal (`purelin`, `a = n`)
d) La sigmoide logística (`logsig`, `a = 1 / (1 + e⁻ⁿ)`)

### Ejercicio 3 — Frontera de decisión

Para `W = [2  −1]` y `b = 1`:

a) Escribe la ecuación de la frontera de decisión.
b) Dibújala en el plano `p₁`–`p₂`.
c) ¿En qué región queda el punto `p = [0, 0]`? ¿Y `p = [0, 2]`?
d) Dibuja el vector `W`. ¿Apunta hacia la región `a = 1`?

### Ejercicio 4 — ¿Por qué funciona la regla?

Demuestra que si `W_new = W_old + p`, entonces para esa misma entrada `p`:

```
W_new · p > W_old · p
```

(Pista: desarrolla `(W_old + p)·p`.)

### Ejercicio 5 — Entrenamiento a mano

Repite el entrenamiento del problema manzana/naranja (sección 9), pero partiendo de:

```
W = [0, 0, 0],     b = 0
```

a) Llena la tabla de la traza paso a paso.
b) ¿En cuántas épocas converge?
c) Compara la solución con la del diseño a mano de la sección 6. ¿Qué observas?

### Ejercicio 6 — Linealmente separable

Para cada una de estas funciones lógicas de dos entradas (0/1), indica si un perceptrón puede aprenderla y justifica con un dibujo:

a) AND
b) OR
c) XOR
d) NAND

### Ejercicio 7 — Pregunta de reflexión

En la sección 9, la solución aprendida tiene el peso más grande en la textura. ¿Qué pasaría con la clasificación si el sensor de textura se descompone y siempre entrega +1?

---

## 13. Soluciones

> Intenta resolver los ejercicios antes de consultar esta sección.

### Ejercicio 1

a) La neurona cambia de decisión donde `n = 0`:

```
2.3·p − 3 = 0     →     p = 3 / 2.3 ≈ 1.30
```

b)
```
p = 1:     n = 2.3 − 3 = −0.7    →   a = hardlim(−0.7) = 0
p = 1.5:   n = 3.45 − 3 = 0.45   →   a = hardlim(0.45) = 1
```

### Ejercicio 2

a) `hardlim(1.6) = 1`
b) `hardlims(1.6) = +1`
c) `purelin(1.6) = 1.6`
d) `logsig(1.6) = 1 / (1 + e⁻¹·⁶) ≈ 0.832`

(Los resultados a, c y d coinciden con el problema resuelto P2.2 del libro.)

### Ejercicio 3

a) `2·p₁ − p₂ + 1 = 0`   →   `p₂ = 2·p₁ + 1`

b) Es una recta con pendiente 2 que corta el eje `p₂` en 1 y el eje `p₁` en −0.5.

c)
```
p = [0, 0]:   n = 0 − 0 + 1 = 1    →   a = 1
p = [0, 2]:   n = 0 − 2 + 1 = −1   →   a = 0
```

d) `W = [2, −1]` apunta hacia abajo y a la derecha, es decir, hacia la región que contiene al origen, donde `a = 1`. ✓

### Ejercicio 4

```
W_new · p = (W_old + p) · p = W_old · p + p · p = W_old · p + ‖p‖²
```

Como `‖p‖² > 0` para cualquier `p ≠ 0`:

```
W_new · p > W_old · p     ∎
```

La entrada neta para esa entrada aumenta, lo que empuja la salida hacia 1.

### Ejercicio 5

a)

| Paso | Entrada | t | n | a | e | W nuevo | b nuevo |
|---|---|---|---|---|---|---|---|
| 1 | naranja | 0 | 0 | 1 | −1 | `[−1, 1, 1]` | −1 |
| 2 | manzana | 1 | −2 | 0 | +1 | `[0, 2, 0]` | 0 |
| 3 | naranja | 0 | −2 | 0 | 0 | sin cambio | — |
| 4 | manzana | 1 | +2 | 1 | 0 | sin cambio | — |

Observa el paso 1: `n = 0`, y como `hardlim(0) = 1`, la red se equivoca aunque todos los pesos sean cero.

b) Converge en **2 épocas**. La segunda pasa sin errores.

c) La solución es `W = [0, 2, 0]`, `b = 0`: **exactamente el doble** del diseño a mano `W = [0, 1, 0]`, `b = 0`. Multiplicar `W` y `b` por una constante positiva no cambia la frontera (`2·(W·p + b) = 0` es el mismo plano que `W·p + b = 0`). Desde pesos en cero, **la red aprendió la misma frontera que diseñamos a mano**.

### Ejercicio 6

| Función | ¿Linealmente separable? | ¿Puede aprenderla el perceptrón? |
|---|---|---|
| AND | Sí: solo `(1,1)` es 1; una recta lo separa | Sí |
| OR | Sí: solo `(0,0)` es 0; una recta lo separa | Sí |
| XOR | **No**: las clases están en esquinas opuestas | **No** |
| NAND | Sí: es AND con la salida invertida | Sí |

### Ejercicio 7

Con el sensor de textura fijo en +1, **toda fruta se clasificaría como manzana**. La textura aporta `+2` a la entrada neta y domina a los otros términos.

Por ejemplo, una naranja real `[1, −1, −1]` con el sensor dañado se leería como `[1, 1, −1]`:

```
n = (−0.5)(1) + (2)(1) + (0.5)(−1) − 0.5 = 0.5    →   a = 1   (¡manzana!)
```

La red depende casi por completo de una sola característica. Esto muestra un límite práctico: si la característica que la red considera más importante falla, la clasificación falla. En sistemas reales conviene tener características redundantes y verificar los sensores.

---

## Para seguir

- **Implementación:** `perceptron_hagan.py` reproduce en Python la traza de la sección 9 y evalúa las 8 entradas posibles.
- **Siguiente tema en el libro:** Cap. 4, perceptrón de varias neuronas (problemas P4.3 y P4.5), para clasificar más de dos clases.
