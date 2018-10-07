import requests
from bs4 import BeautifulSoup



def get_data(url):
    r = requests.get(url)
    data = r.content
    soup = BeautifulSoup(data, "html.parser")

    g_data = soup.find_all("div", {"class": "main-left"})

    # g_data = re.sub("<br\s*?>", "\n", g_data)

    # for br in g_data.find_all("br"):
    #     br.replace_with("\n")

    # print(g_data).

    # print (soup.prettify())


    for item in g_data:
        # print(item)

        content = item

        # print(content)


        title = content.find_all("h1")[0].text

        ################
        ### insert to db
        ################


        paragraphs = content.find_all("div", {"class": "paragraph"})
        for paragraph in paragraphs:
            # print(paragraph)

            # paragraph = postContent.find_all("div", {"class": "paragraph"})

            # print(paragraph)


            figures = paragraph.find_all("figure")
            # print(figures)
            if len(figures) > 0:
                for figure in figures:

                    imageUrl = figure.find_all("img", {"class", "size-full"})[0]["src"]
                    imageCaption = figure.find_all("figcaption", {"class", "caption-text"})[0].text

                    # print(imageUrl)
                    # print(imageCaption)

                    ################
                    ### insert to db
                    ################


            p_messages = paragraph.find_all("p")
            if len(p_messages) > 0:
                p_message = p_messages[0]

                # p_message = p_message.replace("<br />", "\n")

                # p_message.replace("<br >", "\n")
                # p_message = p_message.find_all("br").replace_with("\n")

                # br = p_message.find_all("br")
                # br = br.replace_with("\n")

                # print(br)

                print(p_message)

                ################
                ### insert to db
                ################


            print("\n")



        # print(title)
        # print(paragraphs)


        print("\n")




urls = [
    "http://std.stheadline.com/instant/articles/detail/834721-%E9%A6%99%E6%B8%AF-63%E6%AD%B2%E5%8D%97%E7%BE%8E%E6%97%85%E5%AE%A2%E6%B6%89%E8%97%8F%E5%8F%AF%E5%8D%A1%E5%9B%A0+%E6%A9%9F%E5%A0%B4%E5%85%A5%E5%A2%83%E8%A2%AB%E6%8D%95"
]


for url in urls:
    print("" + url + "\n\n")
    get_data(url)

# greeting()
