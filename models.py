from flask_login import UserMixin
from bson.objectid import ObjectId
from app import mongo  # Import the mongo variable from app.py

class User(UserMixin):
    def __init__(self, username, email, password, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data['username'], user_data['email'], user_data['password'], user_data['_id'])
        return None

class Blog:
    def __init__(self, title, content, author, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author = author

    @staticmethod
    def create(title, content, author):
        blog_data = {"title": title, "content": content, "author": author}
        result = mongo.db.blogs.insert_one(blog_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        blogs = mongo.db.blogs.find()
        return [Blog(blog['title'], blog['content'], blog['author'], blog['_id']) for blog in blogs]

    @staticmethod
    def get(blog_id):
        blog_data = mongo.db.blogs.find_one({"_id": ObjectId(blog_id)})
        if blog_data:
            return Blog(blog_data['title'], blog_data['content'], blog_data['author'], blog_data['_id'])
        return None

    @staticmethod
    def delete(blog_id):
        mongo.db.blogs.delete_one({"_id": ObjectId(blog_id)})
