# Perceptrón en Hardware — Clasificador Manzana / Naranja

Implementación de un perceptrón simple, pensada como primer paso hacia una red neuronal en hardware (microcontrolador y/o RTL).

**Referencia:** M. T. Hagan, H. B. Demuth, M. H. Beale — *Neural Network Design*, Capítulos 3 y 4.

---

## Problema

Un distribuidor quiere separar fruta en una banda transportadora. Tres sensores miden cada fruta y entregan valores bipolares (±1):

| Entrada | Sensor  | +1                | −1                |
|---------|---------|-------------------|-------------------|
| `p[0]`  | Forma   | redonda           | elíptica          |
| `p[1]`  | Textura | lisa              | rugosa            |
| `p[2]`  | Peso    | más de 1 libra    | menos de 1 libra  |

Prototipos:

```
naranja  p1 = [ 1, -1, -1]
manzana  p2 = [ 1,  1, -1]
```

---

## Contenido del script

`perceptron_hagan.py` incluye:

1. **Funciones de transferencia:** `hardlim` (salida 0/1) y `hardlims` (salida ±1).
2. **Diseño gráfico (Cap. 3):** `W = [0 1 0]`, `b = 0`, con salida `hardlims`.
3. **Regla de aprendizaje del perceptrón (Cap. 4):**
   ```
   e     = t - a
   W_new = W_old + e·pᵀ
   b_new = b_old + e
   ```
   Parte de las condiciones iniciales del libro (`W = [0.5 -1 -0.5]`, `b = 0.5`) y reproduce las ecuaciones 4.41–4.53.
4. **Evaluación exhaustiva:** prueba las 8 combinaciones posibles de sensores (2³) y las compara con el prototipo más cercano en distancia de Hamming.
5. **Vista previa embebida:** cuantiza los pesos a enteros `int8` y verifica que la inferencia en aritmética entera coincide con la de punto flotante.
6. **Robustez:** entrena desde 1000 inicializaciones aleatorias y reporta cuántas épocas tarda en converger.

---

## Cómo ejecutarlo

### Requisitos
- Python 3.8 o superior
- NumPy

### 1. Instalar Python

- **Windows:** descárgalo de [python.org](https://www.python.org/downloads/). En el instalador marca la casilla **"Add Python to PATH"**.
- **macOS:** `brew install python`, o el instalador de python.org.
- **Linux:** normalmente ya viene instalado. Si no: `sudo apt install python3 python3-pip`.

Para comprobar la instalación:

```bash
python --version      # en macOS/Linux puede ser: python3 --version
```

### 2. (Opcional) Crear un entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install numpy     # en macOS/Linux puede ser: pip3 install numpy
```

### 4. Ejecutar

```bash
python perceptron_hagan.py
```

> **Windows:** si aparece un `UnicodeEncodeError` (por los símbolos ✓ y ✗), ejecuta:
> ```bash
> python -X utf8 perceptron_hagan.py
> ```

También funciona sin instalar nada en **Google Colab**, o en **VS Code** con la extensión de Python.

---

## Resultados esperados

### Entrenamiento (Cap. 4)

```
Inicial: W = [ 0.5 -1.  -0.5], b = 0.5
paso  1 | p=[ 1 -1 -1] t=0 n=+2.50 a=1 e=-1 -> W=[-0.5  0.   0.5] b=-0.50  [ACTUALIZA]
paso  2 | p=[ 1  1 -1] t=1 n=-1.50 a=0 e=+1 -> W=[ 0.5  1.  -0.5] b=+0.50  [ACTUALIZA]
paso  3 | p=[ 1 -1 -1] t=0 n=+0.50 a=1 e=-1 -> W=[-0.5  2.   0.5] b=-0.50  [ACTUALIZA]
paso  4 | p=[ 1  1 -1] t=1 n=+0.50 a=1 e=+0 -> ...  [ok]
...
Convergió en la época 3 (6 presentaciones).
```

**Solución final:** `W = [-0.5  2  0.5]`, `b = -0.5`, igual que en el libro.

### Evaluación

Las 8 entradas posibles se clasifican igual que el prototipo más cercano en distancia de Hamming. En 1000 inicializaciones aleatorias, el entrenamiento converge siempre en 3 épocas o menos.

---

## Hacia el hardware

Multiplicando los pesos entrenados por 2, todos quedan enteros:

```
W = [-1  4  1],  b = -1     (int8)
```

La inferencia con esos enteros da el mismo resultado que la de punto flotante en los 8 casos. Esto importa para el hardware porque:

- **No se necesitan multiplicadores.** Como las entradas son ±1, cada término del producto `w·p` es sumar o restar el peso.
- **La activación es trivial.** `hardlim` se reduce a leer el bit de signo del acumulador.
- **El acumulador es pequeño.** Con estos pesos el rango es −7…+7, así que basta un acumulador de 4 bits con signo.

En hardware, la neurona completa es un sumador/restador más un comparador de signo.

---

## Hoja de ruta

- [x] Modelo de referencia en Python (Caps. 3 y 4 de Hagan)
- [x] Verificación de inferencia en aritmética entera
- [ ] Implementación en C para microcontrolador (inferencia y, opcionalmente, entrenamiento en el chip)
- [ ] Implementación RTL (Verilog/SystemVerilog) de la neurona
- [ ] Testbench que compare contra vectores dorados generados por el modelo Python
- [ ] Evaluación de recursos (ciclos, memoria, área/LUTs)
- [ ] Extensión a perceptrón multineurona (problemas P4.3 / P4.5 del libro)

---

## Referencias

- Hagan, M. T., Demuth, H. B., Beale, M. H., De Jesús, O. *Neural Network Design*, 2nd ed.
- Rosenblatt, F. (1958). "The perceptron: A probabilistic model for information storage and organization in the brain." *Psychological Review*, 65, 386–408.
