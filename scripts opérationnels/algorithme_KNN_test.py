
import pandas as pd
import numpy as np

labeled_data = pd.read_csv('clean_donnees_cameras.csv')
data_to_classify = pd.read_csv('donnes_classifiees.csv')

# Define function to calculate the euclidean distance between two data points
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

# Define function to predict the weather conditions for unclassified data points
def predict_weather(data_to_classify, labeled_data, k):
    predicted_labels = []
    for i in range(len(data_to_classify)):
        distances = []
        for j in range(len(labeled_data)):
            dist = euclidean_distance(data_to_classify.iloc[i][['humidite', 'temperature', 'indice']].fillna(labeled_data[['humidite', 'temperature', 'indice']].mean()).values, labeled_data.iloc[j][['humidite', 'temperature', 'indice']].values)
            distances.append((dist, labeled_data.iloc[j]['weather']))
        distances = sorted(distances)[:k]
        labels = [label for (_, label) in distances]
        label = max(set(labels), key=labels.count)
        predicted_labels.append(label)
    return predicted_labels

# Predict the weather conditions for the data to be classified
k = 3
predicted_labels = predict_weather(data_to_classify, labeled_data, k)

# Convert numerical labels back to categorical labels
label_map = {0: 'Sunny', 1: 'Cloudy', 2: 'Foggy'}
predicted_labels = [label_map[label] for label in predicted_labels]

# Save predicted labels to CSV file
data_to_classify['weather'] = predicted_labels
data_to_classify.to_csv('predicted_weather.csv', index=False)

