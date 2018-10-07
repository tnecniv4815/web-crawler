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
        img_links = content.find_all("div", {"class": "s171ml6l-0"})[0]
        # img_links = content.find_all("img")


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
    "https://www.hk01.com/zone/1/%E6%B8%AF%E8%81%9E",
    "https://www.hk01.com/%E7%A4%BE%E6%9C%83%E6%96%B0%E8%81%9E/243940/%E6%99%82%E4%BB%A3%E5%BB%A3%E5%A0%B4%E7%94%B3%E7%A6%81%E4%BB%A4-%E9%AB%98%E9%99%A2%E9%A0%92%E4%BB%A4%E7%A6%81%E5%9C%B0%E4%B8%8B%E8%A1%A8%E6%BC%94-%E8%A8%B1%E5%BB%B7%E9%8F%97%E6%9B%BE%E6%94%B6%E8%AD%A6%E5%91%8A%E4%BF%A1"
]


for url in urls:
    print("" + url)
    get_data(url)



