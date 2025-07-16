import pandas as pd

df_original = pd.read_csv('modelConstruction/data/datos_descargados.csv', encoding='utf-8') #Se carga el dataset descargado


df=df_original.copy() #Se crea una copia del dataset para trabajar sobre esta y asi preservar el original
df=df.dropna()
df=df.drop_duplicates()
df=df.drop(["codigosensor","descripcionsensor","unidadmedida","codigoestacion"],axis=1)

print("Departamentos Ordenados:")
departamentos_ordenados=sorted(df['departamento'].unique())
print(departamentos_ordenados)

df=df.replace('<nil>',None) 

"""
Debido a la gran cantidad de datos que se estan manejando, nos podemos 
permitir borrar los datos nulos sin que afecte al entrenamiento del modelo.
"""

df=df.dropna()

#Se remplazan valores repetidos con inconsistencias(tildes)
df['departamento'] = df['departamento'].replace({
    'ATLANTICO': 'ATLÁNTICO',
    'BOGOTA': 'BOGOTÁ D.C.',
    "BOGOTA D.C.":"BOGOTÁ D.C.",
    'BOLIVAR': 'BOLÍVAR',
    'BOYACA': 'BOYACÁ',
    'CHOCO': 'CHOCÓ',
    'CORDOBA': 'CÓRDOBA',
    'NARINO': 'NARIÑO',
    'GUAINIA': 'GUAINÍA',
    'QUINDIO': 'QUINDÍO',
    'VAUPES': 'VAUPÉS'
})

df['fechaobservacion']=pd.to_datetime(df['fechaobservacion']) #Se convierte el tipo de dato de la columan de fecha que estaba como object a un de tipo datatime

df['año'] = df['fechaobservacion'].dt.year
df["mes"] = df['fechaobservacion'].dt.month

print(" ")
print("Informacion del DataSet:")
print(df.info())

print(" ")
print("DataSet Limpio:")
print(df)

"""
This code is written by: David Velásquez    
Contact: davisitovelasquez06@gmail.com
"""