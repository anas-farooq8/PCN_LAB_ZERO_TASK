import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import csv
import json

def getPage(url): # function to get the html of the scrapped page for readability
    response = req.get(url)
    if not response.ok:
        print("Server responded with exit code:", response.status_code) # if scrapping is not allowed
        return None
    else:
        soup = bsp(response.text, "lxml") # converting to html
        pretty = soup.prettify() # increasing readability
        with open('scrapped.html', mode='w', encoding='utf-8') as htmlFile:  # specify encoding method for writing in a file
            htmlFile.write(pretty)
        return soup


def findContent(soup, info): # function to extract the required elements from the website soup
    if soup is None: # if previous function returned none
        return
    
    # going from basic to specific
    ol = soup.find('div', id='srp-river-results') 
    articles = ol.find_all('div', class_='s-item__info clearfix')

    for article in articles:
        # extracting the title
        try:
            head = article.find('span', role='heading')
            title = head.text.strip()
            sub = 'New Listing'
            if sub in title:
                title = title.replace(sub, "")
            print(title)
            info['Title'].append(title)
        except:
            info['Title'].append(' ')


        # extracting the prices
        try:
            prices = article.find('span', class_='s-item__price')
            price = prices.text.strip() #if price_text.startswith('£') else 0.0
            print(price)
            info['Price'].append(price)
        except:
            info['Price'].append(' ')


        # extracting the ratings
        try:
            stars = article.find('div', class_='x-star-rating')
            star = stars.find('span', class_= 'clipped').text  # if len(stars['span']) > 1 else "No rating"
            print(star)
            info['Star-Rating'].append(star)
        except:
            info['Star-Rating'].append(' ')


        # extracting the sales
        try:
            avail = article.find('span', class_='s-item__dynamic s-item__quantitySold')
            availes = avail.find('span', class_ = 'BOLD')
            sales = availes.text.strip()
            print(sales)
            info['Sales'].append(sales)
        except:
            info['Sales'].append(' ')


        # extracting the status
        secondaries = article.find_all('div', class_='s-item__subtitle')
        for secondary in secondaries:
            try:
                extra = secondary.find('span', class_ = 'SECONDARY_INFO')
                status = extra.text.strip()
                print(status)
                info['Status'].append(status)   
            except:
                info['Status'].append(' ')
        

        # extracting the best-seller
        try:
            sell = article.find('span', class_='s-item__etrs')
            best = sell.find('span', class_ = 's-item__etrs-text')
            bestSeller = best.text.strip()
            print(bestSeller)
            info['Best-Seller'].append(bestSeller)
        except:
            info['Best-Seller'].append(' ')


        # extracting the ratings-count
        try:
            rates = article.find('span', {'aria-hidden' : 'false'})
            rating = rates.text.strip()
            print(rating)
            info['Ratings-Count'].append(rating)
        except:
            info['Ratings-Count'].append(' ')


        # extracting the author
        try:
            writing = article.find('div', class_ = 's-item__subtitle')
            author = writing.text.strip().split('|')[0]
            sub = 'by'
            if sub in author:
                info['Author'].append(author)
                print(author)
            else:
                info['Author'].append(' ')
        except:
            info['Author'].append(' ')







def main():  # the function in which all the functionality takes place
    info = { # uninitialized dictionary to use for later 
    'Title': [],
    'Price': [],
    'Star-Rating': [],
    'Sales': [],
    'Status' : [],
    'Best-Seller' : [],
    'Ratings-Count' : [],
    'Author' : []
    }

    for i in range(1, 170): # for all the fifty pages of the site
        url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Psychology+Books&_sacat=0&_pgn={i}'
        soup = getPage(url) # receiving the html element of the page
        findContent(soup, info) # finding and extracting required stuff

    # Write dictionary to CSV file
    csvFile = 'output.csv' # writing the headings of the columns
    with open(csvFile, mode='w', newline='', encoding='utf-8') as file: # using an encoder for special characters
        fieldnames = list(info.keys()) # typecasting the keys into a list
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(len(info['Title'])): # according to number of items, we are copying every value of every key into it's respective heading
            row = {
                'Title': info['Title'][i],
                'Price': info['Price'][i],
                'Star-Rating': info['Star-Rating'][i],
                'Sales': info['Sales'][i],
                'Status': info['Status'][i],
                'Best-Seller': info['Best-Seller'][i],
                'Ratings-Count': info['Ratings-Count'][i],
                'Author': info['Author'][i]
            }
            writer.writerow(row)


     # Write dictionary to JSON file
    json_file = 'scrapped.json'
    with open(json_file, mode='w', encoding='utf-8') as file:
        # Prepare list of dictionaries for JSON serialization
        json_data = []
        for i in range(len(info['Title'])): # according to number of items, we are copying every value of every key into it's respective heading
            row = {
                'Title': info['Title'][i],
                'Price': info['Price'][i],
                'Star-Rating': info['Star-Rating'][i],
                'Sales': info['Sales'][i],
                'Status': info['Status'][i],
                'Best-Seller': info['Best-Seller'][i],
                'Ratings-Count': info['Ratings-Count'][i],
                'Author': info['Author'][i]
            }
            json_data.append(row)
        
        # Write JSON data to file
        json.dump(json_data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()

