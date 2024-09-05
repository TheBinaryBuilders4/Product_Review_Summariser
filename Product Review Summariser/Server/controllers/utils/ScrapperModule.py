# Import packages
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Scrapper:
    async def scrap_reviews(self, reviews_url):
        if 'amazon' in reviews_url:
            return await self.amazon(reviews_url)
        elif 'flipkart' in reviews_url:
            return await self.flipkart(reviews_url)
        else:
            return None


    async def amazon(self, reviews_url):
        # Header to set the requests as a browser requests
        headers = {
            'authority': 'www.amazon.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

        # Define Page No
        len_page = 4

        # Extra Data as Html object from amazon Review page
        async def reviewsHtml(url, len_page):

            # Empty List define to store all pages html data
            soups = []

            # Loop for gather all 3000 reviews from 300 pages via range
            for page_no in range(1, len_page + 1):

                # parameter set as page no to the requests body
                params = {
                    'ie': 'UTF8',
                    'reviewerType': 'all_reviews',
                    'filterByStar': 'critical',
                    'pageNumber': page_no,
                }

                # Request make for each page
                try:
                    response = requests.get(url, headers=headers, params=params)
                except Exception as e:
                    print('Error in Request', e)
                    return None

                # Save Html object by using BeautifulSoup4 and lxml parser
                soup = BeautifulSoup(response.text, 'lxml')

                # Add single Html page data in master soups list
                soups.append(soup)

            return soups


        # Grab Reviews name, description, date, stars, title from HTML
        async def getReviews(html_data):

            # Create Empty list to Hold all data
            data_dicts = []

            # Select all Reviews BOX html using css selector
            boxes = html_data.select('div[data-hook="review"]')

            # Iterate all Reviews BOX
            for box in boxes:
                try:
                    description = box.select_one('[data-hook="review-body"]').text.strip()
                except Exception as e:
                    description = 'N/A'

                # create Dictionary with al review data
                data_dict = {
                    'Description' : description
                }

                # Add Dictionary in master empty List
                data_dicts.append(data_dict)

            return data_dicts

        ### <font color="red">Data Process</font>

        print(f"Scraping Reviews from {reviews_url} ...")
        # Grab all HTML
        html_datas = await reviewsHtml(reviews_url, len_page)

        # Empty List to Hold all reviews data
        reviews = []

        # Iterate all Html page
        for html_data in html_datas:

            # Grab review data
            review = await getReviews(html_data)

            # add review data in reviews empty list
            reviews += review

        # Create a dataframe with reviews Data
        df_reviews = pd.DataFrame(reviews)

        # print(df_reviews)
        print(f"Scraped {df_reviews.shape[0]} Reviews from Amazon\n")
        return df_reviews['Description'].tolist()
    

    # Scrapper for Flipkart
    async def flipkart(self, reviews_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Accept-Language': 'en-us,en;q=0.5'
        }

        comments = []
        print(f"\nScraping Reviews from {reviews_url} ...")
        for i in range(1, 5):
            # Construct the URL for the current page
            # https://www.flipkart.com/motorola-g84-5g-viva-magneta-256-gb/p/itmed938e33ffdf5?pid=MOBGQFX672GDDQAQ&fm=organic&ppt=dynamic&ppn=dynamic&ssid=smencraz9c0000001725339457583
            url = reviews_url+'='+str(i)
            

            # Send a GET request to the page
            page = requests.get(url, headers=headers)

            # Parse the HTML content
            soup = BeautifulSoup(page.content, 'html.parser')

            # Extract Comments
            cmt = soup.find_all('div', class_='ZmyHeo')
            for c in cmt:
                comment_text = c.div.div.get_text(strip=True)
                comments.append(comment_text)
        
        print(f'\nScraped {len(comments)} reviews from Flipkart\n')
        return comments
