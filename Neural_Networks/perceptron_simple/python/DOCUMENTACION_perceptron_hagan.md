# Documentación detallada de `perceptron_hagan.py`

Este documento describe, sección por sección y función por función, el programa `perceptron_hagan.py`: qué hace cada parte, la teoría del libro en la que se basa y por qué está escrita así.

**Referencia:** M. T. Hagan, H. B. Demuth, M. H. Beale — *Neural Network Design*, Capítulos 3 y 4.

---

## Índice

1. [Visión general](#1-visión-general)
2. [Dependencias e importaciones](#2-dependencias-e-importaciones)
3. [Funciones de transferencia](#3-funciones-de-transferencia)
4. [Datos del problema](#4-datos-del-problema)
5. [Perceptrón diseñado gráficamente (Cap. 3)](#5-perceptrón-diseñado-gráficamente-cap-3)
6. [Regla de aprendizaje del perceptrón (Cap. 4)](#6-regla-de-aprendizaje-del-perceptrón-cap-4)
7. [Evaluación exhaustiva](#7-evaluación-exhaustiva)
8. [Vista previa embebida: inferencia con enteros](#8-vista-previa-embebida-inferencia-con-enteros)
9. [Programa principal](#9-programa-principal)
10. [Traza completa del entrenamiento](#10-traza-completa-del-entrenamiento)
11. [Interpretación geométrica](#11-interpretación-geométrica)
12. [Ejercicios sugeridos](#12-ejercicios-sugeridos)

---

## 1. Visión general

El programa resuelve el problema de clasificación manzana/naranja del libro de Hagan con un **perceptrón de una sola neurona y tres entradas**.

```
          p[0] forma   ──┐
          p[1] textura ──┼──►  n = W·p + b  ──►  a = hardlim(n)  ──►  0 = naranja
          p[2] peso    ──┘                                             1 = manzana
```

El programa tiene cinco bloques lógicos:

| Bloque | Función(es) | Propósito |
|---|---|---|
| Transferencia | `hardlim`, `hardlims` | Funciones de activación escalón |
| Cap. 3 | `perceptron_chapter3` | Perceptrón con pesos elegidos a mano |
| Cap. 4 | `train_perceptron` | Aprendizaje automático de pesos y bias |
| Evaluación | `nearest_prototype`, `evaluate_all` | Probar las 8 entradas posibles |
| Embebido | `to_fixed_point`, `infer_int`, `check_fixed_point` | Demostrar que basta aritmética entera |

---

## 2. Dependencias e importaciones

```python
import itertools
import numpy as np
```

- **`itertools`** (biblioteca estándar): se usa `itertools.product([-1, 1], repeat=3)` para generar las 2³ = 8 combinaciones posibles de sensores.
- **`numpy`**: vectores, productos matriz-vector (`@`) y la función vectorizada `np.where`.

---

## 3. Funciones de transferencia

### 3.1 `hardlim(n)`

```python
def hardlim(n):
    return np.where(n >= 0, 1, 0)
```

Es la función escalón de la Tabla 2.1 del libro:

```
            ┌ 1   si n ≥ 0
hardlim(n) =│
            └ 0   si n < 0
```

- `np.where(condición, valor_si_verdadero, valor_si_falso)` funciona igual con escalares y con arreglos.
- **Detalle importante:** el caso `n = 0` da **1**. El libro usa esta convención, y define de qué lado de la frontera de decisión cae un punto que está justo sobre ella (ver el Problema P4.4 del libro).

### 3.2 `hardlims(n)`

```python
def hardlims(n):
    return np.where(n >= 0, 1, -1)
```

Es la versión **simétrica**:

```
             ┌ +1  si n ≥ 0
hardlims(n) =│
             └ −1  si n < 0
```

El Capítulo 3 la usa con salidas −1 (naranja) y +1 (manzana). El Capítulo 4 cambia a `hardlim` con salidas 0/1. Las dos son equivalentes en capacidad (Ejercicio E4.10): `hardlims(n) = 2·hardlim(n) − 1`.

---

## 4. Datos del problema

```python
P_ORANGE = np.array([1, -1, -1])
P_APPLE  = np.array([1,  1, -1])

TRAINING_SET = [(P_ORANGE, 0), (P_APPLE, 1)]

NAMES_HARDLIM  = {0: "naranja", 1: "manzana"}
NAMES_HARDLIMS = {-1: "naranja", 1: "manzana"}
```

### Codificación de los sensores

| Índice | Sensor | +1 | −1 |
|---|---|---|---|
| `p[0]` | Forma | redonda | elíptica |
| `p[1]` | Textura | lisa | rugosa |
| `p[2]` | Peso | > 1 libra | < 1 libra |

### Prototipos

- **Naranja** `[1, −1, −1]`: redonda, rugosa, ligera.
- **Manzana** `[1, 1, −1]`: redonda, lisa, ligera.

Los dos prototipos **solo difieren en la textura** (`p[1]`). Esto explica por qué el diseño del Capítulo 3 usa únicamente esa entrada.

### Conjunto de entrenamiento

`TRAINING_SET` es una lista de pares `(entrada, target)`, la notación `{p_q, t_q}` de la Ec. 4.20. Los targets son 0/1 porque el Capítulo 4 usa `hardlim`.

Los diccionarios `NAMES_*` solo traducen la salida numérica a texto para imprimirla.

---

## 5. Perceptrón diseñado gráficamente (Cap. 3)

```python
def perceptron_chapter3():
    W = np.array([[0, 1, 0]])
    b = np.array([0])
    ...
    for label, p in tests.items():
        n = (W @ p + b).item()
        a = hardlims(n).item()
```

### Teoría

En el Capítulo 3 los pesos **no se aprenden, se diseñan**. El razonamiento del libro es:

1. Como los prototipos solo difieren en `p[1]`, el plano `p[1] = 0` los separa perfectamente.
2. La frontera de decisión cumple `W·p + b = 0`. Para obtener el plano `p[1] = 0` se elige `W = [0 1 0]` y `b = 0`.
3. `W` es ortogonal a la frontera y apunta hacia la manzana, así que la manzana da salida +1.

### Código

- `W` tiene forma `(1, 3)`: una fila por neurona, una columna por entrada (notación S×R del libro, con S = 1 y R = 3).
- `W @ p` es el producto matriz-vector y da un arreglo de un elemento. `.item()` lo convierte en un escalar de Python para imprimirlo.

### Casos de prueba

| Caso | `p` | `n` | `a` | Clase |
|---|---|---|---|---|
| Naranja prototipo | `[1, −1, −1]` | −1 | −1 | naranja |
| Manzana prototipo | `[1, 1, −1]` | +1 | +1 | manzana |
| Naranja elíptica (Ec. 3.13) | `[−1, −1, −1]` | −1 | −1 | naranja |

El tercer caso es el ejemplo del libro de una "naranja imperfecta": el sensor de forma falla, pero la clasificación sigue siendo correcta porque el perceptrón ignora la forma.

---

## 6. Regla de aprendizaje del perceptrón (Cap. 4)

```python
def train_perceptron(training_set, W0, b0, max_epochs=100, verbose=True):
```

Es el núcleo del programa. Implementa la regla de Rosenblatt en su forma unificada (Ecs. 4.34–4.35 y 4.38–4.39):

```
e     = t − a
W_new = W_old + e · pᵀ
b_new = b_old + e
```

### Parámetros

| Parámetro | Tipo | Descripción |
|---|---|---|
| `training_set` | lista de `(p, t)` | Pares entrada/target |
| `W0` | lista o arreglo de 3 elementos | Pesos iniciales |
| `b0` | escalar | Bias inicial |
| `max_epochs` | int | Límite de seguridad por si el problema no es separable |
| `verbose` | bool | Si es `True`, imprime cada paso |

### Valor de retorno

La tupla `(W, b, epoch)`: los pesos finales, el bias final y el número de épocas hasta converger.

### Paso a paso

**Inicialización**

```python
W = np.array(W0, dtype=float).reshape(1, -1)
b = np.array(b0, dtype=float).reshape(1)
```

Se convierten a `float` porque los pesos iniciales del libro son fraccionarios (0.5). `reshape(1, -1)` da a `W` la forma `(1, 3)`.

**Bucle de épocas**

```python
for epoch in range(1, max_epochs + 1):
    errors = 0
    for p, t in training_set:
```

Una **época** es una pasada completa por todo el conjunto de entrenamiento. El entrenamiento es **en línea** (*online*): los pesos se actualizan después de cada muestra, no al final de la época. Así lo hace el libro.

**Propagación hacia adelante**

```python
n = (W @ p + b).item()
a = hardlim(n).item()
```

Calcula la entrada neta `n` y la salida `a`.

**Error y actualización**

```python
e = t - a
if e != 0:
    errors += 1
    W = W + e * p.reshape(1, -1)
    b = b + e
```

El error solo puede tomar tres valores:

| `t` | `a` | `e` | Acción | Efecto geométrico |
|---|---|---|---|---|
| 1 | 0 | +1 | `W += p` | `W` gira **hacia** `p` |
| 0 | 1 | −1 | `W −= p` | `W` gira **alejándose** de `p` |
| t = a | | 0 | nada | Ya está bien clasificado |

Estas son las tres reglas de la Ec. 4.31, unificadas en una sola expresión. El `if e != 0` no es estrictamente necesario, porque con `e = 0` la suma no cambia nada, pero permite contar los errores.

El bias se actualiza como un peso cuya entrada siempre vale 1 (Ec. 4.35).

**Criterio de parada**

```python
if errors == 0:
    return W, b, epoch
raise RuntimeError("No convergió ...")
```

Si una época completa pasa sin errores, todos los patrones están bien clasificados y el algoritmo termina. El **teorema de convergencia** (sección 4-15 del libro) garantiza que esto ocurre en un número finito de pasos **si el problema es linealmente separable**. Si no lo es (por ejemplo, XOR), el bucle nunca termina y el `RuntimeError` avisa del problema.

### Salida en modo `verbose`

Cada línea muestra el número de paso, la entrada, el target, la entrada neta, la salida, el error, los pesos resultantes y si hubo actualización:

```
paso  1 | p=[ 1 -1 -1] t=0 n=+2.50 a=1 e=-1 -> W=[-0.5  0.   0.5] b=-0.50  [ACTUALIZA]
```

---

## 7. Evaluación exhaustiva

Como cada sensor solo toma dos valores, el espacio de entrada tiene **únicamente 2³ = 8 puntos**, los vértices de un cubo. Eso permite probar la red en **todas** las entradas posibles, no solo en una muestra.

### 7.1 `nearest_prototype(p)`

```python
def nearest_prototype(p):
    d_orange = np.sum(p != P_ORANGE)
    d_apple  = np.sum(p != P_APPLE)
    if d_orange == d_apple:
        return None, d_orange, d_apple
    return (0 if d_orange < d_apple else 1), d_orange, d_apple
```

Calcula la **distancia de Hamming**, es decir, cuántos elementos difieren, entre la entrada y cada prototipo:

- `p != P_ORANGE` produce un arreglo booleano, por ejemplo `[False, True, False]`.
- `np.sum` cuenta los `True`.

Devuelve la clase del prototipo más cercano, o `None` si hay empate. Sirve de **referencia independiente**: es la misma idea que usa la red de Hamming del Capítulo 3. En este problema nunca hay empates, porque los prototipos difieren en un solo bit y la suma de las dos distancias siempre es impar.

### 7.2 `evaluate_all(W, b, title)`

```python
for combo in itertools.product([-1, 1], repeat=3):
    p = np.array(combo)
    n = (W @ p + b).item()
    a = hardlim(n).item()
    ref, dn, dm = nearest_prototype(p)
```

Recorre las 8 entradas e imprime una tabla con:

- los tres valores de sensor,
- la entrada neta `n` y la salida `a`,
- la clase asignada por el perceptrón,
- las distancias de Hamming a cada prototipo,
- la clase de referencia y una marca ✓ o ✗ según coincidan.

Con los pesos entrenados, las 8 entradas coinciden con la referencia. Esto confirma la afirmación del libro (p. 3-7): cualquier entrada más cercana a un prototipo se clasifica como ese prototipo.

---

## 8. Vista previa embebida: inferencia con enteros

Esta sección no está en el libro. Es el puente hacia la implementación en microcontrolador o RTL.

### 8.1 `to_fixed_point(W, b, scale)`

```python
Wq = np.round(W * scale).astype(np.int8)
bq = np.round(b * scale).astype(np.int8)
```

Cuantiza los pesos multiplicándolos por un factor de escala y redondeando a `int8`.

**¿Por qué no cambia la clasificación?** La salida depende solo del **signo** de `n`. Si se multiplican `W` y `b` por una constante positiva `k`:

```
k·W·p + k·b = k·(W·p + b)
```

El signo no cambia, así que `hardlim` da el mismo resultado. Con los pesos entrenados `[−0.5, 2, 0.5]` y `b = −0.5`, la escala 2 los vuelve enteros **exactos**, sin error de redondeo: `[−1, 4, 1]` y `−1`.

Se usa una potencia de 2 porque en hardware escalar por 2ⁿ es solo un corrimiento de bits.

### 8.2 `infer_int(Wq, bq, p)`

```python
acc = int(bq[0])
for w, x in zip(Wq.ravel(), p):
    acc += int(w) if x > 0 else -int(w)
return 1 if acc >= 0 else 0, acc
```

Así funcionaría la neurona en un microcontrolador o en un bloque de hardware:

- **Sin multiplicaciones.** Como `x ∈ {−1, +1}`, `w·x` es simplemente `+w` o `−w`. Cada término es una suma o una resta.
- **Activación = bit de signo.** `acc >= 0` equivale a revisar el bit más significativo del acumulador en complemento a dos.
- **Tamaño del acumulador.** Con `W = [−1, 4, 1]`, `b = −1`, el acumulador va de −7 a +5 en la práctica (la tabla lo muestra). Cabe en **4 bits con signo** (−8…+7).

Traducido casi línea por línea a C:

```c
int8_t acc = B;
for (int i = 0; i < 3; i++)
    acc += (p[i] > 0) ? W[i] : -W[i];
uint8_t a = (acc >= 0);
```

### 8.3 `check_fixed_point(W, b, scale=2)`

Cuantiza los pesos, recorre las 8 entradas y compara la salida entera `a_int` con la de punto flotante `a_float`. Imprime ✓ en cada coincidencia y un veredicto final. Con escala 2 el resultado es **idéntico en los 8 casos**.

Este es el concepto de **modelo de referencia (golden model)**: el Python en punto flotante es la "verdad", y cualquier implementación en hardware debe reproducir sus salidas.

---

## 9. Programa principal

```python
if __name__ == "__main__":
```

Este bloque solo se ejecuta al correr el archivo directamente, no al importarlo desde otro script. Hace cinco cosas en orden:

1. **`perceptron_chapter3()`**: demuestra el diseño manual.
2. **`train_perceptron(..., W0=[0.5, -1, -0.5], b0=0.5)`**: entrena con las condiciones iniciales exactas del libro (Ec. 4.40), para comparar la traza con el texto.
3. **`evaluate_all(W, b, ...)`**: prueba los pesos aprendidos en las 8 entradas.
4. **`check_fixed_point(W, b, scale=2)`**: verifica la versión entera.
5. **Prueba de robustez:**
   ```python
   rng = np.random.default_rng(0)
   for _ in range(1000):
       _, _, ep = train_perceptron(TRAINING_SET,
                                   rng.uniform(-1, 1, 3),
                                   rng.uniform(-1, 1),
                                   verbose=False)
   ```
   Entrena 1000 veces desde pesos aleatorios uniformes en [−1, 1] y reporta el mínimo, la media y el máximo de épocas. La semilla `0` hace que el resultado sea reproducible. Con esta semilla: mínimo 1, media ≈ 2.16, máximo 3 épocas.

---

## 10. Traza completa del entrenamiento

Condiciones iniciales: `W = [0.5, −1, −0.5]`, `b = 0.5`.

| Paso | Entrada | t | n | a | e | W resultante | b |
|---|---|---|---|---|---|---|---|
| 1 | naranja `[1,−1,−1]` | 0 | +2.5 | 1 | −1 | `[−0.5, 0, 0.5]` | −0.5 |
| 2 | manzana `[1,1,−1]` | 1 | −1.5 | 0 | +1 | `[0.5, 1, −0.5]` | +0.5 |
| 3 | naranja `[1,−1,−1]` | 0 | +0.5 | 1 | −1 | `[−0.5, 2, 0.5]` | −0.5 |
| 4 | manzana `[1,1,−1]` | 1 | +0.5 | 1 | 0 | sin cambio | |
| 5 | naranja `[1,−1,−1]` | 0 | −3.5 | 0 | 0 | sin cambio | |
| 6 | manzana `[1,1,−1]` | 1 | +0.5 | 1 | 0 | sin cambio | |

- Los pasos 1–3 coinciden con las Ecs. 4.41–4.53 del libro.
- La época 2 (pasos 3–4) tuvo un error, así que el algoritmo sigue.
- La época 3 (pasos 5–6) pasa sin errores y el algoritmo termina.

Cálculo detallado del paso 1:

```
n = [0.5  −1  −0.5]·[1  −1  −1]ᵀ + 0.5
  = 0.5 + 1 + 0.5 + 0.5 = 2.5
a = hardlim(2.5) = 1
e = 0 − 1 = −1
W = [0.5 −1 −0.5] + (−1)·[1 −1 −1] = [−0.5  0  0.5]
b = 0.5 + (−1) = −0.5
```

---

## 11. Interpretación geométrica

La frontera de decisión es el plano:

```
W·p + b = 0
```

| Solución | Plano | Observación |
|---|---|---|
| Cap. 3 (manual) | `p[1] = 0` | Pasa por el origen, solo depende de la textura |
| Cap. 4 (aprendida) | `−0.5·p[0] + 2·p[1] + 0.5·p[2] − 0.5 = 0` | Inclinado; la textura domina (peso 2) |

Las dos separan correctamente los prototipos, pero **no son iguales**, como señala el libro en la p. 4-15. La regla del perceptrón se detiene en **la primera** solución que encuentra, no en la "mejor". No maximiza el margen, a diferencia de métodos posteriores como las SVM.

El peso de la textura (2) es el más grande en magnitud porque es la única característica que distingue las dos frutas. Los pesos de forma y peso son pequeños: el algoritmo los ajustó al pasar, pero no son necesarios.

---

## 12. Ejercicios sugeridos

1. **Cambiar las condiciones iniciales** a `W = [0, 0, 0]`, `b = 0`. ¿Cuántas épocas tarda? ¿Qué frontera encuentra?
2. **Invertir el orden** de `TRAINING_SET` (manzana primero). ¿La solución final es la misma?
3. **Agregar un problema no separable** (por ejemplo, XOR con dos entradas) y observar el `RuntimeError`.
4. **Cambiar `scale`** en `check_fixed_point` a 1 o a 4. ¿Con cuál aparece error de cuantización? ¿Por qué?
5. **Resolver el Ejercicio E3.1** del libro (plátanos y piñas) con `train_perceptron`, cambiando solo los prototipos.
6. **Extender a multineurona:** modificar `train_perceptron` para aceptar targets vectoriales y resolver el problema de cuatro clases P4.3/P4.5 del libro.
