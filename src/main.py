import requests
from bs4 import BeautifulSoup
import datetime
import time
from mongoengine import *
import urllib
from pathlib import Path
import os
from enum import Enum
import re

DEFAULT_IMG_EXT = "jpg"
ROOT_PATH = os.path.abspath(__file__ + "/../../")

# IMG_DEST = os.path.join(ROOT_PATH + "/public/images/")
IMG_DEST = os.path.join("/Users/vincent/repository/github/backend-node-server" + "/public/images/")

IMG_SAVE_DEST = "/public/images/"

# print (ROOT_PATH)
# print (IMG_DEST)
# print (os.path.abspath(__file__ + "/../../"))

DB_NAME = "mydb"


class ArticleContent(Document):
    article_id = ObjectIdField()
    content = StringField()
    type = DecimalField()
    subtitle = StringField()
    media_url = StringField()
    created_at = DateTimeField(required=True)


class ContentType(Enum):
    PARAGRAPH = "1"
    IMAGE = "2"

"""

class ArticleContent:
    content = ""
    type
    caption = ""

    def __init__(self, content, type, caption):
        self.content = content
        self.type = type
        self.caption = caption
"""

class Article(Document):
    article_id = DecimalField()
    title = StringField(max_length=240, required=True)
    thumbnail = StringField()
    contents = ListField(ObjectIdField())
    posted_at = DateTimeField(required=True)
    created_at = DateTimeField(required=True)

def generate_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

    return st

def get_filename_with_extension(tmp_url):
    print ("get_filename_with_extension: ", tmp_url)

    tmp_fileanme = ""

    if type(tmp_url) == str:
        tmp_array = tmp_url.split("/")
        if len(tmp_array) > 0:
            tmp_fileanme = tmp_array[len(tmp_array) - 1]
        else:
            tmp_fileanme = generate_timestamp()
    else:
        tmp_fileanme = generate_timestamp()

    return tmp_fileanme

def get_file_extension(tmp_url):
    # tmp_url = "" + tmp_url
    print ("get_file_extension: ", tmp_url)

    extension = DEFAULT_IMG_EXT

    if type(tmp_url) == str:
        tmp_ext_array = tmp_url.split(".")
        if len(tmp_ext_array) > 0:
            extension = tmp_ext_array[len(tmp_ext_array) - 1]
        else:
            extension = DEFAULT_IMG_EXT
    else:
        extension = DEFAULT_IMG_EXT
    return extension

def saveImage(src_url, dest_url_with_filename):
    print ("src_url: {} \ndest_url_with_filename: {}".format(src_url, dest_url_with_filename))

    img_file = Path(dest_url_with_filename)
    if not img_file.is_file():
        urllib.request.urlretrieve(src_url, dest_url_with_filename)

