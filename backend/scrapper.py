import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.imdb.com/title/tt3581920/reviews/?ref_=tt_ururv_sm'

# Add headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    reviews = soup.find_all('div', class_='ipc-html-content-inner-div')

    with open('movie_reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Review'])
        for review in reviews:
            review_text = review.get_text(strip=True)
            if review_text:
                writer.writerow([review_text])

    print("Reviews have been saved to lastofus.csv")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
