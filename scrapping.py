from bs4 import BeautifulSoup
import requests
import pandas as pd

# getting the links of all the books on the main page
base_url = 'https://books.toscrape.com/'
url = 'https://books.toscrape.com/index.html'
catalog = requests.get(url).text
catalog_scrape = BeautifulSoup(catalog, 'html5lib')


links = []

for book_container in catalog_scrape.find_all('div', class_='image_container'):
    for link in book_container.find_all('a'):
        links.append(link.get('href'))

# now, we will store all the book title and prices
titles = []
prices = []
counter = 0

for link in links:
    url = base_url + link
    book_catalog = requests.get(url).text
    book_scrape = BeautifulSoup(book_catalog, 'html5lib')

    for div in book_scrape.find_all(class_='col-sm-6 product_main'):
        # book titles
        for childdiv in div.find_all('h1'):
            titles.append(childdiv.string)
        # book prices
        for childdiv in div.find_all('p', class_='price_color'):
            prices.append(childdiv.string)

        counter = counter+1
        print(f'{counter}/{len(links)} book(s) scrapped')


book_dataframe = pd.DataFrame({
    'titles': titles,
    'price': prices
})
print('web scrapping realizado com sucesso')
book_dataframe.to_excel('scraped_books.xlsx')
