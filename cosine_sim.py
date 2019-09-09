import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def recommendations(title):
    df = pd.read_csv('Movies.csv')

    df = df[['Title','Genre','Director','Actors','Plot']]

    # discarding the commas between the actors' full names and getting only the first three names
    df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])

    # putting the genres in a list of words
    df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))

    df['Director'] = df['Director'].map(lambda x: x.split(' '))

    # merging together first and last name for each actor and director, so it's considered as one word 
    # and there is no mix up between people sharing a first name
    for index, row in df.iterrows():
        row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
        row['Director'] = ''.join(row['Director']).lower()

    #making a new column for relevant keywords
    df['Key_words'] = ""

    for index, row in df.iterrows():
    	plot = row['Plot']

    	#Using Rake for discarding all punctuations and for using English stopwords
    	r = Rake()
    	r.extract_keywords_from_text(plot)
    	key_words_dict_scores = r.get_word_degrees()

    	row['Ket_words'] = list(key_words_dict_scores.keys()) 
    df.drop(columns = ['Plot'], inplace = True)

    df.set_index('Title', inplace = True)
    df['bag_of_words'] = ''
    columns = df.columns
    for index, row in df.iterrows():
        words = ''
        for col in columns:
            if col != 'Director':
                words = words + ' '.join(row[col])+ ' '
            else:
                words = words + row[col]+ ' '
        row['bag_of_words'] = words
        
    df.drop(columns = [col for col in df.columns if col!= 'bag_of_words'], inplace = True)

    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])

    # creating a Series for the movie titles so they are associated to an ordered numerical
    # list I will use later to match the indexes
    indices = pd.Series(df.index)
    indices[:5]


    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    recommended_movies = []
        
        # gettin the index of the movie that matches the title
    idx = indices[indices == title].index[0]

        # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

        # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
        
        # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
            recommended_movies.append(list(df.index)[i])    
            
    return recommended_movies