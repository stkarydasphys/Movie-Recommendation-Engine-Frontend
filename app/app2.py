import streamlit as st
import requests


# background image
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

# Inject the custom CSS with the background image
st.markdown(background_image, unsafe_allow_html=True)




# markdown for the welcome text
st.markdown(
    """
    # **Movie Recommendation Engine**!

    ## World's Best Recommendation Engine as rated by me!
    """,
    unsafe_allow_html=True
)




# user input
user_id_input = st.number_input("Please insert your User ID",
                                min_value = 0,
                                max_value = 2000,
                                step = 1)





# initialize session state for movies
# it's a dictionary like object, it retains info without reloading the whole thing
if 'movies' not in st.session_state:
    st.session_state['movies'] = [{'title': '', 'rating': 0}]


# function to add a new movie field
def add_movie():
    st.session_state['movies'].append({'title': '', 'rating': 0})


# dynamic input fields using session state
for i, movie in enumerate(st.session_state['movies']):
    st.session_state['movies'][i]['title'] = st.text_input(f"Movie Title {i+1}", key=f"title_{i}")
    st.session_state['movies'][i]['rating'] = st.slider(f"Rating {i+1}", 0, 5, key=f"rating_{i}")


# Button to add more fields
if st.button("Add another movie"):
    add_movie()


movie_suggestions = st.slider('How many movies would you like MRE to suggest?', 1, 50, 10)


# recommendation button and API call
if st.button("Get Recommendations"):

    api_url = "https://movie-recommendation-engine-image-194144152402.europe-west1.run.app/predict"
    params = {"user_id": int(user_id_input),
              "top_n": int(movie_suggestions)}

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        predictions = response.json()
        st.write("Recommended Movies:")

        st.write(predictions)
    else:
        st.write(f"OOPS! Something went wrong!Error code:{response.status_code}")
