from flask import Flask, redirect, request, jsonify 
import os
from sentiment_analysis import analyze_reviews
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

# Route to handle dynamic movie name and redirect to /search
@app.route('/<movie_name>', methods=['GET'])
def redirect_to_search(movie_name):
    return redirect(f'/search?movie={movie_name}')

# Directory containin CSV files
DATA_DIR = "data"

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({'suggestions': []})

    # Getting list of CSV files in the data directory
    try:
        movie_files = [f.replace('.csv', '') for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    except FileNotFoundError:
        return jsonify({'error': 'Data directory not found'}), 500

    # Filter movie files that match the query
    suggestions = [movie for movie in movie_files if query in movie.lower()]
    return jsonify({'suggestions': suggestions})


# Route to handle movie search and sentiment analysis
@app.route('/search', methods=['GET'])
def search_movie():
    # Get the movie name from query parameters
    movie_name = request.args.get('movie')
    
    if not movie_name:
        return jsonify({'error': 'No movie name provided. Please provide a movie name as a query parameter.'}), 400

    # file path for the movie reviews CSV file
    file_name = f"data/{movie_name}.csv"

    # Check if the file exists
    if os.path.exists(file_name):
        results, rating = analyze_reviews(file_name)
        return jsonify({'reviews': results, 'rating': rating})
    else:
        return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
