import pandas as pd

#Importacion de dataframe
base_url = 'https://www.datos.gov.co/resource/62tk-nxj5.csv'
limit = 50000
offset = 0
all_dataframes = []

while offset<4000000:
    url = f'{base_url}?$limit={limit}&$offset={offset}'
    print(f'Descargando: {url}')
    df_chunk = pd.read_csv(url)

    if df_chunk.empty:
        break  # Ya no hay más datos

    all_dataframes.append(df_chunk)
    offset += limit  # Pasamos a la siguiente página

# Unimos todos los DataFrames
df_original = pd.concat(all_dataframes, ignore_index=True)

# Guardar el DataFrame en un archivo CSV
nombre_archivo = 'modelConstruction/data/datos_descargados.csv'
df_original.to_csv(nombre_archivo, index=False)
print(f'Datos guardados en {nombre_archivo}')

"""
This code is written by: David Velásquez    
Contact: davisitovelasquez06@gmail.com
"""