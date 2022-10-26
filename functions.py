import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import plotly.express as px
import seaborn as sns
from folium import plugins 





def intro():
    
    st.title('Análisis de los alojamientos turísticos en Madrid')
    st.subheader("Introducción")

    with st.expander('Contexto', expanded= False):
        st.write("""
            Airbnb es una compañía que ofrece una plataforma digital dedicada a la oferta de alojamientos a particulares y turísticos 
            (alquiler vacacional) mediante la cual los anfitriones pueden publicitar y contratar el arriendo de sus propiedades con sus
             huéspedes; anfitriones y huéspedes pueden valorarse mutuamente, como referencia para futuros usuarios.\n
            Airbnb es la compañía de referencia en lo que a "alquiler vacacional" se refiere, y es por eso que vamos a analizar sus datos.
            """)

def carga_datos():
    # Leer CSV
    global data 
    data = pd.read_csv('./listings_completo.csv', encoding= 'utf8', sep = ',')
    
    # Eliminacion de columnas
    data = data.drop(['scrape_id', 'last_scraped', 'source'], axis = 1)

    data = data.drop(['description', 'neighborhood_overview', 'picture_url', 'host_url', 'host_since', 
                    'host_location', 'host_about', 'host_response_time', 'host_response_rate', 'host_acceptance_rate',
                    'host_is_superhost', 'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood',
                    'host_verifications', 'host_has_profile_pic', 'host_identity_verified','host_total_listings_count'], axis = 1)

    data = data.drop(['neighbourhood', 'bathrooms', 'bathrooms_text', 'beds', 
                    'amenities', 'bedrooms', 'minimum_minimum_nights', 'maximum_minimum_nights',
                    'minimum_maximum_nights', 'maximum_maximum_nights', 'minimum_nights_avg_ntm',
                    'maximum_nights_avg_ntm', 'calendar_updated', 'availability_60', 'availability_90', 
                    'availability_365', 'calendar_last_scraped'], axis = 1)

    data = data.drop(['number_of_reviews_ltm', 'number_of_reviews_l30d', 'first_review', 'review_scores_rating', 
                    'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
                    'review_scores_location', 'review_scores_value', 'instant_bookable', 'calculated_host_listings_count_entire_homes',
                    'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms',
                    'reviews_per_month'], axis = 1)

    data = data.drop(['id', 'host_listings_count', 'maximum_nights', 'last_review', 'availability_30', 
                    'has_availability', 'neighbourhood_cleansed'], axis = 1)

    # Renombrar columna

    data = data.rename(columns={'neighbourhood_group_cleansed': 'neighbourhood', 'calculated_host_listings_count': 'host_lcount'})

    # Eliminacion de filas con nulos en nombre

    data = data[data.name.notnull()]

    # Transformacion de datos de columna precio a 'int' por problemas

    data['price'] = data['price'].str.replace('$',' ')
    data['price'] = data['price'].str.replace(',','', regex=False).astype(float)
    data['price'] = data['price'].astype(int)

    # Reemplazar nulos y pasarlos a boolean

    data['license'].fillna(0,inplace=True)
    data['license'] = data['license'].apply(lambda x: 1 if x!=0 else 0)
    data['license'] = data['license'].astype(bool)

    return data

def analisis_intro():
    
    st.header("Datos")

    with st.container():
        st.write("""
            En Madrid actualmente hay casi 21000 anuncios de alojamientos turísticos.\n
            A continuación podemos ver algunos datos básicos acerca de como están distribuidos los anuncios en funcion de los barrios.
            \n
            Como es lógico la mayor concentracion de anuncios se encuentra en la zona centro de la capital.
            """)


# Primera grafica de los alojamientos por distrito 

def conteo_distrito():
    conteo = data['neighbourhood'].value_counts(ascending=True)

    fig = plt.figure(figsize=(10,5))
    plt.hlines(y=conteo.index,
            xmin=0,
            xmax=conteo,
            color='skyblue')

    plt.plot(conteo, conteo.index, 'o')
    st.pyplot(fig)

# Segunda grafica de los alojamientos por distrito    

