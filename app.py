import requests
from bs4 import BeautifulSoup


def get_data(url):
    r = requests.get(url)
    data = r.content
    soup = BeautifulSoup(data, "html.parser")

    g_data = soup.find_all("div", {"class": "s1d313me-0"})

    # print(g_data).

    # print (soup.prettify())


    for item in g_data:
        # print(item)

        content = item.contents[0]


        # img_links = content.find_all("img", {"class": "s171ml6l-1"})
        # img_links = content.find_all("div", {"class": "s19vvetr-0"})
        img_links = content.find_all("img")


        news_top = content.find_all("div", {"class": "sc-bdVaJa"})


        news_bottom = content.find_all("div", {"class": "s1lsq47l-3"})[0]

        news_detail_link = news_bottom.find_all("a", href=True)[0]

        title = news_detail_link.text
        link = news_detail_link["href"]

        print(img_links)

        # print(title)
        # print(link)


        print("\n")





urls = [
    "https://www.hk01.com/zone/1/%E6%B8%AF%E8%81%9E"
]


for url in urls:
    print("" + url)
    get_data(url)



