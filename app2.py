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


with st.expander("Click me to expand!"):
    keywords_input = st_tags(
    label='# Enter the name of an anime:',
    text='Find an anime name, hit enter and the button!',
    # value=['Cowboy bebop'],
    suggestions=anime_names_list,
    maxtags = 1,
    key='1'
    )
    predict_size_input_word = st.number_input('Size of desired prediction list:', value=10)
    # predict_size_input2 = form.number_input('Size of desired prediction list:', value=10)

    button_clicked_2 = st.button('Get Recommendations!')

    if button_clicked_2:
        if keywords_input != []:
            keywords_input_word = keywords_input[0].replace(keywords_input[0][0], keywords_input[0][0].upper(), 1)
            keywords_input = [keywords_input_word]
            # st.write(keywords_input)
        

        if keywords_input == []:
            st.markdown("""
                    ### Your input was empty!
                    #### It should look like this after hitting enter:
                    """)
            st.image('data/images/keyword_input_example_valid_tag.png')
        elif keywords_input[0] not in anime_names_list:
            st.markdown("""
                    ### This anime name is not in our anime list!
                    #### 1. The name should be similar than the ones on [MyAnimeList](https://myanimelist.net/topanime.php)
                    #### 2. Please try to use the names given by the auto-completion. 
                    #### 3. Hit the TAB button to select quickly auto-completed text.

                    
                    _______________
                    """)
            st.write('Autocompletion looks like this:')
            st.image('data/images/keyword_input_example_autocompletion.png')
        else:
            params_text_input = {
            'anime' : keywords_input,
            'length' : predict_size_input_word,
            'model' : 'notation'
            }

            response_text_input = requests.get(url_api, params=params_text_input).json()
            prediction_list_text_input = convert_dict_to_list(response_text_input['prediction'])
            prediction_list_names_text_input = [prediction_list_text_input[i][0] for i in range(len(prediction_list_text_input))]

            st.markdown(f'''
                _______________

                ## You might want to watch these animes :
                ''')
            i = 1
            for row in prediction_list_names_text_input:
                st.write(f"{i} - " + row)
                i+=1

    else:
        st.write('Make sure to hit "Enter" after finding your anime name accordingly to the existing names')
        #anime_input = st.text_input('Name of the anime to predict on:', value='Naruto')
