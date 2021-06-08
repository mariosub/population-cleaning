import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# datos
df = pd.read_csv ('population_spain_dataset.csv')
df.head()
df.tail()


# limpieza

df = df.loc[df['Nacimiento'] == 'Total']
del(df['Nacimiento'])

# chequeamos si hay cam27nieves88@gmail.compos nulos

df.isna().sum()

# no hay elementos nulos.
df.info()

# Elementos nulos en este caso si tiene sentido en el 'Total' que es el conteo de la población.

# valores únicos en periodo
df['Periodo'].unique()
# tenemos datos desde 2015 hasta 2020

# unique en el campo sexo
df['Sexo'].unique()

# también se puede borrar las filas que correspondan a Sexo = Total ya que es la suma de hombres + mujeres

df = df.loc[df['Sexo'] != 'Total']
df['Sexo'].unique()  # solo quedan hombers vs mujeres

# lo mismo pasa con la columna 'Edad'. Los datos que tiene el campo que vale "todas las edades" es la suma, por lo que también
# se podría eliminar.
df['Edad'].unique()
df = df.loc[df['Edad'] != 'Todas las edades']
# también hay algún espacio al principio --> lo quitamos
df['Edad'] = df['Edad'].str.strip()
df['Edad'].unique()

# con el lugar pasa que está la comunidad y sus provicias!!! hay que filtrar y/o eliminar las comunidades
# ya que se puede calcular con la suma de las provincias!!!

df['Lugar'].unique()
comun = ['01 Andalucía', '02 Aragón', '03 Asturias, Principado de', '04 Balears, Illes', '05 Canarias', '06 Cantabria', '07 Castilla y León',
'08 Castilla - La Mancha', '09 Cataluña', '10 Comunitat Valenciana', '11 Extremadura', '12 Galicia', '13 Madrid, Comunidad de', '14 Murcia, Región de',
'15 Navarra, Comunidad Foral de', '16 País Vasco', '17 Rioja, La', '18 Ceuta', '19 Melilla']
df = df.loc[~df['Lugar'].isin(comun)]
df['Lugar'].unique()

# vamos a quitar el número en los nombres de las provincias a partir de una función

def eliminar_cifras(txt):
  return "".join(c for c in txt if not c.isdigit())

df['Lugar'] = df['Lugar'].map(eliminar_cifras) # queda un espacio que hay que borrar

# quitamos el espacio del principio
df['Lugar'] = df['Lugar'].str.strip()

# aqui ya tenemos el dataset preparado
# periodos de 2015 a 2020
# sexo hombre/mujer
# total número de población que corresponda
# lugar corresponde a la provincia
# edad corresponde a los rangos de 4 años de edad desde 0 a 4 años, hasta 100 y más años

# exportamos los datos
df.to_csv("data_population_clean.cvs")

# los outliers en este caso no tienen sentido, todas las variables son categóricas
# excepto el periodo que es un entero pero solo obtiene valores de un rango, y el
# total donde el que un valor se salga del rango de la media no tiene sentido porque
# son datos reales que tienen importancia y no se han de quitar esos outliers.
# lo que si se puede haccer es verlos, pero no quitarlos!

###################################################

# agrupamos los danos que vamos a analizar

# Madrid 2020
df_madrid = df.loc[(df['Lugar']=='Madrid') & (df['Periodo']==2020)]
df_mad = pd.DataFrame({'Edad': list(df_madrid.loc[(df_madrid['Sexo']=='Mujeres')]['Edad']),
                    'Hombres': list(df_madrid.loc[(df_madrid['Sexo']=='Hombres')]['Total']),
                    'Mujeres': list(df_madrid.loc[(df_madrid['Sexo']=='Mujeres')]['Total'])})


# Zaragoza 2020
df_zaragoza = df.loc[(df['Lugar']=='Zaragoza') & (df['Periodo']==2020)]
df_zgz = pd.DataFrame({'Edad': list(df_zaragoza.loc[(df_zaragoza['Sexo']=='Mujeres')]['Edad']),
                    'Hombres': list(df_zaragoza.loc[(df_zaragoza['Sexo']=='Hombres')]['Total']),
                    'Mujeres': list(df_zaragoza.loc[(df_zaragoza['Sexo']=='Mujeres')]['Total'])})

# Extremadura 2020
df_extremadura = df.loc[((df['Lugar']=='Cáceres') | (df['Lugar']=='Badajoz')) & (df['Periodo']==2020)]
edades = list(df_extremadura.loc[(df_extremadura['Sexo']=='Mujeres') & (df_extremadura['Lugar']=='Badajoz')]['Edad'])
total_mujeres_ext = df_extremadura.loc[(df_extremadura['Sexo']=='Mujeres') & (df_extremadura['Lugar'].isin(['Badajoz', 'Cáceres']))]
total_hombres_ext = df_extremadura.loc[(df_extremadura['Sexo']=='Hombres') & (df_extremadura['Lugar'].isin(['Badajoz', 'Cáceres']))]
mujeres_ex = []
hombres_ex = []
for edad in edades:
    mujeres_ex.append(total_mujeres_ext.loc[total_mujeres_ext['Lugar'].isin(['Cáceres', 'Badajoz']) & (total_mujeres_ext['Edad'] == edad)]['Total'].sum())
    hombres_ex.append(total_hombres_ext.loc[total_hombres_ext['Lugar'].isin(['Cáceres', 'Badajoz']) & (total_hombres_ext['Edad'] == edad)]['Total'].sum())
