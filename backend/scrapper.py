# import requests
# from bs4 import BeautifulSoup
# import csv

# # URL of the IMDb movie reviews page
# url = 'https://www.imdb.com/title/tt3581920/reviews/?ref_=tt_ururv_sm'

# # Add headers to mimic a real browser
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # Send HTTP request to fetch the page
# response = requests.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find all review divs
#     reviews = soup.find_all('div', class_='ipc-html-content-inner-div')

#     # Open CSV file to save the reviews
#     with open('movie_reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Review'])  # Write header row
#         for review in reviews:
#             review_text = review.get_text(strip=True)
#             if review_text:  # Only write non-empty reviews
#                 writer.writerow([review_text])

#     print("Reviews have been saved to lastofus.csv")
# else:
#     print(f"Failed to retrieve page. Status code: {response.status_code}")
import requests
from bs4 import BeautifulSoup
import re

def fetch_imdb_reviews(movie_title, max_reviews=20):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    # Step 1: Search IMDb to get the movie ID
    search_url = f"https://www.imdb.com/find?q={movie_title.replace(' ', '+')}&s=tt&ttype=ft"
    search_response = requests.get(search_url, headers=headers)
    search_soup = BeautifulSoup(search_response.text, 'html.parser')
    
    first_result = search_soup.find('td', class_='result_text')
    if not first_result or not first_result.a:
        return {"error": "Movie not found on IMDb."}

    # Extract IMDb ID from the first result
    movie_path = first_result.a['href']
    imdb_id = re.search(r'/title/(tt\d+)/', movie_path).group(1)

    # Step 2: Scrape reviews using the IMDb ID
    review_url = f'https://www.imdb.com/title/{imdb_id}/reviews'
    review_response = requests.get(review_url, headers=headers)
    review_soup = BeautifulSoup(review_response.text, 'html.parser')

    review_divs = review_soup.find_all('div', class_='ipc-html-content-inner-div')
    reviews = [div.get_text(strip=True) for div in review_divs if div.get_text(strip=True)]

    # Return only the first N reviews
    return reviews[:max_reviews]
