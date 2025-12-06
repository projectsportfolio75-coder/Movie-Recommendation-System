import pickle
import streamlit as st
import requests

# Load the saved model files
@st.cache_data
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommendation function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in distances[1:6]:
            # Fetch movie details
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_posters.append(fetch_poster(movie_id))
        
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return [], []

# Streamlit App UI
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Header
st.title('🎬 Movie Recommendation System')
st.markdown("---")

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations button
if st.button('Show Recommendation'):
    with st.spinner('Finding similar movies...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    if recommended_movie_names:
        st.markdown("### Recommended Movies")
        
        # Display movies in columns
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.image(recommended_movie_posters[idx], use_container_width=True)
                st.markdown(f"**{recommended_movie_names[idx]}**")
    else:
        st.error("Movie not found in the database. Please select a valid movie.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit | Data from TMDB</p>
    </div>
    """,
    unsafe_allow_html=True
)
