import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def CNN(csv):

    caminho_model = 'CNN.pkl'
    model = pickle.load(open(caminho_model, 'rb'))

    caminho_vectorizer = 'dtfidf.pkl'
    with open(caminho_vectorizer, 'rb') as file:
        tfidf_vectorizer = pickle.load(file)

    labels_mapping = {0: 'Negativo', 1: 'Neutro', 2: 'Positivo'}
    
    # Read CSV file into a DataFrame
    data = pd.read_csv(csv)
    
    # Drop columns with all NaN values
    data = data.dropna(axis=1, how='all')
    
    # Extract the 'opinion' column
    x = data['opinion'].values
    
    # Transform text data using TF-IDF vectorizer
    X_test_reviews = tfidf_vectorizer.transform(x)
    
    # Make predictions using the loaded model
    predictions = model.predict(X_test_reviews.toarray())
    predicted_labels = np.argmax(predictions, axis=1)
    predicted_sentiments = [labels_mapping[label] for label in predicted_labels]
    
    # Add columns to DataFrame
    data['sentiment'] = predicted_sentiments
    data['Negativo'] = predictions[:, 0]
    data['Negativo'] = [float('{:.2f}'.format(num)) for num in data['Negativo']]
    data['Neutro'] = predictions[:, 1]
    data['Neutro'] = [float('{:.2f}'.format(num)) for num in data['Neutro']]
    data['Positivo'] = predictions[:, 2]
    data['Positivo'] = [float('{:.2f}'.format(num)) for num in data['Positivo']]
    
    # Add columns for counts and total rows
    total_rows = len(data)
    positive_count = (predicted_labels == 2).sum()
    neutral_count = (predicted_labels == 1).sum()
    negative_count = (predicted_labels == 0).sum()
    
    data['Total Rows'] = total_rows
    data['Positive Count'] = positive_count
    data['Neutral Count'] = neutral_count
    data['Negative Count'] = negative_count
    
    # Save results to CSV file
    data.to_csv(csv, index=False)
