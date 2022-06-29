
import logging
import sys

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class Madel:
    def __init__(self, uri,user,pwd):
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name, knows_from):
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[k:KNOWS { from: $knows_from }]->(p2) "
            "RETURN p1, p2, k"
        )
        result = tx.run(query, person1_name=person1_name,person2_name=person2_name, knows_from=knows_from)
        try:
            return [{
                        "p1": row["p1"]["name"],
                        "p2": row["p2"]["name"],
                        "knows_from": row["k"]["from"]}for row in result]

        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
    def create(self, person1_name, person2_name, knows_from):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name, knows_from)
            for row in result:
                print("Created friendship between: {p1}, {p2} from {knows_from}"
                      .format(p1=row['p1'],p2=row['p2'],knows_from=row["knows_from"]))


    # ADD FRIENDS
    def add_friend(tx, name, friend_name):
        tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

    def print_friends(tx, name):
        for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                            "RETURN friend.name ORDER BY friend.name", name=name):
            print(record["friend.name"])



bolt_url ="neo4j://localhost:7687"
user = "neo4j"
password = "dev"
# Madel.enable_log(logging.INFO, sys.stdout)
app = Madel(bolt_url, user, password)
app.create("Alice", "David", "School")
# app.find_person("Alice")