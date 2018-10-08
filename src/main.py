import requests
from bs4 import BeautifulSoup
import datetime
from mongoengine import *

DB_NAME = "mydb"



class Article(Document):
    title = StringField(max_length=240, required=True)
    thumbnail = StringField()
    contents = ListField()
    created_at = DateTimeField(required=True)


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

        time = content.find_all("div", {"class", "time"})
        if len(time) > 0:
            time = time[0].text


        title = content.find_all("div", {"class", "title"})
        if len(title) > 0:
            title = title[0].text

        thumbnail = content.find_all("img")
        if len(thumbnail) > 0:
            thumbnail = thumbnail[0]["src"]


        created_date_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")

        ################
        ### insert to db
        ################

        print(title)
        print(time)
        print(thumbnail)
        print(link)


        # print(created_date_time)

        oldArticles = Article.objects(created_at=created_date_time)
        if len(oldArticles) == 0:
            # new
            newArticle = Article(title=title, thumbnail=thumbnail, created_at=created_date_time, contents=[])
            newArticle.save()

        # print(oldArticles)


        # x = Article.objects.insert


        print("\n")


urls = [
    "http://std.stheadline.com/instant/articles/listview/%E9%A6%99%E6%B8%AF/"
]

connect(DB_NAME)

for url in urls:
    print("" + url)
    insertArticle(url)




