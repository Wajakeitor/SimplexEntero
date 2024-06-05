import streamlit as st
from scipy.optimize import linprog

# Configurar el ancho de la página
st.set_page_config(layout="wide")


st.title("Solución de Problemas de Programación Entera por Ramificación y Acotamiento.")

# Entrada para las dimensiones de la matriz
cols = st.columns(8)
m = cols[0].number_input("Cantidad de variables", min_value=2, value=3, step=1)
n = cols[1].number_input("Cantidad de restricciones", min_value=1, value=3, step=1)

# Funcion objetivo
objetivo = list(range(m))
MinMax = ['Min', 'Max']
cols = st.columns([3 if i%2==0 else 1 for i in range(2+2*m)])
minmaxOpcion = cols[0].selectbox("Hola Mundo", MinMax, label_visibility= 'collapsed')
cols[1].markdown("$Z = $")
for i in range(m):
    objetivo[i] = cols[i*2+2].number_input("Hello World", key=f"{i}", value=0.0, label_visibility='collapsed')
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

cols = st.columns([1 if i%2==0 else 3 for i in range(2*m)])

options2 = ['Continua', 'Entera', 'Binaria']
for i in range(m):
    cols[2*i].markdown(f"$X_{{{i}}}: $")
    tipos.append(cols[2*i+1].selectbox("variable", options=options2, key=f"{m+i}", index=1, label_visibility='collapsed'))



# Mostrar la matriz ingresada
st.write("Matriz ingresada:")
st.table(A)

