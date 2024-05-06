def recommend(movie):
    """Function to recommend similar movies"""
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i].movie_id
        recommended_movies_name.append(movies.iloc[i].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies_name, recommended_movies_poster

    ////
def recommends():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
            try:
                if request.from_values:
                    movie_name = request.form['movies']
                    recommended_movies_name, recommended_movies_poster = recommend(movie_name)
                    status = True
                    return render_template('recommend.html', recommended_movies_name=recommended_movies_name,
                               recommended_movies_poster=recommended_movies_poster, movie_list=movie_list, status=status)
            except Exception as e :
                error = {'error':e}
                return render_template('recommend.html',status=status,error=error,movie_list=movie_list)
    else:
        return render_template('recommend.html', movie_list = movie_list,status=status)