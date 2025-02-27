#Error because in virtual library no packages are installed, so goto terminal and install with pip install streamlit
import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
import bz2
import os


#import py7zr
#import gdown




#Google Drive File IDs
#movies_dict_id = "1Aj5NYqHxOdsTyPICPBFo-rI_0Z8fdF3d"
#similarity_id = "1LvCo6TuwkLG1Hk_WYlTFN9h315ZuvUnE"
#KAGGLE_URL = ""

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3bb817c4c76ad683b0d62eafa2aba1d2'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # fetching indexes
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # Next we are printing the movies list
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

# Function to compress similarity.pkl to similarity.pkl.bz2
def compress_pkl(input_file, output_file):
    with open(input_file, "rb") as f:
        data = pickle.load(f)

    with bz2.BZ2File(output_file, "wb") as f:
        pickle.dump(data, f)

    print(f"Compression complete! Saved as {output_file}")

# Function to decompress similarity.pkl.bz2 to similarity.pkl
def decompress_pkl(compressed_file, output_file):
    if not os.path.exists(output_file):  # Only extract if missing
        with bz2.BZ2File(compressed_file, "rb") as f:
            data = pickle.load(f)

        with open(output_file, "wb") as f:
            pickle.dump(data, f)

        print(f"Decompression complete! Saved as {output_file}")
    else:
        print(f"{output_file} already exists. Skipping decompression.")

# File paths
compressed_file = "similarity.pkl.bz2"
output_file = "similarity.pkl"

# Decompress if needed
decompress_pkl(compressed_file, output_file)

# Load the decompressed similarity.pkl
with open(output_file, "rb") as f:
    similarity = pickle.load(f)

# Load similarity.pkl
#similarity = pickle.load(open("similarity.pkl", "rb"))

# Download both files
#download_file(movies_dict_id, "movies_dict.pkl")
#download_from_kaggle(similarity_id, "similarity.pkl")

# Load the files normally
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
#similarity = pickle.load(open("similarity.pkl", "rb"))

#movies_list_web = pickle.load(open('movies.pkl', 'rb'))
#movies = movies_list_web['title'].values


#similarity = pickle.load(open('similarity.pkl', 'rb'))
#pickle.dump(similarity,open("similarity.pkl", "wb"))

st.title('Movie Recommender System')  #In terminal give streamlit run app.py. It will open the title in webpage

selected_movie_name = st.selectbox(
    "Select a movie to know its recommendations!",
       movies['title'].values
)



if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])



    #for i in names:
      #  st.write(i)
#Now we want movies poster

# We need 4 files
# 1. Procfile --->web: sh setup.sh && streamlit run app.py
# 2. setup.sh //shell script
# 3. .gitignore ----->venv
# 4. in Terminal give---> pip freeze > requirements.txt ----->The libraries required for this app to be installed
# 5. Goto Heroku

#I have deployed in Streamlit community loud
# https://movie-recommender-system-external.streamlit.app/