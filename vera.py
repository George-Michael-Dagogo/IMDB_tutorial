import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import concurrent.futures
import pandas as pd

#url = 'https://www.macys.com/shop/featured/women-handbags'
url = [f'https://www.macys.com/shop/featured/women-handbags/Pageindex/{i:d}' for i in (range(1,3,1))]

brands = []
prices = []
discounts = []
ratings = []
product_urls = []
image_urls = []
product_names = []
product_description = []

def scrape_pages(url):
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    print(url)
    sales_box = soup.find_all('li', class_= "cell productThumbnailItem")

    for box in sales_box:
        #brands
        if box.find('div', class_ = "productBrand") is not None:
            brand = box.find('div', class_ = "productBrand").text.replace('\n\t\t','').strip()
            brands.append(brand)
        else:
            brands.append('None')

          #product_name
        if box.find('a', attrs={"title": True}) is not None:
            product_name = box.find('a', attrs={"title": True})   #.replace('\n\t\t','').replace('\n','').strip()
            product_name = product_name['title']
            product_names.append(product_name)
        else:
            product_names.append('None')        


        #price
        if box.find('span', class_ = "regular originalOrRegularPriceOnSale") is not None:
            price = box.find('span', class_ = "regular originalOrRegularPriceOnSale").text.replace('\n\t\t','').replace('\n','').strip()
            prices.append(price)
        elif box.find('span', class_ = "regular") is not None:
            price = box.find('span', class_ = "regular").text.replace('\n\t\t','').replace('\n','').strip()
            prices.append(price)
        else:
            prices.append('None')

        #discounts
        if box.find('span', class_ = "discount") is not None:
            discount = box.find('span', class_ = "discount").text.replace('\n\t\t','').replace('\n','').strip()
            discounts.append(discount)
        elif box.find('span',attrs={'data-auto': 'final-price'}) is not None:
            discount = box.find('span', attrs={'data-auto': 'final-price'}).text.replace('\n\t\t','').replace('\n','').strip()
            discounts.append(discount)
        else:
            discounts.append('None')

        #ratings
        if box.find('div', class_ = "stars" ) is not None:
            rating = box.find('div', class_ = "stars",attrs={"aria-label": True})   #.replace('\n\t\t','').replace('\n','').strip()
            rating = rating['aria-label']
            ratings.append(rating)
        else:
            ratings.append('None')
    
     
        if  box.find('source',attrs={"data-lazysrcset": True}) is not None:
            image_url = box.find('source',attrs={"data-lazysrcset": True})
            image_url = image_url['data-lazysrcset']
            image_urls.append(image_url)
        elif box.find('source',attrs={"srcset": True}) is not None:
            image_url = box.find('source',attrs={"srcset": True})
            image_url = image_url['srcset']
            image_urls.append(image_url)
        else:
            image_urls.append('None')

                #product_url
        if box.find('a', attrs={"href": True}) is not None:
            product_url = box.find('a', attrs={"href": True})   #.replace('\n\t\t','').replace('\n','').strip()
            product_url = product_url['href']
            product_urls.append(product_url)
        else:
            product_urls.append('None')




with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(scrape_pages,url)

def details_get(urls):
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    link = 'https://www.macys.com'+ urls
    print(link)
    new_page = requests.get(link, headers = headers)
    new_soup = BeautifulSoup(new_page.content, "html.parser")
    if new_soup.find('div', class_= "details-content") is not None:
        details = new_soup.find('div', class_= "details-content").text.replace('\n','...').strip()
        product_description.append(details)
    else:
        product_description.append('None') 

for i in product_urls:
    print(i)
    details_get(i)



brand_df = pd.DataFrame({
    'brand':brands,
    'product':product_names,
    'price':prices,
    'discount/on_sale':discounts,
    'rating':ratings,
    'product_urls': product_urls,
    'image_url':image_urls,
    'product_details':product_description
})


brand_df


