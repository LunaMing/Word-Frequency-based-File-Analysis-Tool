from neo4j import GraphDatabase


def add_author_write_paper(tx, name, paper_title):
    tx.run("MERGE (a:Author {name: $name}) "
           "MERGE (a)-[:WRITE]->(p:Paper {title: $paper_title})",
           name=name, paper_title=paper_title)


def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])


def print_author_papers(tx, name):
    for record in tx.run("MATCH (a:Author)-[:WRITE]->(paper) WHERE a.name = $name "
                         "RETURN paper.title ORDER BY paper.title", name=name):
        print(record["paper.title"])


def neo4j_driver():
    driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123456"))

    with driver.session() as session:
        session.write_transaction(add_author_write_paper, "author1",
                                  "title1")
        session.read_transaction(print_author_papers, "author1")

    driver.close()
    exit()
