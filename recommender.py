import pickle

# Load trained model
similarity = pickle.load(open('models/similarity.pkl', 'rb'))
movies_list = pickle.load(open('models/movies_list.pkl', 'rb'))

def recommend(movie_name):
    if movie_name not in movies_list:
        return []

    index = movies_list.index(movie_name)
    distances = similarity[index]

    movies = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies_list[i[0]] for i in movies]