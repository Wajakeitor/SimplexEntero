import streamlit as st
import numpy as np
from scipy.optimize import linprog
from copy import deepcopy

# Configurar el ancho de la página
st.set_page_config(layout="wide")

# Estructura de arbol
rutaValor = []
rutaArbol = []
class Arbol():
    def __init__(self, m, C, A, b, A_eq, b_eq, tipoVariable, intervalos, min):
        self.m = m
        self.C = deepcopy(C)
        self.A_ub = deepcopy(A)
        self.b_ub= deepcopy(b)
        self.A_eq = deepcopy(A_eq)
        self.b_eq = deepcopy(b_eq)
        self.tipoVar = deepcopy(tipoVariable)
        self.intervalos = deepcopy(intervalos)
        self.cota = np.inf if min else np.NINF 
        self.min = min
        self.left = None
        self.right = None

    def __call__(self):
        result = linprog(c=self.C, A_ub=self.A, b_ub=self.b, A_eq=self.A_eq, b_eq=self.b_eq, bounds=self.intervalos, method='highs')
        if result.success:
            if (result.fun<self.cota and not self.min) or (result.fun>self.cota and self.min):
                for i in range(m):
                    if abs(int(result.x[i])-result.x[i]) > 0.000_000_1:
                        if self.tipoVar[i] != 'continua':
                            intervaloAux = deepcopy(intervalos)
                            intervaloAux[i] = intervaloAux[i][0], result.x[i]//1
                            self.left = Arbol(self.m, self.C, self.A_ub, self.b_ub, self.A_eq, self.b_eq, self.tipoVar, intervaloAux, self.min)

                            intervaloAux = deepcopy(intervalos)
                            intervaloAux[i] = result.x[i]//1 + 1, intervaloAux[i][1]
                            self.right = Arbol(self.m, self.C, self.A_ub, self.b_ub, self.A_eq, self.b_eq, self.tipoVar, intervaloAux, self.min)
                            break

                if result.fun in np.indrutaValor:
                    pass

        return result


st.title("Solución de Problemas de Programación Entera por Ramificación y Acotamiento.")

# Entrada para las dimensiones de la matriz
cols = st.columns(8)
m = cols[0].number_input("Cantidad de variables", min_value=2, value=3, step=1)
n = cols[1].number_input("Cantidad de restricciones", min_value=1, value=3, step=1)

# Funcion objetivo
C = list(range(m))
MinMax = ['Min', 'Max']
cols = st.columns([3 if i%2==0 else 1 for i in range(2+2*m)])
minmaxOpcion = cols[0].selectbox("Hola Mundo", MinMax, label_visibility= 'collapsed')
cols[1].markdown("$Z = $")
for i in range(m):
    C[i] = cols[i*2+2].number_input("Hello World", key=f"{i}", value=0.0, label_visibility='collapsed')
    cols[i*2+3].markdown(f"$X_{{{i+1}}}$")

cols = st.columns(1)
cols[0].markdown("s.a.")

# Crear la matriz de inputs
A = []
b = []
restriccion = []
tipos = []

options = ['≤', '=', '≥']
for i in range(n):
    row = []
    cols = st.columns([3 if i%2==0 else 1 for i in range(2*(m))]+[2.5,3,1])
    for j in range(m):
        value = cols[2*j].number_input("Algo mundo", key=f"{i}_{2*j}", value=0.0, label_visibility='collapsed')
        cols[2*j+1].markdown(f"$X_{{{j+1}}}$")
        row.append(value)

    A.append(row)
    value = cols[2*j+2].selectbox("tipo", options, key=f"{i}_{2*j+1}", label_visibility='collapsed')
    restriccion.append(value)

    value = cols[2*j+3].number_input(f"restricción", key=f"{i}_{2*j+2}", value=0.0, label_visibility='collapsed')
    b.append(value)

    cols[2*j+4].markdown(f"$b_{i}$")

cols = st.columns([1 if i%2==0 else 3 for i in range(2*m)]+[1,2])

# Definir el tipo de variable
options2 = ['Continua', 'Entera', 'Binaria']
for i in range(m):
    cols[2*i].markdown(f"$X_{{{i}}}: $")
    tipos.append(cols[2*i+1].selectbox("variable", options=options2, key=f"{m+i}", index=1, label_visibility='collapsed'))

cols[-1].markdown(f"$X_{{i}}\geq 0$")

cols = st.columns(1)

# Definir valores extras para simplex relajado
A_ub = []
b_ub = []
A_eq = []
b_eq = []
intervalos = []
if minmaxOpcion == 'Max':
    for i in range(m):
        C[i] *= -1


for i in range(n):
    if restriccion[i] == '≤':
        A_ub.append(A[i])
        b_ub.append(b[i])
    elif restriccion[i] == '=':
        A_eq.append(A[i])
        b_eq.append(b[i])
    else:
        A_ub.append([-a for a in A[i]])
        b_ub.append([-b[i]])

if len(A_ub) == 0: A_ub = None
if len(b_ub) == 0: b_ub = None
if len(A_eq) == 0: A_eq = None
if len(b_eq) == 0: b_eq = None

for i in range(m):
    if tipos[i] == 'Binaria':
        intervalos.append((0,1))
    else: intervalos.append((0, None))

arbol = Arbol(m, C, A_ub, b_ub, A_eq, b_eq, tipos, intervalos)