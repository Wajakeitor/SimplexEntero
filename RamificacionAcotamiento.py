import streamlit as st
import numpy as np
import locale
from scipy.optimize import linprog
from copy import deepcopy
from graphviz import Digraph

# Configurar el ancho de la página
st.set_page_config(layout="wide")

import subprocess

# Ejecutar el comando y capturar la salida
output = subprocess.check_output(["cat", "/etc/lsb-release"])

# Decodificar la salida y mostrarla
st.write(output.decode("utf-8"))

# Configurar el locale para el formato numérico de México
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def format_number(num):
    return locale.format_string("%0.3f", num, grouping=True)

# Estructura de arbol
rutaValor = []
rutaArbol = []
cota = np.inf
SolOptima = []
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
        self.min = min
        self.x = None
        self.fun = None
        self.left = None
        self.right = None
        self.label = ""
        self.separador = None
        self.valSep = None

    def __call__(self):
        global cota
        global SolOptima
        global rutaValor
        global rutaArbol

        result = linprog(c=self.C, A_ub=self.A_ub, b_ub=self.b_ub, A_eq=self.A_eq, b_eq=self.b_eq, bounds=self.intervalos, method='highs')
        if result.success:
            solucion = True
            self.x = result.x
            self.fun = result.fun
            if (result.fun <= cota):
                for i in range(m):
                    if abs(int(result.x[i])-result.x[i]) > 0.000_001:
                        if self.tipoVar[i] != 'Continua':
                            self.valSep = int(result.x[i])
                            self.separador = i
                            intervaloAux = deepcopy(self.intervalos)
                            intervaloAux[i] = [intervaloAux[i][0], int(result.x[i])]
                            self.left = Arbol(self.m, self.C, self.A_ub, self.b_ub, self.A_eq, self.b_eq, self.tipoVar, intervaloAux, self.min)

                            intervaloAux = deepcopy(self.intervalos)
                            intervaloAux[i] = [int(result.x[i]) + 1, intervaloAux[i][1]]
                            self.right = Arbol(self.m, self.C, self.A_ub, self.b_ub, self.A_eq, self.b_eq, self.tipoVar, intervaloAux, self.min)
                            solucion = False
                            break
                        
                if solucion:
                    if result.fun < cota:
                        cota = result.fun
                        SolOptima = result.x
                        self.label = "Z cota"
                    else:
                        self.label = "Agotado"
                else:
                    if result.fun <= cota:
                        final=True
                        for i in range(len(rutaValor)):
                            if rutaValor[i] == result.fun:
                                rutaArbol[i].append(self.left)
                                rutaArbol[i].append(self.right)
                                final = False
                                break
                        if final:
                            rutaValor.append(result.fun)
                            rutaArbol.append([])
                            rutaArbol[-1].append(self.left)
                            rutaArbol[-1].append(self.right)
                        self.label = ""
                    else:
                        self.left = "Agotado"
            
            else:
                self.label = "Problema agotado"

        else: self.label = "Solución no factible"

        if len(rutaValor)==0: return self
        else:
            i = np.argmin(rutaValor)
            nodo = rutaArbol[i][0]
            rutaArbol[i].pop(0)
            if len(rutaArbol[i]) == 0:
                rutaArbol.pop(i)
                rutaValor.pop(i)
            nodo()

        return self


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
    cols[2*i].markdown(f"$X_{{{i+1}}}: $")
    tipos.append(cols[2*i+1].selectbox("variable", options=options2, key=f"{m+i}", index=1, label_visibility='collapsed'))

cols[-1].markdown(f"$X_{{i+1}}\geq 0$")

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
        b_ub.append(-b[i])

if len(A_ub) == 0: A_ub = None
if len(b_ub) == 0: b_ub = None
if len(A_eq) == 0: A_eq = None
if len(b_eq) == 0: b_eq = None

for i in range(m):
    if tipos[i] == 'Binaria':
        intervalos.append((0,1))
    else: intervalos.append((0, None))

arbol = Arbol(m, C, A_ub, b_ub, A_eq, b_eq, tipos, intervalos, minmaxOpcion)
arbol()


signo = -1 if minmaxOpcion == 'Max' else 1

st.write("La solución optima es:")
st.write(SolOptima)
st.write(f"Z = {cota * signo if cota else None}")


def EscribirSolucion(array):
    if array is None: return ""
    cadena = ""
    for i, x in enumerate(array):
        if i%4 == 0 and i != 0: cadena += "\n"
        cadena += f"X_{i+1} = {format_number(x)}  "
    return cadena

# Crear un gráfico simple
dot = Digraph()

Aristas = []
i = 0
def PintarHijo(padre, ipadre):
    global i
    if padre.left != None:
        dot.node(f'{i}', f'{ EscribirSolucion(padre.left.x)}\n{ padre.left.fun * signo if padre.left.fun  else "" }\n{padre.left.label}')
        Aristas.append([f'{ipadre}', f'{i}', f"X_{padre.separador+1} ≤ {padre.valSep}"])
        ipadreI = i
        i += 1
    if padre.right != None:
        dot.node(f'{i}', f'{EscribirSolucion(padre.right.x)}\n{padre.right.fun * signo if padre.right.fun else ""}\n{padre.right.label}')
        Aristas.append([f'{ipadre}', f'{i}', f"X_{padre.separador+1} ≥ {padre.valSep+1}"])
        ipadreD = i
        i += 1
    if padre.left != None: PintarHijo(padre.left, ipadreI)
    if padre.right != None: PintarHijo(padre.right, ipadreD)

dot.node(f'{i}', f'{EscribirSolucion(arbol.x)}\n{arbol.fun * signo if arbol.fun else ""}\n{arbol.label}')
i += 1
PintarHijo(arbol, 0)

for origen, destino, etiqueta in Aristas:
    dot.edge(origen, destino, label=etiqueta)

# Renderizar el gráfico en Streamlit
st.graphviz_chart(dot)
