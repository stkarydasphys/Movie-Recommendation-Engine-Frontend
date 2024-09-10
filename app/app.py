import streamlit as st
import requests

import os
from dotenv import load_dotenv

load_dotenv()

# setting page width
# st.set_page_config(layout="wide")

# background image
background_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""

# injecting the custom CSS with the background image
st.markdown(background_image, unsafe_allow_html=True)


##### INPUT PAGE #####

def input_page():
    st.title("Welcome to **Movie Recommendation Engine**! ")

    # markdown for the welcome text
    st.markdown(
    """
    ## World's Best Recommendation Engine as rated by at least 3 Le Wagon students and their moms!
    """,
    unsafe_allow_html=True
    )

    # user input
    user_id_input = st.number_input("Please insert your User ID",
                                min_value = 0,
                                max_value = 2000,
                                step = 1)

    movie_suggestions = st.slider('How many movies would you like MRE to suggest?', 1, 10, 1)

#   i use this to make the go back button to work on the first try, but for some reason it bugs some times
#   st.session_state.page = "recommendations"

    if st.button("Get Recommendations"):
        # store user input in session state and switch to recommendations page
        st.session_state.user_id = user_id_input
        st.session_state.num_recommendations = movie_suggestions
        st.session_state.page = "recommendations"


##### RECOMMENDATION PAGE #####

def recommendations_page():
    st.title("Let's see what MRE has prepared for you!")

    # retrieve user input from session state
    user_id = st.session_state.get("user_id", "N/A")
    num_recommendations = st.session_state.get("num_recommendations", 0)

    # API call to predict
    api_url = "https://movie-recommendation-engine-image-194144152402.europe-west1.run.app/predict"
    params = {"user_id": int(user_id),
               "top_n": int(num_recommendations)}
    response = requests.get(api_url, params=params)

    # TMDB API key
    API_key = st.secrets["TMDB_API_KEY"]    # os.getenv("TMDB_API_KEY")

    # our predictions
    if response.status_code == 200:
        titles, tmdb_ids = response.json()
        # creating columns for the posters
#        cols = st.columns(5)

#       no need for this,it is just the table of predictions
#        st.write(titles)

        for idx, movie in enumerate(titles):
            # creating two columns: one for the poster and one for the movie overview
            col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

            with col1:
                # API request to TMDB to fetch poster
                tmdb_url_image = f"https://api.themoviedb.org/3/movie/{tmdb_ids[idx]}/images"
                headers = {
                            "accept": "application/json",
                            "Authorization": f"Bearer {API_key}"
                        }
                tmdb_response_image = requests.get(tmdb_url_image, headers=headers)

                if tmdb_response_image.status_code == 200:
                    image_data_tmdb = tmdb_response_image.json()
                    poster_path = image_data_tmdb["posters"][0]["file_path"]
                    base_url = "https://image.tmdb.org/t/p/w500"
                    full_poster_url = f"{base_url}{poster_path}"

                    st.image(full_poster_url, width=200)  # we can adjust the width as needed
                else:
                    st.image(background_url, width=200)  # fallback image if poster is not found, something cooler maybe?

            with col2:
                # API request to TMDB to fetch details
                tmdb_url_details = f"https://api.themoviedb.org/3/movie/{tmdb_ids[idx]}?language=en-US"
                headers = {
                            "accept": "application/json",
                            "Authorization": f"Bearer {API_key}"
                        }
                tmdb_response_details = requests.get(tmdb_url_details, headers=headers)
                tmdb_json = tmdb_response_details.json()

                if tmdb_response_details.status_code == 200:
                    st.write(f"**{movie}**")  # Movie title
                    st.write(f"Overview: {tmdb_json.get('overview')}")
                    st.write(f"Runtime: {tmdb_json.get('runtime')} minutes")

                    genre_list_temp = tmdb_json.get('genres')
                    genre_list = [genre.get("name") for genre in genre_list_temp]
                    genre_string = genre_list[0]
                    for genre in genre_list[1:]:
                        genre_string += "{}".format(", "+genre)

                    st.write(f"Genre(s): {genre_string}")

                    st.write(f"Score on TMDB: {round(tmdb_json.get('vote_average'),2)}/10 in {tmdb_json.get('vote_count')} votes!")
                else:
                    st.write("No Overview Available!")



    else:
        st.write(f"OOPS! Something went wrong!Error code:{response.status_code}")

    st.session_state.page = "input"

    # button to go back
    if st.button("Go back to user input"):
        # store user input in session state and switch to recommendations page
        st.session_state.page = "input"



# page displayed
if "page" not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    input_page()
else:
    recommendations_page()
