import streamlit as st
import requests
import numpy as np
import pandas as pd


url_api ='http://0.0.0.0:8000/predict'

st.markdown("""# Anime Map
## This is a sub header
This is text

_______________
""")


anime_input = st.text_input('Give the name of an anime!"', value='Naruto')
predict_size_input = st.number_input('Size of desired prediction list', value=10)
model_input = st.selectbox(
       'Which model do you want to use?',
       ('notation', 'completed'))
params = {
    'anime' : anime_input,
    'length' : predict_size_input,
    'model' : model_input
}

response = requests.get(url_api, params=params).json()

prediction = response['prediction']

st.markdown(f'''
_______________

## You might want to watch these animes :
${prediction}
_______________
''')