df_ext = pd.DataFrame({'Edad': edades,
                    'Hombres': hombres_ex,
                    'Mujeres': mujeres_ex})


# España 2015-2020
df_espana = df.loc[(df['Lugar']=='Total Nacional')]
# envejecimiento
periods = list(df_espana['Periodo'].unique())
edades_mas_64 = ['De 65 a 69 años', 'De 70 a 74 años', 'De 75 a 79 años', 'De 80 a 84 años', 'De 85 a 89 años', 'De 90 a 94 años', 'De 95 a 99 años', '100 y más años']
dict_env = {}
total_pob_dict = {}
for per in periods:
	total_pob = df_espana.loc[df_espana['Periodo'] == per]['Total'].sum()
	total_pob_mas_64 = df_espana.loc[df_espana['Edad'].isin(edades_mas_64) & (df_espana['Periodo'] == per)]['Total'].sum()
	env = (total_pob_mas_64/total_pob)*100
    dict_env[per] = env
    total_pob_dict[per] = total_pob
# dataframe pirámide 2020
df_esp = pd.DataFrame({'Edad': list(df_espana.loc[(df_espana['Sexo']=='Mujeres') & (df_espana['Periodo'] == 2020)]['Edad']),
                    'Hombres': list(df_espana.loc[(df_espana['Sexo']=='Hombres') & (df_espana['Periodo'] == 2020)]['Total']),
                    'Mujeres': list(df_espana.loc[(df_espana['Sexo']=='Mujeres') & (df_espana['Periodo'] == 2020)]['Total'])})


##########################3
# histograma
df_espana['Total'].hist()

# corr
df_mujeres_mad = df_madrid.loc[df_madrid['Sexo'] == 'Mujeres']
anios = df_mujeres_mad['Edad']
pob = df_mujeres_mad['Total']
plot(list(anios), list(pob))

plot(list(anios), mujeres_ex)


df_hombres_mad = df_madrid.loc[df_madrid['Sexo'] == 'Hombres']
anios = df_hombres_mad['Edad']
pob = df_hombres_mad['Total']
plot(list(anios), list(pob))

plot(list(anios), hombres_ex)

# corrr
np.corrcoef(list(df_mujeres_mad['Total']), mujeres_ex)
np.corrcoef(list(df_hombres_mad['Total']), hombres_ex)
np.corrcoef(list(df_hombres_mad['Total']),  list(df_mujeres_mad['Total']))
np.corrcoef(hombres_ex, mujeres_ex)
np.corrcoef(list(df_hombres_mad['Total']), mujeres_ex)
np.corrcoef(list(df_mujeres_mad['Total']), hombres_ex)

##############
# regresión lineal
modelo = linear_model.LinearRegression()
modelo.fit(np.array([2020, 2019, 2018, 2017, 2016, 2015]).reshape(-1, 1), np.array([47450795, 47026208, 46722980, 46572132, 46557008, 46624382]).reshape(-1, 1))
y_pred = modelo.predict(np.array([2020, 2019, 2018, 2017, 2016, 2015]).reshape(-1, 1))
plt.plot(np.array([2020, 2019, 2018, 2017, 2016, 2015]).reshape(-1, 1), np.array([47450795, 47026208, 46722980, 46572132, 46557008, 46624382]).reshape(-1, 1))
plt.plot(np.array([2020, 2019, 2018, 2017, 2016, 2015]).reshape(-1, 1), y_pred, color='red')
plt.show()


################


# pirámides poblacionales
# zaragoza:
population_pyramid(df_zgz, 'Zaragoza')
# madrid:
population_pyramid(df_mad, 'Madrid')
# Extremadura
population_pyramid(df_ext, 'Extremadura')
# españa
population_pyramid(df_esp, 'España')
# env en españa
from matplotlib.pyplot import plot
plot(dict_env.keys(), dict_env.values())



def population_pyramid(dff, name):
    y = range(0, len(dff))
    x_male = dff['Hombres']
    x_female = dff['Mujeres']

    #define plot parameters
    fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(9, 6))

    #specify background color and plot title
    fig.patch.set_facecolor('xkcd:light grey')
    plt.figtext(.5,.9,name, fontsize=15, ha='center')

    #define male and female bars
    axes[0].barh(y, x_male, align='center', color='royalblue')
    axes[0].set(title='Hombres')
    axes[1].barh(y, x_female, align='center', color='lightpink')
    axes[1].set(title='Mujeres')

    #adjust grid parameters and specify labels for y-axis
    axes[1].grid()
    axes[0].set(yticks=y, yticklabels=dff['Edad'])
    axes[0].invert_xaxis()
    axes[0].grid()

    #display plot
    plt.show()
