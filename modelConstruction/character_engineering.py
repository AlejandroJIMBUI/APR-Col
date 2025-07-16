#Ingenieria de caracteristicas
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

from category_encoders import *
from clean_data import df

caracteristicas_numericas = ['latitud', 'longitud']

scaler=MinMaxScaler()
df[caracteristicas_numericas] = scaler.fit_transform(df[caracteristicas_numericas])

print("Caracteristicas Categoricas:")
caracteristicas_categoricas = list(df.select_dtypes(include="object"))
print(caracteristicas_categoricas)

label_encoders={}
mapeos_categorias = {}
for column in caracteristicas_categoricas:
  le=LabelEncoder()
  df[column+"_encoded"]=le.fit_transform(df[column])
  label_encoders[column] = le  # Se guarda el encoder
  mapeos_categorias[column] = dict(zip(le.classes_, le.transform(le.classes_)))  # Se guardas el mapeo
  
df=df.drop(["nombreestacion","departamento","municipio","zonahidrografica"],axis=1)

print("")
print("Correlacion entre las variables:")
print(df.corr())

"""
This code is written by: David Velásquez    
Contact: davisitovelasquez06@gmail.com
"""