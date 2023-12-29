from bs4 import BeautifulSoup
import requests
import pandas as pd
from fake_useragent import UserAgent
import concurrent.futures


def attractions():
# THINGS TO DO
#https://www.tripadvisor.com/Attraction_Review-g186338-d187676-Reviews-Natural_History_Museum-London_England.html# done

#https://www.tripadvisor.com/Attraction_Review-g186338-d187555-Reviews-The_British_Museum-London_England.html done

#https://www.tripadvisor.com/Attraction_Review-g186338-d187547-Reviews-Tower_of_London-London_England.html not

#https://www.tripadvisor.com/Attraction_Review-g186338-d553603-Reviews-London_Eye-London_England.html done

#https://www.tripadvisor.com/Attraction_Review-g186338-d188862-Reviews-National_Gallery-London_England.html done

    url = [f"https://www.tripadvisor.com/Attraction_Review-g186338-d187547-Reviews-or{i:d}-Tower_of_London-London_England.html" for i in (range(10,3000,10))]

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
                dates.append(i.text.replace('Written ',''))
            content = box.find_all('span', class_ ='yCeTE')
            for k in content:
                contents.append(k.text)

        print(url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(scrape,url)

    filt = [string for string in contents if not string.startswith("Tickets") and string != "Learn more about animal welfare in tourism"]
    titles = [string for index, string in enumerate(filt) if index % 2 == 0]
    stories = [string for index, string in enumerate(filt) if index % 2 != 0]
    data = {'date_written': dates, 'title': titles, 'content': stories}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_csv(f'./Tari_csv/Attractions/{url[0][27:-5]}.csv', index=False)


def hotels():
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    from fake_useragent import UserAgent
    import concurrent.futures


    #HOTELS

    #https://www.tripadvisor.com/Hotel_Review-g186338-d188961-Reviews-Hotel_41-London_England.html

    #https://www.tripadvisor.com/Hotel_Review-g186338-d193121-Reviews-The_Milestone_Hotel_and_Residences-London_England.html

    #https://www.tripadvisor.com/Hotel_Review-g186338-d6484754-Reviews-Shangri_La_The_Shard_London-London_England.html done

    #https://www.tripadvisor.com/Hotel_Review-g186338-d188019-Reviews-Brown_s_Hotel-London_England.html done

    #https://www.tripadvisor.com/Hotel_Review-g186338-d2413342-Reviews-The_Hari-London_England.html done

    url = [f"https://www.tripadvisor.com/Hotel_Review-g186338-d188961-Reviews-or{i:d}-Hotel_41-London_England.html" for i in (range(10,3000,10))]

    dates = []
    contents = []
    titles = []
    def scrape(url):
        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}

        s = requests.Session()
        s.headers.update(headers)

        page = s.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        review_box = soup.find_all('div', class_= "WAllg _T")
        for box in review_box:

            date = box.find_all('span', class_ ='teHYY _R Me S4 H3')
            for i in date:
                dates.append(i.text.replace('Date of stay: ',''))

            content = box.find_all('span', class_ ='QewHA H4 _a')
            for k in content:
                contents.append(k.text)

            title = box.find_all('a', class_ ="Qwuub")
            for k in title:
                titles.append(k.text)

        print(url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(scrape,url)

    data = {'date_written': dates, 'title': titles, 'content': contents}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_csv(f'./Tari_csv/Hotels/{url[0][27:-5]}.csv', index=False)

def restaurants():
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    from fake_useragent import UserAgent
    import concurrent.futures

    #RESTAURANTS

    #https://www.tripadvisor.com/Restaurant_Review-g186338-d719675-Reviews-Launceston_Place-London_England.html done

    #https://www.tripadvisor.com/Restaurant_Review-g186338-d12801049-Reviews-Core_by_Clare_Smyth-London_England.html done

    #https://www.tripadvisor.com/Restaurant_Review-g186338-d10682050-Reviews-Ormer_Mayfair-London_England.html done

    #https://www.tripadvisor.com/Restaurant_Review-g186338-d720761-Reviews-The_Ledbury-London_England.html done

    #https://www.tripadvisor.com/Restaurant_Review-g186338-d3853609-Reviews-The_Five_Fields-London_England.html done

    url = [f"https://www.tripadvisor.com/Hotel_Review-g186338-d3853609-Reviews-or{i:d}-The_Five_Fields-London_England.html" for i in (range(10,3000,10))]
    dates = []
    contents = []
    titles = []
    def scrape(url):
        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}

        s = requests.Session()
        s.headers.update(headers)

        page = s.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        review_box = soup.find_all('div', class_= "ui_column is-9")
        for box in review_box:

            date = box.find_all('div', class_ ="prw_rup prw_reviews_stay_date_hsx")
            for i in date:
                dates.append(i.text.replace('Date of visit: ',''))  #.replace('Date of visit: ','')

            content = box.find('div', class_ ='entry')
            for k in content:
                contents.append(k.text)

            title = box.find_all('div', class_ ="quote")
            for k in title:
                titles.append(k.text)

        print(url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(scrape,url)

    data = {'date_written': dates, 'title': titles, 'content': contents}
    df = pd.DataFrame(data)

    df.to_csv(f'./Tari_csv/Restaurants/{url[0][27:-5]}.csv', index=False)


