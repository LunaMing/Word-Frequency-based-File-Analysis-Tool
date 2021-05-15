from neo4j import GraphDatabase


def add_paper_contain_word(tx, paper_title, word, number):
    tx.run("MERGE (p:Paper {title: $paper_title}) "
           "MERGE (p)-[:CONTAIN {number: $number}]->(w:Word {name: $name})",
           name=word, paper_title=paper_title, number=number)


def add_author_write_paper(tx, name, paper_title):
    tx.run("MERGE (p:Paper {title: $paper_title}) "
           "MERGE (a:Author {name: $name})-[:WRITE]->(p)",
           name=name, paper_title=paper_title)


def print_paper_words(tx, paper_title):
    for record in tx.run("MATCH (p:Paper)-[c:CONTAIN]->(word) WHERE p.title = $title "
                         "RETURN c.number, word.name ORDER BY c.number DESC", title=paper_title):
        print(record['word.name'] + ": " + record['c.number'])


def neo4j_driver():
    driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123456"))

    with driver.session() as session:
        session.write_transaction(add_author_write_paper, "author1", "title1")
        session.write_transaction(add_paper_contain_word, "title1", "word1", "1")
        session.write_transaction(add_paper_contain_word, "title1", "word2", "2")
        session.read_transaction(print_paper_words, "title1")

    driver.close()
    exit()
