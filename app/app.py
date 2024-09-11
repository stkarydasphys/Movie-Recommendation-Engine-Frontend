import streamlit as st
import requests
import random
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

good_comments = [
    "Yeah, that movie was good!",
    "Awesome!",
    "Loved it!",
    "Hey, we should be friends!",
    "Niiice!",
    "I've seen better but hey, whatever floats your boat, amirite?",
    "No way, that's my favorite!",
    "OK!",
    "Oh right, that's the one with that guy that starred in that other movie right?",
    "Seriously?",
    "Good one.",
    "Not a fan, but hey, whatevz!",
    "Good!",
    "Classic!"
]

average_comments = [
    "Meh, didn't like it either.",
    "Yeah, no!",
    "Pffft! Seen better...",
    "Yeah, makes sense.",
    "Aww, you didn't like that?",
    "Oh come on!",
    "Got you.",
    "Not that bad, come on!",
    "Well, i liked it...",
    "Haven't seen it",
    "LOL yeah.",
    "I see."
]

# function commenting on user's ratings
def comment(rating):
    if rating >= 4.0:
        return random.choice(good_comments)
    elif rating > 1:
        return random.choice(average_comments)
    else:
        return "Ouch!"





##### INPUT PAGE #####

def input_page():
    st.title("Welcome to **Movie Recommendation Engine**! ")

    # markdown for the welcome text
    st.markdown(
    """
    ## Hello! Let me introduce myself, I am MRE, your Deep Learning powered Movie Recommendation Engine.
    """,
    unsafe_allow_html=True
    )

    # user input
    user_id_input = st.number_input("And who might you be? (User ID)",
                                min_value = 0,
                                max_value = 2000,
                                step = 1)

    movie_suggestions = st.slider('How many movies would you like me to suggest?', 1, 15, 1)

    # button that triggers history to appear
    if st.button("Your Rating History"):
        # API call to fetch the user's history based on their user ID
        api_url = "https://movie-recommendation-engine-image-194144152402.europe-west1.run.app/predict"
        params = {"user_id": int(user_id_input), "top_n": int(movie_suggestions)}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            titles, tmdb_ids, history_titles, history_tmdb_ids, history_ratings = response.json()

            if len(history_titles) > 10:
                st.markdown(
                f"""
                ### Your rating history looks interesting! You have rated {len(history_titles)} movies! Let's see some of them:
                """,
                unsafe_allow_html=True
                )

                for index in range(10):
                    st.markdown(f'''
                                You watched <span style="font-size:20px; font-weight:bold;">{history_titles[index]}</span>
                                and rated it <span style="font-size:20px; font-weight:bold;">{history_ratings[index]}/5.0</span>.
                                <br>
                                <span style="font-size:14px;">"{comment(history_ratings[index])}"</span>
                            ''', unsafe_allow_html=True)


                st.markdown("""<p style="font-size:26px;">OK, great, I got you! Let's see my suggestions according to your history</p>""", unsafe_allow_html=True)

            elif len(history_titles) > 1:
                st.markdown(
                f"""
                ### You have only rated {len(history_titles)} movies! Let's see them:
                """,
                unsafe_allow_html=True
                )
                for index in range(len(history_titles)):
                    st.write(f"You watched {history_titles[index]} and rated it {history_ratings[index]}/5.0")

                st.markdown("""<p style="font-size:24px;">Your rating history is rather small, but hey don't worry, I got you covered! Let's see my suggestions:</p>""", unsafe_allow_html=True)

            else:
                st.markdown(
                f"""
                ### Aaah you must be new around here, you have not rated any movies! Alright, let's see some suggestions to get you started:
                """,
                unsafe_allow_html=True
                )

        else:
            st.write(f"OOPS! Something went wrong! Error code: {response.status_code}")

    # if st.session_state.user_id and st.session_state.num_recommendations:
    #     st.session_state.page = "recommendations"


    if st.button("Are you ready?"):
        # store user input in session state
        st.session_state.user_id = user_id_input
        st.session_state.num_recommendations = movie_suggestions

        # force an update by setting a dummy value in the session state
        st.session_state["trigger"] = not st.session_state.get("trigger", False)

        # switch to recommendations page
        st.session_state.page = "recommendations"

        if st.button("Let's see some recommendations!"):
            st.session_state.page = "recommendations"






##### RECOMMENDATIONS PAGE #####

def recommendations_page():
    st.title("Alright, let's watch some movies!")

    # retrieve user input from session state
    user_id = st.session_state.get("user_id", 0)
    num_recommendations = st.session_state.get("num_recommendations", 0)

    # API call to predict
    api_url = "https://movie-recommendation-engine-image-194144152402.europe-west1.run.app/predict"
    params = {"user_id": int(user_id),
               "top_n": int(num_recommendations)}
    response = requests.get(api_url, params=params)

    # TMDB API key
    API_key = os.getenv("TMDB_API_KEY")       # this is for local use
#    API_key = st.secrets["TMDB_API_KEY"]    # this is for the streamlit cloud app








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
        font-size: 18px;  /* Font size */
        margin-top: 10px;
        color: white;
    }
    .runtime, .genres, .score {
        font-size: 14px;  /* Font size */
        margin-top: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)










    # our predictions
    if response.status_code == 200:
        titles, tmdb_ids, history_titles, history_tmdb_ids, history_ratings = response.json()

        for idx, movie in enumerate(titles):
            # Create a transparent tile for each recommendation
            st.markdown(f'<div class="recommendation-tile">', unsafe_allow_html=True)

            with st.container():
                col1, col2 = st.columns([1, 2])  # adjusting width ratio

                # poster column
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
                        st.image(full_poster_url, width=250)  # poster width
                    else:
                        st.image("fallback_image_url", width=250)  # fallback image

                    st.markdown('</div>', unsafe_allow_html=True)

                # movie details column
                with col2:
                    st.markdown('<div class="details">', unsafe_allow_html=True)

                    # movie details
                    tmdb_url_details = f"https://api.themoviedb.org/3/movie/{tmdb_ids[idx]}?language=en-US"
                    tmdb_response_details = requests.get(tmdb_url_details, headers=headers)
                    tmdb_json = tmdb_response_details.json()

                    if tmdb_response_details.status_code == 200:
                        # transparent background applied only to the title!
                        st.markdown(f'<p class="movie-title">{movie}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="overview">{tmdb_json.get("overview", "No overview available.")}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="runtime">Runtime: {tmdb_json.get("runtime", "N/A")} minutes</p>', unsafe_allow_html=True)

                        # genres
                        genres = tmdb_json.get('genres', [])
                        genre_list = [genre["name"] for genre in genres]
                        genre_string = ", ".join(genre_list) if genre_list else "N/A"
                        st.markdown(f'<p class="genres">Genre(s): {genre_string}</p>', unsafe_allow_html=True)

                        # rating
                        st.markdown(f'<p class="score">Score on TMDB: {round(tmdb_json.get("vote_average", 0), 2)}/10 from {tmdb_json.get("vote_count", 0)} votes</p>', unsafe_allow_html=True)

                    else:
                        st.write("No Overview Available!")

                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)



    else:
        st.write(f"OOPS! Something went wrong!Error code:{response.status_code}")

    st.session_state.page = "input"

    # button to go back
    if st.button("Go back to user input"):
        # store user input in session state and switch to recommendations page
        st.session_state.page = "input"


##### PAGE HANDLING #####

if "page" not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    input_page()
else:
    recommendations_page()
