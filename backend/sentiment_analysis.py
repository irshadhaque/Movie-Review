import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_reviews(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Initialize the sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    results = []
    positive_count = 0
    negative_count = 0

    # Analyze each review
    for review in df['Review']:
        scores = sid.polarity_scores(review)
        sentiment = 'Positive' if scores['compound'] >= 0 else 'Negative'
        results.append({'review': review, 'sentiment': sentiment})

        if sentiment == 'Positive':
            positive_count += 1
        else:
            negative_count += 1

    # Calculate overall rating
    total_reviews = positive_count + negative_count
    overall_rating = (positive_count / total_reviews) * 10 if total_reviews > 0 else 0
    return results, round(overall_rating, 1)
