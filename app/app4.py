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
    ## Hello! Let me introduce myself, I am MRE, an AI powered Movie Recommendation Engine.
    """,
    unsafe_allow_html=True
    )

    # user input
    user_id_input = st.number_input("And who might you be? (User ID)",
                                min_value = 0,
                                max_value = 2000,
                                step = 1)

    movie_suggestions = st.slider('How many movies would you like me to suggest?', 1, 15, 1)

#   i use this to make the go back button to work on the first try, but for some reason it bugs some times
#   st.session_state.page = "recommendations"

    if st.button("Get Recommendations"):
        # store user input in session state and switch to recommendations page
        st.session_state.user_id = user_id_input
        st.session_state.num_recommendations = movie_suggestions
        st.session_state.page = "recommendations"




##### RECOMMENDATION PAGE #####

def recommendations_page():
    st.title("Alright, let me see what I can do for you...")

    # retrieve user input from session state
    user_id = st.session_state.get("user_id", "N/A")
    num_recommendations = st.session_state.get("num_recommendations", 0)

    # API call to predict
    api_url = "https://movie-recommendation-engine-image-194144152402.europe-west1.run.app/predict"
    params = {"user_id": int(user_id),
               "top_n": int(num_recommendations)}
    response = requests.get(api_url, params=params)

    # TMDB API key
    API_key = os.getenv("TMDB_API_KEY")       # this is for local use
#    API_key = st.secrets["TMDB_API_KEY"]    # this is for the streamlit cloud app



    # our predictions
    if response.status_code == 200:
        titles, tmdb_ids, history_titles, history_tmdb_ids, history_ratings = response.json()
        # creating columns for the posters
#        cols = st.columns(5)

#       no need for this,it is just the table of predictions
#        st.write(titles)


# rating history of user
        if len(history_titles) > 5:

            st.markdown(
            f"""
            ### Your rating history looks interesting! You have rated {len(history_titles)} movies! Let's see, some of them:
            """,
            unsafe_allow_html=True
            )

            for index in range(5):
                st.write(f"You watched {history_titles[index]} and rated it {history_ratings[index]}/5.0")

            st.markdown('<p style="font-size:22px;">OK, great, I got you! According to these, here are my suggestions:</p>', unsafe_allow_html=True)

        elif len(history_titles) > 1:

            st.markdown(
            f"""
            ### You have only rated {len(history_titles)} movies! Let's see them:
            """,
            unsafe_allow_html=True
            )
            for index in range(len(history_titles)):
                st.write(f"You watched {history_titles[index]} and rated it {history_ratings[index]}/5.0")

            st.write("Your rating history is rather small, but hey don't worry, I got you covered! Here are my suggestions:")

        else:
            st.markdown(
            f"""
            ### Aaah you must be new around here, you have not rated any movies! Alright, here are some suggestions to get you started:
            """,
            unsafe_allow_html=True
            )


# suggestions
        for idx, movie in enumerate(titles):
            # creating two columns: one for the poster and one for the movie overview
            col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

            with col1:
                # API request to TMDB to fetch poster
                tmdb_url_image = f"https://api.themoviedb.org/3/movie/{tmdb_ids[idx]}/images?language=en"
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
                    # st.write(f"**{movie}**")  # vanilla streamlit movie title
                    st.markdown(f'<p style="font-size:30px; text-decoration:underline;">{movie}</p>', unsafe_allow_html=True)
                    st.write(f"Overview: {tmdb_json.get('overview')}")   # vanilla streamlit overview
                    # st.markdown(f'<p style="background-color:black;">Overview: {tmdb_json.get("overview")}</p>', unsafe_allow_html=True)   # overview with background
                    # st.markdown(f'''
                    #                 <div style="
                    #                     background-color: rgba(255, 255, 255, 0.1);  /* Semi-transparent background */
                    #                     backdrop-filter: blur(10px);  /* Blur effect */
                    #                     padding: 10px;  /* Some padding for better spacing */
                    #                     border-radius: 10px;  /* Optional: Rounded corners */
                    #                 ">
                    #                     <p style="font-size:18px; color:white;">Overview: {tmdb_json.get("overview")}</p>
                    #                 </div>
                    #             ''', unsafe_allow_html=True)
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
