from bs4 import BeautifulSoup
import requests
import pandas as pd

import concurrent.futures

url = [f"https://www.tripadvisor.com/Attraction_Review-g186338-d187676-Reviews-or{i:d}-Natural_History_Museum-London_England.html" for i in (range(10,20000,10))]

dates = []
contents = []
def scrape(url):
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    s = requests.Session()
    s.headers.update(headers)
    page = s.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    review_box = soup.find_all('div', class_= "_c")
    for box in review_box:
        date = box.find_all('div', class_ ='biGQs _P pZUbB ncFvv osNWb')
        for i in date:
            dates.append(i.text)
        content = box.find_all('span', class_ ='yCeTE')
        for k in content:
            contents.append(k.text)

    print(url)

with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
    executor.map(scrape,url)

filt = [string for string in contents if not string.startswith("Tickets") and string != "Learn more about animal welfare in tourism"]
titles = [string for index, string in enumerate(filt) if index % 2 == 0]
stories = [string for index, string in enumerate(filt) if index % 2 != 0]
data = {'date_written': dates, 'title': titles, 'content': stories}
df = pd.DataFrame(data)
df.to_csv(f'./Tari_csv{url[0][27:-5]}.csv', index=False)
