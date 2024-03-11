import time
import requests
import re
from googlesearch import search
from bs4 import BeautifulSoup
from urllib.error import HTTPError

# Replace the URL with your Anilist user's animelist URL
url = "https://anilist.co/user/MuuuSia/animelist"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all div elements with class "entry row"
entries = soup.find_all('div', class_='entry row')

# Open the Markdown file in append mode
with open('index.md', 'w', encoding='utf-8') as file:
    # Loop through each entry and extract title, score, image URL, and description
    for entry in entries:
        title = entry.find('div', class_='title').text.strip()
        score = entry.find('div', class_='score').text.strip()

        # Find the div with class "image" and get the image URL
        image_div = entry.find('div', class_='image')
        style_attribute = image_div['style']
        url_match = re.search(r'url\(([^"]+)\)', style_attribute) if image_div else "No image available."
        image_url = url_match.group(1)
        print(image_url)

        # Get the URL of the anime page to extract the description
        anime_url = entry.find('div', class_='title').find('a')['href']
        anime_page = requests.get(f"https://anilist.co{anime_url}")
        anime_soup = BeautifulSoup(anime_page.content, 'html.parser')

        # Find the div with class "description"
        description_div = anime_soup.find('p', class_='description')
        description = description_div.text.strip() if description_div else "No description available."

        # Write the entry to the Markdown file with title, image, score, and description
        file.write(f"## {title}\n")
        file.write(f"**Score:** {score}\n\n")
        file.write(f"![{title}]({image_url})\n\n")
        file.write(f"**Description:** {description}\n\n")

        # Search for anime reviews on Google and get the first 3 results
        search_query = f"{title} anime reviews"
        search_results = search(search_query, num=3, stop=3, pause=5)

        subpage_filename = f"{title}_reviews.md"

        with open(subpage_filename, 'w', encoding='utf-8') as subpage_file:
            subpage_file.write(f"# Google Search Results for {title} anime reviews\n")
            for result in search_results:
                print("jej!")
                subpage_file.write(f"[{result}]({result})")
                subpage_file.write(f"\n\n")
                time.sleep(5)

        file.write(f"**Reviews from Google:** [Link to Google Search Results]({subpage_filename})\n\n")

print("Successfully scraped and appended to anime_list.md")
