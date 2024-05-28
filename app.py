from flask import Flask, request, render_template
import pickle
import pandas as pd
import requests
import patsy 


app = Flask(__name__)

# Load movie data and similarity matrix
movies = pickle.load(open("model/movies_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

def fetch_poster(movie_id):
    #print("Movie ID:", movie_id)  # Debug print
    if movie_id is None:
        return None
    
    url = "https://api.themoviedb.org/3/movie/{}?api_key=44e9c3b1a15577876c0d00566c7521e1&language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer YOUR_BEARER_TOKEN"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return None
    else:
        return None
    pass

def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)),reverse=True , key= lambda x:x[1])[1:11]

    recommended_movies_name =[]
    recommended_movies_poster=[]

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_name.append(movies.iloc[i[0]].title)
        #fetch posters from API
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies_name , recommended_movies_poster



@app.route("/")
def home():
    """Home page route"""
    return render_template("index.html")


@app.route('/recommend', methods=['GET','POST'])
def recommends():
    movies_list = movies['title'].values
    status = False
    if request.method.lower() == 'post':
        if request.form:
            movie_name = request.form['movies']
            status=True
            recommended_movies_name , recommended_movies_poster = recommend(movie_name)
            return render_template('recommend.html',name=recommended_movies_name,poster = recommended_movies_poster,movie_list=movies_list,status=status)
    # If request method is not 'POST', return the template here
    return render_template('recommend.html',status=status,movie_list=movies_list)

@app.route('/about')
def about():
    """about page route"""
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
