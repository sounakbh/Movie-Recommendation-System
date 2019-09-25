import numpy as np
import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def getMovies(title):
    df = pd.read_csv('Movies.csv')
    
    #taking title, genre,plot and actors for recommendation process
    df = df[['Title','Genre','Director','Actors','Plot']]

    # cleaning the 3 columns and bringing it to shape
    df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
    df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))
    df['Director'] = df['Director'].map(lambda x: x.split(' '))

    # merging first and last name to avoid duplicates
    for index, row in df.iterrows():
        row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
        row['Director'] = ''.join(row['Director']).lower()

    df['Key_words'] = ""

    for index, row in df.iterrows():
        #extracting all unique words from every row and adding to key_words column
    	plot = row['Plot']
    	r = Rake()
    	r.extract_keywords_from_text(plot)
    	keywordScores = r.get_word_degrees()
    	row['Key_words'] = list(keywordScores.keys()) 

    df.drop(columns = ['Plot'], inplace = True)

    df.set_index('Title', inplace = True)
    df['bag_of_words'] = ''
    columns = df.columns

    for index, row in df.iterrows():
        #creating a BOG model with actor, director, title, plot
        words = ''
        for col in columns:
            if col != 'Director':
                words = words + ' '.join(row[col]) + ' '
            else:
                words = words + row[col] + ' '
        row['bag_of_words'] = words
        
    df.drop(columns = [col for col in df.columns if col != 'bag_of_words'], inplace = True)

    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])
    titleIndex = pd.Series(df.index)
    titleIndex[:5]

    #generating the cosine similarity matrix
    cosineSimilarityMatrix = cosine_similarity(count_matrix, count_matrix)
    finalSelections = []

    #finding the row where the desired movie is located and taking the highest valus excluding the unit value
    idx = titleIndex[titleIndex == title].index[0]
    scoreSeries = pd.Series(cosineSimilarityMatrix[idx]).sort_values(ascending = False)
    topMovies = list(scoreSeries.iloc[1:11].index)
        
    #appending the recommendations in a list
    for i in topMovies:
        finalSelections.append(list(df.index)[i])    
            
    return finalSelections