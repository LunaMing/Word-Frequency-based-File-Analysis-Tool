from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, StructuredRel


class PaperInfo(models.Model):
    title = models.CharField(max_length=255)
    author = models.TextField()
    school = models.TextField()
    abstract = models.TextField()

    def __str__(self):
        return self.title


class Word(StructuredNode):
    name = StringProperty(unique_index=True, required=True)


class Contain(StructuredRel):
    number = IntegerProperty(required=True)


class Paper(StringProperty):
    title = StringProperty(unique_index=True, required=True)

    word = RelationshipTo(Word, 'CONTAIN', model=Contain)


class Author(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

    paper = RelationshipTo(Paper, "WRITE")
