import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import st_folium
import functions as ft 
from PIL import Image



ft.carga_datos()
st.set_page_config(page_title = "ANALISIS AT", page_icon=":house_with_garden:", layout="wide")

menu = st.sidebar.selectbox(
    'Elige una opción',
    ('Introducción', 'Hipótesis', 'Resolución', 'Conclusión'))

if menu == 'Introducción':
    ft.intro()

    tab1, tab2, tab3, tab4 = st.tabs(['Datos', 'Mapa de puntos', 'Mapa en colores', 'Mapa de calor'])

    with tab1:
    
        ft.analisis_intro()
        ft.conteo_distrito()
        ft.conteo_distrito2()

    with tab2:
        st.header("Mapa de puntos")
        st.map(ft.data, zoom= 8)  

    with tab3:
        st.header("Mapa coloreado")
        ft.color_map()

    with tab4:
        st.header("Mapa de Calor")
        ft.heat_map_mad()

elif menu == 'Hipótesis':
    ft.hipotesis()     

    tab1, tab2, tab3 = st.tabs(["Tipos de habitación", "Precio por capacidad y minimo de noches", "Precio por distrito"])     
    
    with tab1:
        st.header("Tipos de habitación")
        st.write("""
            En la siguiente gráfica podemos ver los tipos de habitación que se ofertan por distrito.
            """)
        ft.room_type()
        st.write("""
            Tal y como se puede apreciar en la gráfica, casi el total de tipos de habitación esta englobado
            por "Alojamientos enteros" o "Habitación Privada".\n
            Son muy pocos los anuncios enfocados a compartir habitación.
            """)

    with tab2:
        st.header("Precio por capacidad y minimo de noches")
        ft.precio_cap_noches()

    with tab3:
        st.header("Precio por distrito")
        ft.precio_promedio()


elif menu == 'Resolución':
    st.title('Existe economía sumergida en relación a los alojamientos turísticos')
    img = Image.open('neighbourhood.png')
    st.image(img,use_column_width="auto")

    tab1, tab2, tab3 = st.tabs(["Mínimo de noches por alojamiento", "Alojamientos por anfitrión", "Licencias Turísticas"])

    with tab1:
        st.header("Mínimo de noches por alojamiento")
        ft.min_noches()
        ft.min_noches2()

    with tab2:
        st.header("Alojamientos por anfitrión")
        st.write("""
            A continuación vamos a ver cuantos de los anfitriones tienen anunciado 1 o más alojamientos.
            """)
        ft.host_list()
        st.write("""
            Como podemos observar, aunque la mayoría de personas tiene un sòlo anuncio, éstos constituyen menos del 50\% de los mismos,
            por lo que ya desmontamos una parte de la teoría de la filosofía de "economía colaborativa".
            """)
        ft.host_list2()
        


    with tab3:
        st.header("Licencias Turísticas")
        ft.licencias2()
        st.write("""
            Cómo podemos ver, tanto en la tabla, como en la gráfica, tan sólo unos pocos alojamientos disponen de licencia turística.
            De hecho, son más del 85\% los que no disponen de la misma, por lo que aunque no podemos saber si estas personas pagan
            o no impuestos por el alquiler de estos inmuebles, si que sabemos que al menos no están controlados o sujetos de forma 
            directa al pago de ningún impuesto, ya que la única regulación que tienen es la que la plataforma Airbnb quiera hacer
            sobre ellos.
            """)
        ft.licencias()

else:
    ft.conclusion()

    
        
        
    









