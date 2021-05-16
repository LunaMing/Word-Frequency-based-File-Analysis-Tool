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

class Dog(StructuredNode):
    name = StringProperty(required=True)
    owner = RelationshipTo('Person', 'owner')

class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    pets = RelationshipFrom('Dog', 'owner')

bob = Person.get_or_create({"name": "Bob"})[0]
bobs_gizmo = Dog.get_or_create({"name": "Gizmo"}, relationship=bob.pets)

tim = Person.get_or_create({"name": "Tim"})[0]
tims_gizmo = Dog.get_or_create({"name": "Gizmo"}, relationship=tim.pets)

# not the same gizmo
assert bobs_gizmo[0] != tims_gizmo[0]