def scrapeArticleDetail(article, url, posted_date_time_obj):
    list = []

    endpoint = "http://std.stheadline.com/instant/articles/detail/"

    links = url.split("/")
    if len(links) > 0:
        url_end = links[len(links)-1]

        # url = "http://std.stheadline.com/instant/articles/detail/" + "835807-%E9%A6%99%E6%B8%AF-%E6%B7%B1%E6%B0%B4%E5%9F%97%E5%8A%8F%E6%88%BF%E8%80%81%E7%BF%81%E6%B6%89%E6%AE%BA%E6%88%BF%E5%AE%A2%E5%BE%8C%E7%B8%B1%E7%81%AB%E7%87%92%E5%B1%8B%E5%86%8D%E5%A2%AE%E6%96%83+%E5%88%97%E8%AC%80%E6%AE%BA%E5%8F%8A%E8%87%AA%E6%AE%BA%E9%87%8D%E6%A1%88%E7%B5%84%E8%B7%9F%E9%80%B2"
        url = endpoint + url_end
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

            """
            image
            """
            for figure in figures:
                # full_img_path = ""

                fig_images = figure.find_all("img")

                if len(fig_images) > 0:
                    fig_image_url = fig_images[0]["src"]


                    # ext = get_file_extension(fig_image_url)
                    # filename = generate_timestamp()
                    # full_img_path = IMG_DEST + filename + "." + ext

                    filename_with_ext = get_filename_with_extension(fig_image_url)
                    image_path = IMG_SAVE_DEST + filename_with_ext
                    full_img_path = IMG_DEST + filename_with_ext

                    saveImage(fig_image_url, full_img_path)



                    # print (fig_image_url)


                fig_caption = "" + figure.find_all("figcaption", {"class": "caption-text"})[0].text

                # append
                # list_obj = ArticleContent(full_img_path, ContentType.IMAGE, fig_caption)
                # list.append(list_obj)

                # newArticle = Article(title=title, thumbnail=thumbnail_image_dest_path, posted_at=posted_date_time_obj, created_at=datetime.datetime.now(), contents=[])

                # 2 = Image
                content_type = 2



                tmp_old_article_content = ArticleContent.objects(article_id=article.id, media_url=image_path, type=content_type).first()
                if tmp_old_article_content is None:
                    # print ("laksdfjlkasdjflkasjdflkjasdklf")
                    # print (tmp_old_article_content)

                    new_article_content = ArticleContent(article_id=article.id, type=content_type, subtitle=fig_caption, media_url=image_path, created_at=datetime.datetime.now())
                    new_article_content.save()

                    new_insert_article_content = ArticleContent.objects(article_id=article.id, media_url=image_path, type=content_type).first()
                    if new_insert_article_content is not None:
                        article.contents.append(new_insert_article_content.id)
                        article.save()

                # print ("contentId: " + new_article_content.id)
                # print ("articleId: " + article.id)
                # print ("article_contents: " + article.contents)

                # print (fig_caption.text)

            """
            paragrpah
            """
            ps = item.find_all("p")

            for p in ps:

                for br in p.find_all("br"):
                    br.replace_with("\n")


                # print ("pppp")
                # print (p)
                # print ("pppp~~~~~")
                # # print (s)
                # print ("pppp_____")
                # print (p.text)

                # append
                # list_obj = ArticleContent(p.text, ContentType.PARAGRAPH, "")
                # list.append(list_obj)

                # 1 = paragraph
                content_type = 1

                tmp_old_article_content = ArticleContent.objects(article_id=article.id, content=p.text, type=content_type).first()
                if tmp_old_article_content is None:
                    print ("tmp_old_article_content paragraph")
                    print (tmp_old_article_content)

                    new_article_content = ArticleContent(article_id=article.id, type=content_type, created_at=datetime.datetime.now(), content=p.text)
                    new_article_content.save()

                    new_insert_article_content = ArticleContent.objects(article_id=article.id, content=p.text, type=content_type).first()
                    print ("new_insert_article_content")
                    print (new_insert_article_content)
                    if new_insert_article_content is not None:
                        article.contents.append(new_insert_article_content.id)
                        article.save()



        """
        get article object
        query article content object (get ObjectId)
        update contents[ObjectId, ObjectId]
        """

        """
        print ("tmp_article_contents")

        tmp_article_contents = ArticleContent.objects(article_id=article.id)
        for content_obj in tmp_article_contents:
            print ("type: {}  , subtitle: {}".format(content_obj.type, content_obj.subtitle))
            article.contents.append(content_obj.id)

        article.save()
        
        """


        print ("list")
        print (list)
        print ("\n\n")


    return list



def insertArticleDetail(url, posted_date_time_obj):
    print("insertArticleDetail")

    articles = Article.objects(posted_at=posted_date_time_obj)
    if len(articles) > 0:
        article = articles[0]

        list = scrapeArticleDetail(article, url, posted_date_time_obj)

        # list = []

        # list.append(ArticleContent("123", ContentType.PARAGRAPH, "asdf"))

        # list.append("aaa")
        # list.append("bbb")
        # list.append("ccc")

        # Article.update(posted_at=posted_date_time_obj, contents=list)

        # article

        # print (article.id)

        # article.title = "haha"
        # article.contents = list #["asdf", "123123", "sdfasdag"]
        # article.save()

        # if len(list) > 0:
            # article.contents = list
            # article.update()



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


        posted_date_time_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")

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
        # print (posted_date_time_obj.date())


        ext = get_file_extension(thumbnail)



        filename = posted_date_time_obj.strftime("%Y-%m-%d_%H:%M")

        thumbnail_image_path = IMG_SAVE_DEST + filename + "." + ext
        thumbnail_image_dest_path = IMG_DEST + filename + "." + ext

        print (thumbnail)
        print (thumbnail_image_path)
        print (thumbnail_image_dest_path)

        # urllib.request.urlretrieve(thumbnail, thumbnail_image_dest_path)

        saveImage(thumbnail, thumbnail_image_dest_path)



        # print(created_date_time)

        oldArticles = Article.objects(posted_at=posted_date_time_obj)
        if len(oldArticles) == 0:
            # new
            # article_id=posted_date_time_obj,
            newArticle = Article(title=title, thumbnail=thumbnail_image_path, posted_at=posted_date_time_obj, created_at=datetime.datetime.now())
            newArticle.save()


        if link != "":
            insertArticleDetail(link, posted_date_time_obj)




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




