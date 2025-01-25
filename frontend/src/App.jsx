import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import custom CSS for styling

function App() {
    const [movie, setMovie] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [rating, setRating] = useState(null);
    const [error, setError] = useState('');

    const fetchSuggestions = async (query) => {
        if (!query) {
            setSuggestions([]);
            return;
        }
        try {
            const response = await axios.get(`http://localhost:5000/suggestions?query=${query}`);
            setSuggestions(response.data.suggestions);
        } catch (err) {
            console.error('Error fetching suggestions:', err);
        }
    };

    const searchMovie = async () => {
        if (!movie) {
            setError('Please enter a movie name.');
            return;
        }
        try {
            setError('');
            const response = await axios.get(`http://localhost:5000/search?movie=${movie}`);
            setReviews(response.data.reviews);
            setRating(response.data.rating);
        } catch (err) {
            setError('Movie not found or an error occurred.');
            console.error(err);
        }
    };

    return (
        <div className="app">
            <div className="search-container">
                <h1 className="title">Movie Sentiment Analyzer</h1>
                <div className="search-box">
                    <input
                        type="text"
                        placeholder="Enter movie name"
                        value={movie}
                        onChange={(e) => {
                            const query = e.target.value;
                            setMovie(query);
                            fetchSuggestions(query); // Fetch suggestions dynamically
                        }}
                    />
                    <button onClick={searchMovie}>Search</button>
                </div>

                {/* Suggestions Dropdown */}
                {suggestions.length > 0 && (
                    <ul className="suggestions">
                        {suggestions.map((suggestion, index) => (
                            <li
                                key={index}
                                onClick={() => {
                                    setMovie(suggestion); // Set the clicked suggestion as input
                                    setSuggestions([]); // Clear suggestions
                                }}
                            >
                                {suggestion}
                            </li>
                        ))}
                    </ul>
                )}

                {error && <p className="error">{error}</p>}

                {rating !== null && <h2 className="rating">Overall Rating: {rating}/10</h2>}

                <div className="reviews">
                    <h3>Reviews:</h3>
                    <ul>
                        {reviews.map((review, index) => (
                            <li key={index}>
                                <p>{review.review}</p>
                                <strong>{review.sentiment}</strong>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default App;
