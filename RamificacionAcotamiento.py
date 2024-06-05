import streamlit as st
from scipy.optimize import linprog

# Configurar el ancho de la página
st.set_page_config(layout="wide")

def main():
    st.title("Matriz Dinámica en Streamlit")
    
    # Entrada para las dimensiones de la matriz
    n = st.number_input("Número de filas (n)", min_value=1, value=3, step=1)
    m = st.number_input("Número de columnas (m)", min_value=1, value=3, step=1)

    # Crear la matriz de inputs
    matrix = []
    for i in range(n):
        row = []
        cols = st.columns(m)
        for j in range(m):
            value = cols[j].text_input(f"({i},{j})", key=f"{i}_{j}")
            row.append(value)
        matrix.append(row)
    
    # Mostrar la matriz ingresada
    st.write("Matriz ingresada:")
    st.table(matrix)

if __name__ == "__main__":
    main()
