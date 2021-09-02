import streamlit as st
from streamlit_tags import st_tags
import requests
import numpy as np
import pandas as pd

#local_url:
# url_api ='http://0.0.0.0:8000/predict'

#gcc api_url:
url_api ='https://animemapapi-kmovigytdq-ey.a.run.app/predict'

anime_df = pd.read_csv("data/anime_map_data_animelist_100plus_PG_anime_name_pivot_df.csv")
# anime_names = anime_df['Name']
anime_names_list = anime_df["Name"].tolist()
anime_names_list_lower = [name.lower() for name in anime_names_list]

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
st.write("### Anime recommendations from Genres")
with st.expander("Click me to expand!"):
    form = st.form(key='my-form')
    genre_input = form.selectbox("Select option", options=list(GENRE_CHOICES.keys()), format_func=format_func)
    predict_size_input = form.number_input('Size of desired prediction list:', value=10)
    model_input = form.selectbox(
        'Model to use:',
        ('notation', 'completed'))

    button_clicked = form.form_submit_button('Get Recommendations!')

    if button_clicked:
        params = {
            'anime' : genre_input,
            'length' : predict_size_input,
            'model' : model_input
        }

        response = requests.get(url_api, params=params).json()
        prediction_list = convert_dict_to_list(response['prediction'])
        prediction_list_names = [prediction_list[i][0] for i in range(len(prediction_list))]
        st.markdown(f'''
            _______________

            #### You might want to watch these animes :
            ''')
        st.write("1 - " + genre_input)
        i = 2
        for row in prediction_list_names:
            st.write(f"{i} - " + row)
            i+=1

    else:
         st.markdown(f'''
            How to use:
            
            1. pick an anime genre
            2. **(optional)** pick the desired number of recommendations generated from your choice
            3. **(optional)** pick the desired model used to generate the recommendations
            4. hit the 'Get Recommendations!' button
            5. profit!
            ''')

# Second collapsible box for text-input related recommendations (use st.multiselect)
# https://docs.streamlit.io/en/stable/api.html
# https://docs.streamlit.io/en/stable/api.html

st.write("### Anime recommendations from Title")
with st.expander("Click me to expand!"):
    keywords_input = st_tags(
    label='##### Enter the name of an anime:',
    text="Write here and use the auto-correction system.",
    # value=['Cowboy bebop'],
    suggestions=anime_names_list,
    maxtags = 1,
    key='1'
    )
    
    predict_size_input_word = st.number_input('Size of desired prediction list:', value=10)
    # predict_size_input2 = form.number_input('Size of desired prediction list:', value=10)

    button_input_word = st.button('Get Recommendations!')

    if button_input_word:
        if keywords_input != []:
            # keywords_input_word = keywords_input[0].replace(keywords_input[0][0], keywords_input[0][0].upper(), 1)
            keywords_input_word = keywords_input[0].lower()
            keywords_input_lower = [keywords_input_word]
            # st.write(keywords_input)
            # anime_names_list_lower
        else:
            keywords_input_lower = keywords_input

        if keywords_input_lower == []:
            st.markdown("""
                    ### Your input was empty!
                    #### It should look like this after hitting enter:
                    """)
            st.image('data/images/keyword_input_example_valid_tag.png')
        elif keywords_input_lower[0] not in anime_names_list_lower:
            st.markdown("""
                    ### This anime name is not in our anime list!
                    #### 1. The name should be similar to those from [MyAnimeList](https://myanimelist.net/topanime.php)
                    #### 2. Please try to use the names given by the auto-completion. 
                    #### 3. Hit the TAB button to select quickly auto-completed text.

                    
                    _______________
                    """)
            st.write('Autocompletion looks like this:')
            st.image('data/images/keyword_input_example_autocompletion.png')
        else:
            params_text_input = {
            # get the correct name from the initial list (used by model) 
            # at the same index than the lower_case name in the lower_case_list (used by website text verification)
            'anime' : anime_names_list[anime_names_list_lower.index(keywords_input_lower[0])],
            'length' : predict_size_input_word,
            'model' : 'notation'
            }

            response_text_input = requests.get(url_api, params=params_text_input).json()
            prediction_list_text_input = convert_dict_to_list(response_text_input['prediction'])
            prediction_list_names_text_input = [prediction_list_text_input[i][0] for i in range(len(prediction_list_text_input))]

            #TODO: show the list result as thumbnails for each anime
            st.markdown(f'''
                _______________

                #### You might want to watch these animes :
                ''')
            i = 1
            for row in prediction_list_names_text_input:
                st.write(f"{i} - " + row)
                i+=1

    else:
        st.markdown(f'''
            How to use:

            1. find an anime name (from [MyAnimeList](https://myanimelist.net/topanime.php))
            2. write it down in the form with the help of auto-completion
            3. hit "enter" to validate your choice (unique choice for now)
            4. hit the 'Get Recommendations!' button
            5. profit!
            ''')
        #anime_input = st.text_input('Name of the anime to predict on:', value='Naruto')




#TODO: add flexbox support
#TODO: add styling : title size, add images
CSS = """
h1 {
    font-size: 110px;
}

h2 {
    font-size: 40px;
    text-align: end;
}

h3 {
    font-size: 27px;
}

h4 {
    font-size: 20px;
}

h5 {
    font-size: 16px;
}

.streamlit-expanderHeader {
    font-size: 16px;
}

.block-container {
    margin-top:-100px;
}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)
