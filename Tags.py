import datetime
from mongoengine import Document, StringField, DateTimeField


class Tags(Document):
    name = StringField(max_length=100, required=True)
    date = DateTimeField(default=datetime.datetime.now)