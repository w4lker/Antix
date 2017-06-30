from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django_mongoengine import Document, EmbeddedDocument
from django_mongoengine import fields



class User(Document):
    username = fields.StringField(max_length=50)
    password = fields.StringField(length=32)