def conteo_distrito2():
    
    df_neigh = data.groupby('neighbourhood')["listing_url"].count()
    df_neigh = pd.DataFrame(df_neigh)
    df_neigh.reset_index(inplace = True)
    df_neigh.columns = ["Distrito","num.alojamientos"]
    df_neigh = df_neigh.sort_values("num.alojamientos", ascending = False)

    df_neigh[:10]
    #Represento en un pieplot la distribución de los aumentos más relevantes y agrupo el resto en la categoría "otros ajustes". 

    #the top 5
    df_neigh_5 = df_neigh[:10].copy()

    #others
    new_row = pd.DataFrame(data = {
        "Distrito" : ["Otros"],
        "num.alojamientos" : [df_neigh["num.alojamientos"][5:].sum()]
    })

    #combining top 5 with others
    df_neigh_pie = pd.concat([df_neigh_5, new_row])

    fig = px.pie(df_neigh_pie, 
            values="num.alojamientos", 
            names='Distrito',
            title='Porcentaje de alojamientos por distrito',
            template="plotly_white"
            )
    
    fig.update_traces(textposition='inside', textinfo='percent')

    st.plotly_chart(fig,use_container_width=True)
    


def color_map():
    fig = plt.figure(figsize=(10,6))
    sns.scatterplot(x=data['longitude'], y=data['latitude'], hue=data['neighbourhood'])
    plt.ioff()

    return st.pyplot(fig)

# Mapa de calor por coodenadas

def heat_map_mad():

    map_madrid = folium.Map(location=[40.418759, -3.688986], zoom_start=11)

    heat_data = [[row['latitude'], row['longitude']] for index, row in data.iterrows()]

    # plot in the map
    plugins.HeatMap(heat_data).add_to(map_madrid)
   
    return st_folium(map_madrid)


def hipotesis():
    st.title('Existe economía sumergida en relación a los alojamientos turísticos')
    st.write("""
            Son muchos los artículos de opinión que tratan acerca de este tema. 
            Unos dicen que es economía colaborativa y otros lo tachan de economía sumergida.
            \n
            Según el modelo de "Airbnb", la idea es conectar personas que quieren ofrecer sus casas o
            sus espacios, con personas que viajan y necesitan un alojamiento.\n
            Indican además, que está enfocado a que muchas de las familias de clase media que afrontan desafíos 
            económicos y son propietarias de casas, puedan generar ingresos compartiéndolas.\n
            Y en cuanto al cumplimiento de leyes y economía, indican que impulsan a los anfitriones a cumplir 
            con sus obligaciones fiscales y buscan nuevas vías con los gobiernos para garantizar que lo hacen.
            \n
            Para intentar esclarecer todo esto vamos a analizar algunos datos.
            """)

# Gráfica tipo de alojamientos por distritos
  
def room_type():

    fig, ax = plt.subplots(figsize=(10, 6))
    room_data = (
        data
        .groupby(['neighbourhood', 'room_type'])
        .size()
        .unstack('room_type')
        .fillna(0)
        .sort_values('Entire home/apt')
        .apply(lambda row: row / row.sum(), axis=1)
        .reindex(columns=data['room_type'].value_counts().index))
    room_data.plot(kind='barh', width=.75, stacked=True, ax=ax)

    ax.set_xticks(np.linspace(0,1, 5))
    ax.set_xticklabels(np.linspace(0,1, 5))
    ax.grid(axis='x', c='k', ls='--')
    ax.set_xlim(0,1)

    ax.set_ylabel('Distrito')
    ax.set_xlabel('Porcentaje de Anuncios')
    ax.legend(loc=(1.01, 0))

    ax.set_title('Tipos de Habitación', weight='bold')

    return st.pyplot(fig)
    # st.plotly_chart(fig,use_container_width=True)

# Gráfica, numero de anuncios por anfitrion

def host_list():
    
    df_host = data.groupby('host_lcount')['listing_url'].nunique()
    df_host = pd.DataFrame(df_host)
    df_host.reset_index(inplace = True)
    df_host.columns = ['anuncios.anfitrion', 'numero.anunciantes']
    df_host = df_host.sort_values("anuncios.anfitrion", ascending = True)

    #Represento en un pieplot la distribución de los aumentos más relevantes y agrupo el resto en la categoría "otros ajustes". 

    #the top 5
    df_host_5 = df_host[:5].copy()

    #others
    new_row = pd.DataFrame(data = {
                        "anuncios.anfitrion" : ["6 o más"],
                        "numero.anunciantes" : [df_host["numero.anunciantes"][5:].sum()]
    })

    #combining top 5 with others
    df_host_pie = pd.concat([df_host_5, new_row])

    df_host_pie.agg(sum)

    fig = px.pie(df_host_pie, 
                values="numero.anunciantes", 
                names='anuncios.anfitrion',
                title='Porcentaje de anunciantes por alojamiento',
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.G10,
                )
        
    fig.update_traces(textposition='inside', textinfo='percent')

    return st.plotly_chart(fig,use_container_width=True)
    
# Gráfica, numero de anuncios por anfitrion2

def host_list2():

    fig = px.violin(data, y="host_lcount", width=600, height=600)

    return st.plotly_chart(fig,use_container_width=True)

