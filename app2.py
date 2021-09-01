import streamlit as st
from streamlit_tags import st_tags
import requests
import numpy as np
import pandas as pd

    
url_api ='http://0.0.0.0:8000/predict'
anime_df = pd.read_csv("data/anime_map_data_animelist_100plus_PG_anime_name_pivot_df.csv")
anime_names_list = anime_df["Name"].tolist()


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

keywords_input = st_tags(
label='# Enter the name of an anime:',
text='Press enter to add more',
value=['Cowboy Bebop'],
suggestions=anime_names_list,
maxtags = 1,
key='1'
)

# predict_size_input2 = form.number_input('Size of desired prediction list:', value=10)
params2 = {
    'anime' : keywords_input,
    'length' : 10,
    'model' : 'notation'
}

response2 = requests.get(url_api, params=params2).json()
prediction_list2 = convert_dict_to_list(response2['prediction'])
prediction_list_names2 = [prediction_list2[i][0] for i in range(len(prediction_list2))]

button_clicked_2 = st.button('Get Recommendations!')

if button_clicked_2:
    st.markdown(f'''
        _______________

        ## You might want to watch these animes :
        ''')
    i = 1
    for row in prediction_list_names2:
        st.write(f"{i} - " + row)
        i+=1

else:
    st.write('Choose some options then click on "Get Recommendations!" button.')
    #anime_input = st.text_input('Name of the anime to predict on:', value='Naruto')
