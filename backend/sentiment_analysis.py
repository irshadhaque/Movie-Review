import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_reviews(csv_file):
    df = pd.read_csv(csv_file)

    sid = SentimentIntensityAnalyzer()

    results = []
    compound_scores = []

    for review in df['Review']:
        scores = sid.polarity_scores(review)
        compound = scores['compound']
        compound_scores.append(compound)

        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        results.append({
            'review': review,
            'sentiment': sentiment,
            'compound_score': compound
        })

    # Calculate overall rating: average compound score scaled to 0–10
    if compound_scores:
        average_compound = sum(compound_scores) / len(compound_scores)
        overall_rating = round((average_compound + 1) * 5, 1)  # Maps -1:1 to 0:10
    else:
        overall_rating = 0.0

    return results, overall_rating
