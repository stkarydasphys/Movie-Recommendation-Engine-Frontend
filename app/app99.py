import streamlit as st
import requests

import os
from dotenv import load_dotenv



load_dotenv()

# setting page width
# st.set_page_config(layout="wide")

# background image
background_url = "https://images.unsplash.com/photo-1668890094751-6986d0ca9dfc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
# background_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1668890094751-6986d0ca9dfc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""

# injecting the custom CSS with the background image
st.markdown(background_image, unsafe_allow_html=True)



# changing the fonts with CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Anton', sans-serif;
        font-size: 20px;
        text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
    }
    </style>
    """, unsafe_allow_html=True)

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
    params = {"user_id": int(user_id), "top_n": int(num_recommendations)}
    response = requests.get(api_url, params=params)

    # TMDB API key
    API_key = st.secrets["TMDB_API_KEY"]    # os.getenv("TMDB_API_KEY")

    # CSS for improved layout and design
    st.markdown("""
    <style>
    .recommendation-tile {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        padding: 15px;
        margin: 20px 0;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        width: 100%;
        background-color: rgba(255, 255, 255, 0.3);  /* Transparent background for entire tile */
    }
    .poster {
        flex: 1;
        text-align: center;
    }
    .details {
        flex: 2;
        padding-left: 20px;
    }
    .movie-title {
        font-size: 22px;  /* Font size */
        font-weight: bold;
        text-align: left;  /* Aligned to the left */
        color: white;
        margin-bottom: 10px;
        padding: 5px;
        border-radius: 5px;
    }
    .overview {
        font-size: 14px;  /* Font size */
        margin-top: 10px;
        color: white;
    }
    .runtime, .genres, .score {
        font-size: 12px;  /* Font size */
        margin-top: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Our predictions
    if response.status_code == 200:
        titles, tmdb_ids = response.json()

        for idx, movie in enumerate(titles):
            # Create a transparent tile for each recommendation
            st.markdown(f'<div class="recommendation-tile">', unsafe_allow_html=True)

            with st.container():
                col1, col2 = st.columns([1, 2])  # Adjust width ratio

                # Poster column
                with col1:
                    st.markdown('<div class="poster">', unsafe_allow_html=True)

                    # API request to TMDB to fetch poster
                    tmdb_url_image = f"https://api.themoviedb.org/3/movie/{tmdb_ids[idx]}/images?language=en"
                    headers = {"accept": "application/json", "Authorization": f"Bearer {API_key}"}
                    tmdb_response_image = requests.get(tmdb_url_image, headers=headers)

                    if tmdb_response_image.status_code == 200:
                        image_data_tmdb = tmdb_response_image.json()
                        poster_path = image_data_tmdb["posters"][0]["file_path"]
                        base_url = "https://image.tmdb.org/t/p/w500"
                        full_poster_url = f"{base_url}{poster_path}"
                        st.image(full_poster_url, width=250)  # Poster width
                    else:
                        st.image("fallback_image_url", width=250)  # Fallback image

                    st.markdown('</div>', unsafe_allow_html=True)

                # Movie details column
                with col2:
                    st.markdown('<div class="details">', unsafe_allow_html=True)

                    # Fetch and display movie details
                    tmdb_url_details = f"https://api.themoviedb.org/3/movie/{tmdb_ids[idx]}?language=en-US"
                    tmdb_response_details = requests.get(tmdb_url_details, headers=headers)
                    tmdb_json = tmdb_response_details.json()

                    if tmdb_response_details.status_code == 200:
                        # Transparent background applied only to the title
                        st.markdown(f'<p class="movie-title">{movie}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="overview">{tmdb_json.get("overview", "No overview available.")}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="runtime">Runtime: {tmdb_json.get("runtime", "N/A")} minutes</p>', unsafe_allow_html=True)

                        # Display genres
                        genres = tmdb_json.get('genres', [])
                        genre_list = [genre["name"] for genre in genres]
                        genre_string = ", ".join(genre_list) if genre_list else "N/A"
                        st.markdown(f'<p class="genres">Genre(s): {genre_string}</p>', unsafe_allow_html=True)

                        # Display score
                        st.markdown(f'<p class="score">Score on TMDB: {round(tmdb_json.get("vote_average", 0), 2)}/10 from {tmdb_json.get("vote_count", 0)} votes</p>', unsafe_allow_html=True)

                    else:
                        st.write("No Overview Available!")

                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.write(f"OOPS! Something went wrong! Error code: {response.status_code}")

    st.session_state.page = "input"

    # Button to go back
    if st.button("Go back to user input"):
        st.session_state.page = "input"







# page displayed
if "page" not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    input_page()
else:
    recommendations_page()
