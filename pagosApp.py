#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 21:38:45 2024

@author: juliansanchez

cd /Users/juliansanchez/App_pagos
streamlit run pagosApp.py


"""
import streamlit as st
import pandas as pd

# Ruta del archivo CSV para guardar la información
file_path = 'pagos_data.csv'

# Cargar el archivo CSV existente
df = pd.read_csv(file_path)

# Título de la aplicación con imagen
st.image('/Users/juliansanchez/App_pagos/A_small_icon-style_image_that_represents_a_financi.png', width=120)
st.title('Gestor de Pagos')

# Mostrar la tabla con los pagos
st.header('Estado de Pagos')

# Mostrar cada cuenta con su valor y si ha sido pagada
for i in range(len(df)):
    col1, col2, col3, col4, col5 = st.columns([2.5, 1.5, 1.5, 1.5, 1.5])
    with col1:
        cuenta = st.text_input(f"Cuenta {i+1}", df.at[i, 'Cuenta'], key=f'cuenta_{i}')
        df.at[i, 'Cuenta'] = cuenta
    with col2:
        valor = st.number_input(f"Valor {i+1}", df.at[i, 'Valor'], key=f'valor_{i}')
        df.at[i, 'Valor'] = valor
    with col3:
        fecha_pago = st.text_input(f"Fecha de Pago {i+1}", df.at[i, 'Fecha de Pago'], key=f'fecha_pago_{i}')
        df.at[i, 'Fecha de Pago'] = fecha_pago
    with col4:
        pagado = st.checkbox('Pagado', df.at[i, 'Pagado'], key=f'pagado_{i}')
        df.at[i, 'Pagado'] = pagado
    with col5:
        st.write("")  # Espacio vacío para alineación
        if st.button('Eliminar', key=f'eliminar_{i}'):
            df = df.drop(i).reset_index(drop=True)
            df.to_csv(file_path, index=False)
            st.experimental_rerun()

# Guardar cambios al archivo CSV
df.to_csv(file_path, index=False)

# Calcular totales
total_valor = df['Valor'].sum()
total_pagado = df[df['Pagado']]['Valor'].sum()
total_faltante = total_valor - total_pagado

# Mostrar los totales
st.header('Totales')
st.write(f"**Total Valor:** ${total_valor:,.2f}")
st.write(f"**Total Pagado:** ${total_pagado:,.2f}")
st.write(f"**Total Faltante:** ${total_faltante:,.2f}")

# Mostrar la tabla actualizada
st.header('Tabla de Pagos Actualizada')
st.dataframe(df)

# Sección para agregar una nueva cuenta
st.header('Agregar nueva cuenta')
nueva_cuenta = st.text_input('Nombre de la cuenta')
nuevo_valor = st.number_input('Valor', min_value=0.0, step=0.01)
nueva_fecha_pago = st.text_input('Fecha de Pago (día del mes o "Indeterminado")')

if st.button('Agregar Cuenta'):
    if nueva_cuenta:
        nueva_fila = {"Cuenta": nueva_cuenta, "Valor": nuevo_valor, "Fecha de Pago": nueva_fecha_pago or "Indeterminado", "Pagado": False}
        df = df.append(nueva_fila, ignore_index=True)
        df.to_csv(file_path, index=False)
        st.experimental_rerun()

# Ejecución de la aplicación: streamlit run pagosApp.py
