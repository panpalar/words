#!/usr/bin/env python

from Tag import Tag
from mongoengine import Document, StringField, ListField, EmbeddedDocumentField


class Question(Document):
    word = StringField(max_length=500, required=True)
    answer = StringField(max_length=500, required=True)
    tags = ListField(EmbeddedDocumentField(Tag), required=False)