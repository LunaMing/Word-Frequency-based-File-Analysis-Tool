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
    number = IntegerProperty()


class Paper(StructuredNode):
    title = StringProperty(unique_index=True, required=True)

    word = RelationshipTo(Word, 'CONTAIN', model=Contain)

    def get_contain_words(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)=$self MATCH (a)-[:CONTAIN]->(b) RETURN b")
        return [Word.inflate(row[0]) for row in results]

    def get_paper_author(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)=$self MATCH (a)<-[:WRITE]-(b) RETURN b")
        return [Author.inflate(row[0]) for row in results]


class Author(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

    paper = RelationshipTo(Paper, "WRITE")
