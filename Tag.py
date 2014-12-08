import datetime
from mongoengine import EmbeddedDocument, StringField, BooleanField, DateTimeField, ObjectIdField


class Tag(EmbeddedDocument):
    id = ObjectIdField()
    name = StringField(max_length=100, required=True)
    date = DateTimeField(default=datetime.datetime.now)