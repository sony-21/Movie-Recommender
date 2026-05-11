import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

print("Loading data...")

movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

print("Merging data...")

df = movies.merge(ratings, on='movieId')

print("Creating pivot table...")

movie_pivot = df.pivot_table(index='title', columns='userId', values='rating')
movie_pivot.fillna(0, inplace=True)

print("Calculating similarity...")

similarity = cosine_similarity(movie_pivot)

print("Saving model...")

pickle.dump(similarity, open('models/similarity.pkl', 'wb'))
pickle.dump(movie_pivot.index.tolist(), open('models/movies_list.pkl', 'wb'))

print("✅ DONE! similarity.pkl created successfully")