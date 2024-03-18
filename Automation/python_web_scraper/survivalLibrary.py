import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdf(url, category):
    filename = url.split('/')[-1]
    os.makedirs(os.path.join("books", category), exist_ok=True)
    with open(os.path.join("books", category, filename), 'wb') as f:
        f.write(requests.get(url).content)
    print(f"Downloaded: {filename}")

def select_category(categories):
    print("Select a category:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category.text.strip()}")

    choice = int(input("Enter the number of the category: "))
    if choice < 1 or choice > len(categories):
        print("Invalid choice. Please select a valid category.")
        return select_category(categories)
    else:
        return categories[choice - 1]

url = 'https://www.survivorlibrary.com/library-download.html'     
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

category_links = soup.find_all('a', href=lambda href: href and href.startswith("/index.php/8-category"))

selected_category = select_category(category_links)

selected_category_url = urljoin(url, selected_category['href'])
selected_category_response = requests.get(selected_category_url)
selected_category_soup = BeautifulSoup(selected_category_response.content, 'html.parser')

library_links = selected_category_soup.find_all('a', href=lambda href: href and href.startswith("/library"))

for link in library_links:
    pdf_url = urljoin(selected_category_url, link['href'])
    download_pdf(pdf_url, selected_category.text.strip())