def licencias():

    fig = px.bar(data.license.value_counts(),
            y="license",
            color='license')
    fig.update_coloraxes(colorscale='Bluered')

    
    return st.plotly_chart(fig,use_container_width=True)

# Gráfica de los alojamientos que disponen de licencia

def licencias2():

    licencia = pd.DataFrame(data['license'].value_counts())
    licencia['Porcentaje'] = ((licencia ['license'] /licencia ['license'].sum())*100).round(2)
    licencia['Porcentaje'] = licencia ['Porcentaje'].astype(str) + " %" 

    return st.table(licencia)

# Grafico de minimo de noches

def min_noches():

    fig = px.violin(data,
                y= 'minimum_nights',
                width=600, height=600)

    return st.plotly_chart(fig,use_container_width=True)

def min_noches2():

    # Conteo minimo de noches

    df_min = data.groupby("minimum_nights")["listing_url"].count()
    df_min = pd.DataFrame(df_min)
    df_min.reset_index(inplace = True)
    df_min.columns = ["minimo_noches","num.alojamientos"]
    df_min = df_min.sort_values("num.alojamientos", ascending = True)

    def grupos(x):
        if x == 1:
            return 'Estancias de 1 día'
        elif x > 1 and x <= 3:
            return 'Estancias de 2 o 3 dias'
        elif x > 3 and x <= 10:
            return 'Estancias de 3 a 10 dias'
        elif x > 10 and x <= 21:
            return 'Estancias de 10 a 21 dias'
        else:
            return 'Estancias de mas de 21 dias'

    df_min['minimo_noches'] = df_min['minimo_noches'].apply(grupos)

    df_min = pd.DataFrame(df_min.groupby('minimo_noches')['num.alojamientos'].sum().reset_index()).sort_values(by='num.alojamientos', ascending=False)

    # Grafica minimo de noches para reserva

    fig = px.bar(df_min,
            x= 'minimo_noches',
            y= 'num.alojamientos',
            title='Minimo de noches necesario para reservar',
            color= 'minimo_noches',
            color_discrete_sequence=px.colors.qualitative.Vivid,
            )
    return st.plotly_chart(fig,use_container_width=True)


# Grafica precio promedio por distrito

def precio_promedio():

    # Bar plot precio-mediana/distrito

    median_prices = pd.DataFrame(data.groupby('neighbourhood')["price"].median().reset_index())

    fig = px.bar(median_prices,
                    x= 'neighbourhood',
                    y= 'price',
                    color= 'neighbourhood',
                    title='Precio más representativo por distrito',
                    template="plotly_white",
                    color_discrete_sequence=px.colors.qualitative.Light24,
                    )
                     
    return st.plotly_chart(fig,use_container_width=True)

 # Scatter plot precio/numero de noches/capacidad

def precio_cap_noches():

    fig = px.scatter(data,
                x= 'minimum_nights',
                y= 'accommodates',
                color= 'price')
    fig.update_coloraxes(colorscale='haline')

    return st.plotly_chart(fig,use_container_width=True)
    
def conclusion():
    st.title('Conclusión')
    st.write("""
            Tras analizar los datos y las gráficas obtenidas, me reafirmo en la hipótesis de que existe una 
            economía sumergida en torno a este tipo de alojamientos.\n

            Son varios los factores que tiran por tierra la "filosofía" de la economía colaborativa. Vamos a hacer recuento:\n

                - La mayoría de los alojamietos ofertados pertenecen a la categoría de "pisos enteros" o "habitaciones privadas".\n
                - La mayoría de los alojamientos se ofertan por una estancia mínima de menor a las 10 noches, sin embargo aún
                existen cerca de 2000 alojamientos, cuya oferta es para una larga estancia, lo cual parece poco apropiado
                para una estadía de vacaciones. Entre éstas hay unos 1500 alojamientos cuya estancia mínima supera los 20 dias,
                por lo que estaríamos hablando mínimo de un alquiler mensual. Al hacerlo a traves de la plataforma, existe cierta
                garantía, pero sin pasar por un contrato legal de alquiler.\n
                - Tan sólo un 41,7% de los anfitriones, tienen sólo una oferta activa. Es decir, más de la mitad de las personas que
                ofertan sus alojamientos, tienen al menos 2 o más alojamientos ofertados, por lo que se puede deducir que para estas
                personas, ésta actividad constituye un negocio.\n
                - Por último, el 86,68% de los alojamientos ofertados, o lo que es lo mismo, casi 18000 de los casi 21000 alojamientos
                ofertados en la plataforma NO disponen de licencia de alojamiento turístico, por lo que el control existente por
                parte de las autoridades, sobre este negocio, es prácticamente nulo.

            """)