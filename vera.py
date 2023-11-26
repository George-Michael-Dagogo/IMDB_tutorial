import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import concurrent.futures
import pandas as pd

url = 'https://www.macys.com/shop/featured/women-handbags'

ua = UserAgent()
userAgent = ua.random
headers = {'User-Agent': userAgent}
s = requests.Session()
s.headers.update(headers)
page = s.get(url)
soup = BeautifulSoup(page.content, "html.parser")
sales_box = soup.find_all('div', class_= "productDescription")
brands = []
prices = []
discounts = []
ratings = []
product_urls = []
image_urls = []

for box in sales_box:
    #brands
    if box.find('div', class_ = "productBrand") is not None:
        brand = box.find('div', class_ = "productBrand").text.replace('\n\t\t','').strip()
        brands.append(brand)
    else:
        brands.append('None')

    #price
    if box.find('span', class_ = "regular originalOrRegularPriceOnSale") is not None:
        price = box.find('span', class_ = "regular originalOrRegularPriceOnSale").text.replace('\n\t\t','').replace('\n','').strip()
        prices.append(price)
    else:
        prices.append('None')

    #discounts
    if box.find('span', class_ = "discount") is not None:
        discount = box.find('span', class_ = "discount").text.replace('\n\t\t','').replace('\n','').strip()
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

    #product_url
    if box.find('a', attrs={"href": True}) is not None:
        product_url = box.find('a', attrs={"href": True})   #.replace('\n\t\t','').replace('\n','').strip()
        product_url = product_url['href']
        product_urls.append(product_url)
    else:
        product_urls.append('None')


def image_link_get(new_url):
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent

    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    s = requests.Session()
    s.headers.update(headers)
    page = s.get('https://www.macys.com'+ new_url)
    new_soup = BeautifulSoup(page.content, "html.parser")
    image_box = new_soup.find_all('div', class_= "image-grid-container")
    
    print(new_url)

    for box in image_box:
        #brands
        if  box.find('source', type='image/webp',attrs={"srcset": True}) is not None:
            image_url = box.find('source', type='image/webp',attrs={"srcset": True})
            image_url = image_url['srcset']
            image_urls.append(image_url)
        else:
            image_urls.append('None')



with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(image_link_get,product_urls)

brand_df = pd.DataFrame({
    'brand':brands,
    'price':prices,
    'discount/on_sale':discounts,
    'rating':ratings,
    'product_urls': product_urls
    #'image_url':image_urls
})


brand_df


