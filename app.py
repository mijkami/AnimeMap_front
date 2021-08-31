import streamlit as st
import requests
import numpy as np
import pandas as pd

    
url_api ='http://0.0.0.0:8000/predict'

def convert_dict_to_list(dict):
    temp = []
    dictList = []
    for key, value in dict.items():
        temp = [key,value]
        dictList.append(temp)
    return dictList


st.markdown("""# Anime Map
## Machine-learning based recommendation system

_______________
""")



GENRE_CHOICES = {
    "Fullmetal Alchemist: Brotherhood": "Action",
    "Kimi no Na wa.": "Drama",
    "Toradora!": "Romance",
    "Fairy Tail": "Fantasy",
    "Cowboy Bebop": "Science-Fiction",
    "Tenkuu no Escaflowne": "Robots",
    "Aria the Animation": "Slice of Life"
    }

def format_func(option):
    return GENRE_CHOICES[option]

# first collapsible box for simple Genres recommendation
st.write("# Anime recommendations from Genres")
with st.expander("Click me to expand!"):
    form = st.form(key='my-form')
    genre_input = form.selectbox("Select option", options=list(GENRE_CHOICES.keys()), format_func=format_func)
    predict_size_input = form.number_input('Size of desired prediction list:', value=10)
    model_input = form.selectbox(
        'Model to use:',
        ('notation', 'completed'))

    params = {
        'anime' : genre_input,
        'length' : predict_size_input,
        'model' : model_input
    }

    response = requests.get(url_api, params=params).json()
    prediction_list = convert_dict_to_list(response['prediction'])
    prediction_list_names = [prediction_list[i][0] for i in range(len(prediction_list))]

    button_clicked = form.form_submit_button('Get Recommendations!')

    if button_clicked:
        st.markdown(f'''
            _______________

            ## You might want to watch these animes :
            ''')
        st.write("1 - " + genre_input)
        i = 2
        for row in prediction_list_names:
            st.write(f"{i} - " + row)
            i+=1

    else:
        st.write('Choose some options then click on "Get Recommendations!" button.')

# Second collapsible box for text-input related recommendations (use st.multiselect)
# https://docs.streamlit.io/en/stable/api.html
# https://docs.streamlit.io/en/stable/api.html
st.write("# Anime recommendations from Genres")
with st.expander("Click me to expand!"):
    form = st.form(key='my-form') 
    anime_input = st.selectbox(
           'Genre of anime to predict on:',
           ('Naruto', 'Bleach'))

    #anime_input = st.text_input('Name of the anime to predict on:', value='Naruto')

# st.markdown(f'''
# _______________

# ## You might want to watch these animes :
# {genre_input}
# {prediction_list_names}
# _______________
# ''')


CSS = """

..streamlit-expanderHeader {
    font-size: 40px;
}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)
