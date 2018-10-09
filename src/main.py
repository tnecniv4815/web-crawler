import requests
from bs4 import BeautifulSoup
import datetime
import time
from mongoengine import *
import urllib
from pathlib import Path

import os

DEFAULT_IMG_EXT = "jpg"
ROOT_PATH = os.path.abspath(__file__ + "/../../")
IMG_DEST = os.path.join(ROOT_PATH + "/public/images/")

# print (ROOT_PATH)
# print (IMG_DEST)
# print (os.path.abspath(__file__ + "/../../"))

DB_NAME = "mydb"



class Article(Document):
    title = StringField(max_length=240, required=True)
    thumbnail = StringField()
    contents = ListField()
    created_at = DateTimeField(required=True)

def generate_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

    return st

def get_file_extension(tmp_url):
    extension = ""

    tmp_ext_array = tmp_url.split(".")
    if len(tmp_ext_array) > 0:
        extension = tmp_ext_array[len(tmp_ext_array) - 1]
    else:
        extension = DEFAULT_IMG_EXT
    return extension

def saveImage(src_url, dest_url_with_filename):
    img_file = Path(dest_url_with_filename)
    if not img_file.is_file():
        urllib.request.urlretrieve(src_url, dest_url_with_filename)

def scrapeArticleDetail(url):
    list = []

    links = url.split("/")
    if len(links) > 0:
        endpoint = links[len(links)-1]

        # url = "http://std.stheadline.com/instant/articles/detail/" + "835807-%E9%A6%99%E6%B8%AF-%E6%B7%B1%E6%B0%B4%E5%9F%97%E5%8A%8F%E6%88%BF%E8%80%81%E7%BF%81%E6%B6%89%E6%AE%BA%E6%88%BF%E5%AE%A2%E5%BE%8C%E7%B8%B1%E7%81%AB%E7%87%92%E5%B1%8B%E5%86%8D%E5%A2%AE%E6%96%83+%E5%88%97%E8%AC%80%E6%AE%BA%E5%8F%8A%E8%87%AA%E6%AE%BA%E9%87%8D%E6%A1%88%E7%B5%84%E8%B7%9F%E9%80%B2"
        url = "http://std.stheadline.com/instant/articles/detail/" + endpoint
        print("scrapeArticleDetail_url: " + url)


        request = requests.get(url)
        data = request.content
        soup = BeautifulSoup(data, "html.parser")

        contents = soup.find_all("div", {"class": "paragraph"})

        # print (soup)
        # print (contents)

        for item in contents:
            # print (item)

            figures = item.find_all("figure")

            for figure in figures:
                fig_images = figure.find_all("img")

                if len(fig_images) > 0:
                    fig_image_url = fig_images[0]["src"]


                    ext = get_file_extension(fig_image_url)
                    filename = generate_timestamp()
                    FULL_IMG_PATH = IMG_DEST + filename + "." + ext

                    saveImage(fig_image_url, FULL_IMG_PATH)

                    # append
                    list.append(FULL_IMG_PATH)

                    print (fig_image_url)


                fig_caption = figure.find_all("figcaption", {"class": "caption-text"})[0]

                print (fig_caption.text)


        print ("\n\n")


    return list



def insertArticleDetail(url, created_date_time_obj):
    print("insertArticleDetail")

    articles = Article.objects(created_at=created_date_time_obj)
    if len(articles) > 0:
        article = articles[0]

        list = scrapeArticleDetail(url)



def scrapeArticle(url):

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


        created_date_time_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")

        """
        ################
        ### insert to db
        ################
        """


        print(title)
        # print(time)
        # print(thumbnail)
        # print(link)

        # thumbnail_image_dest_path = "/Users/vincent/repository/github/web-crawler/public/images/abc.jpg"

        # print (IMG_DEST)
        # print (created_date_time_obj.date())


        ext = get_file_extension(thumbnail)



        filename = created_date_time_obj.strftime("%Y-%m-%d_%H:%M")

        thumbnail_image_dest_path = IMG_DEST + filename + "." + ext
        # print (thumbnail_image_dest_path)

        # urllib.request.urlretrieve(thumbnail, thumbnail_image_dest_path)

        saveImage(thumbnail, thumbnail_image_dest_path)


        # print(created_date_time)

        oldArticles = Article.objects(created_at=created_date_time_obj)
        if len(oldArticles) == 0:
            # new
            newArticle = Article(title=title, thumbnail=thumbnail_image_dest_path, created_at=created_date_time_obj, contents=[])
            newArticle.save()


        if link != "":
            insertArticleDetail(link, created_date_time_obj)




        # print(oldArticles)


        # x = Article.objects.insert


        print("\n")


urls = [
    "http://std.stheadline.com/instant/articles/listview/%E9%A6%99%E6%B8%AF/"
]

connect(DB_NAME)

for url in urls:
    print("" + url)
    scrapeArticle(url)




