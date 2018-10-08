import requests
from bs4 import BeautifulSoup
import datetime
from mongoengine import *




class Article(Document):
    title = StringField(max_length=240, required=True)
    created_at = DateTimeField()
    thumbnail = StringField()
    contents = ListField()

def insertArticleDetail(url):
    print("insertArticleDetail")



def insertArticle(url):

    r = requests.get(url)
    data = r.content
    soup = BeautifulSoup(data, "html.parser")

    g_data = soup.find_all("div", {"class": "news-wrap"})

    # print(g_data).

    # print (soup.prettify())


    for item in g_data:
        # print(item)

        content = item.contents[1]

        link = content["href"]

        time = content.find_all("div", {"class", "time"})[0].text
        title = content.find_all("div", {"class", "title"})[0].text
        thumbnail = content.find_all("img")[0]["src"]

        ################
        ### insert to db
        ################

        print(title)
        print(time)
        print(thumbnail)
        print(link)



        print("\n")








urls = [
    "http://std.stheadline.com/instant/articles/listview/%E9%A6%99%E6%B8%AF/"
]

for url in urls:
    print("" + url)
    insertArticle(url)




