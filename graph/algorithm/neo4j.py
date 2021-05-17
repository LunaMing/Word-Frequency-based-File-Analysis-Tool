import traceback

from neomodel import clear_neo4j_database, db

from graph.models import Author, Paper, Word


def get_all_kind(kind):
    try:
        if kind == 'Paper':
            nodes = Paper.nodes.all()
        elif kind == 'Author':
            nodes = Author.nodes.all()
        elif kind == 'Word':
            nodes = Word.nodes.all()
        else:
            raise Exception("'kind' not in Paper or Author or Word")
        response = []
        for node in nodes:
            if kind == 'Paper':
                obj = node.title
            elif kind == 'Author' or 'Word':
                obj = node.name
            else:
                raise Exception("'kind' not in Paper or Author or Word")
            response.append(obj)
    except Exception as e:
        traceback.print_exc()
        response = {"error": e}
    return response


def export_neo4j_data():
    data = []
    try:
        papers = Paper.nodes.all()
        for paper in papers:
            authors = []
            author_list = paper.get_paper_author()
            for author in author_list:
                author_obj = {
                    "id": author.id,
                    "name": author.name,
                }
                authors.append(author_obj)

            words = []
            word_list = paper.get_contain_words()
            for word in word_list:
                word_obj = {
                    "id": word.id,
                    "name": word.name,
                }
                words.append(word_obj)

            paper = {
                "id": paper.id,
                "title": paper.title,
                "words": words,
                "authors": authors,
            }
            data.append(paper)
    except Exception as e:
        traceback.print_exc()
        data = {"error": e}
    return data


def import_neo4j(paper_data, word_data):
    for i in range(len(paper_data)):
        paper_title = paper_data[i]
        try:
            paper = Paper.get_or_create({"title": paper_title})[0]
        except Exception as e:
            traceback.print_exc()
            return e
        word_list = word_data[i]
        for word_name in word_list:
            word = Word.get_or_create({"name": word_name})[0]
            paper.word.connect(word)


def clear_neo4j():
    clear_neo4j_database(db)
