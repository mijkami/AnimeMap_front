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
Fill the cells and run them to get a recommendation!

_______________
""")


anime_input = st.text_input('Name of the anime to predict on:', value='Naruto')
predict_size_input = st.number_input('Size of desired prediction list:', value=10)
model_input = st.selectbox(
       'Model to use:',
       ('notation', 'completed'))
params = {
    'anime' : anime_input,
    'length' : predict_size_input,
    'model' : model_input
}

response = requests.get(url_api, params=params).json()



prediction_list = convert_dict_to_list(response['prediction'])
prediction_list_names = [prediction_list[i][0] for i in range(len(prediction_list))]

st.markdown(f'''
_______________

## You might want to watch these animes :
{prediction_list_names}
_______________
''')