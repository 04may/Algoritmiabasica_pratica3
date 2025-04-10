# 📌 Practica 3: Búsqueda con retroceso

## 📌 1. Presentación de la práctica
Este proyecto implementa un **algoritmo de búsqueda con retroceso** (backtracking) para contar el número de recorridos válidos que puede realizar un robot (YuMi) en una cuadrícula con restricciones específicas.  
El robot:
- Empieza en la esquina inferior izquierda de la cuadrícula (coordenadas \((0, 0)\)).
- Debe visitar cada cuadrado exactamente una vez (camino hamiltoniano).
- Debe pasar por tres puntos de control en pasos específicos: \(\lfloor m \times n / 4 \rfloor\), \(\lfloor 2 \times m \times n / 4 \rfloor\), \(\lfloor 3 \times m \times n / 4 \rfloor\).
- Finaliza en la casilla \((0, 1)\).

Este enfoque utiliza la técnica de **backtracking** para generar y filtrar recorridos posibles en la cuadrícula.

## 📌 2. Características
* **Recorrido Hamiltoniano** con pasos de control definidos.
* **Búsqueda con retroceso** (backtracking) para explorar todas las posibilidades.
* **Filtrado (pruning)** mediante distancias de Manhattan y verificación de conectividad.
* **Opcional (Bola extra)**: Enfoque *meet in the middle* (`man_in_the_middle.py`) para optimizar la búsqueda.
* **Resultados**:
  - Se muestra el número total de recorridos válidos.
  - Se calcula el tiempo de ejecución en milisegundos.
  
---

## 📌 3. Organización de archivos

El directorio contiene los siguientes archivos:

- **📜 `retroceso.py`**  
  Script principal que implementa la búsqueda con retroceso para calcular los recorridos válidos.
- **📜 `man_in_the_middle.py`**  
  Versión opcional con la técnica *meet in the middle* para la bola extra (optimización).
- **📜 `test.txt`**  
  Fichero de entrada que contiene los casos de prueba (dimensiones de la cuadrícula y puntos de control).
- **📜 `results.txt`**  
  Archivo de salida con el número de recorridos y el tiempo de ejecución para cada caso de `test.txt`.
- **📜 `results_man_in_the_middle.txt`**  
  Archivo de salida para la versión *meet in the middle*.
- **📜 `ejecutar.sh`**  
  Script de automatización para compilar/ejecutar (si es necesario).
- **📜 `README.md`**  
  Este archivo, con la descripción del proyecto y las instrucciones de uso.

---

## 📌 4. Instrucciones de uso

1. **Dar permisos de ejecución** :
   ```sh
   chmod +x ejecutar.sh
    ./ejecutar.sh

2. **Ejecutar el algoritmo de búsqueda** : 
Para correr el programa principal (backtracking) y procesar los casos de prueba definidos en test.txt, ejecute:
   ```sh
   python retroceso.py

3. **Ejecutar la versión meet in the middle (Bola extra)**
Para probar la variante con la estrategia meet in the middle y procesar los casos de prueba definidos en test.txt,, ejecute:
   ```sh
   python man_in_the_middle.py



