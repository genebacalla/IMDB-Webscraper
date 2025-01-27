import pandas as pd
import numpy as np

# Load datasets
movies_basics_dataset = pd.read_csv("G:/GCASH/dataset/title.basics.tsv", sep='\t', encoding='utf-8')
movies_rating_dataset = pd.read_csv("G:/GCASH/dataset/title.ratings.tsv", sep='\t', encoding='utf-8')

# Filter for 'movie' titleType
movie_basics_dataframe = movies_basics_dataset[movies_basics_dataset['titleType'] == 'movie']

# Drop unnecessary columns
movie_basics_dataframe = movie_basics_dataframe.drop(columns=['endYear', 'originalTitle', 'isAdult', 'titleType', 'runtimeMinutes'])

# Convert 'startYear' to numeric and handle errors
movie_basics_dataframe['startYear'] = pd.to_numeric(movie_basics_dataframe['startYear'], errors='coerce')

# Filter rows for 'startYear' between 2014 and 2024
movie_basics_dataframe = movie_basics_dataframe[(movie_basics_dataframe['startYear'] >= 2014) & (movie_basics_dataframe['startYear'] <= 2024)]

# Replace '\\N' with None
movie_basics_dataframe = movie_basics_dataframe.replace('\\N', None)

# Drop rows with any NaN values
movie_basics_dataframe = movie_basics_dataframe.dropna(how='any')

# Merge with ratings dataset
movie_basics_dataframe = pd.merge(movie_basics_dataframe, movies_rating_dataset[['tconst', 'averageRating', 'numVotes']], on='tconst', how='left')

# Drop rows where all cells are empty or contain only whitespace
movie_basics_dataframe = movie_basics_dataframe.replace('', None)

movie_basics_dataframe = movie_basics_dataframe.dropna(how='any')

# Save the cleaned data to a file
movie_basics_dataframe.to_csv('title.basics.tsv', sep='\t', index=False)
