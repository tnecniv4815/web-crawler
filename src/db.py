import datetime
from mongoengine import *
connect('mydb')

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)

    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()


# ross = User(email='ross@example.com')
# ross.first_name = 'Ross'
# ross.last_name = 'Lawley'
# ross.save()






post1 = TextPost(title='Using MongoEngine', content='See the tutorial')
post1.tags = ['mongodb', 'mongoengine']
# post1.save()

post2 = TextPost(title='title123123', content='Sasdf')
post2.tags = ['asdfdfg', '12123']

posts = [
    post1, post2
]

x = TextPost.objects.insert(posts)

print (x)



# class Post(Document):
#     title = StringField(max_length=120, required=True)
#     author = ReferenceField(User)
#     tags = ListField(StringField(max_length=30))
#
# post1 = TextPost(title='Fun with MongoEngine', author=john)
# post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
# post1.tags = ['mongodb', 'mongoengine']
# # post1.save()
#
# post3 = TextPost(title='MongoEngine', author=ann)
# post3.content = 'looks pretty cool.'
# post3.tags = ['mongoengine2']

# post2 = LinkPost(title='MongoEngine Documentation', author=ross)
# post2.link_url = 'http://docs.mongoengine.com/'
# post2.tags = ['mongoengine']
# post2.save()

# posts = [
#     post1,
#     post3
# ]
#






print ("ok")