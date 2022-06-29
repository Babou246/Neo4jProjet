from http.client import SERVICE_UNAVAILABLE
import logging
from main import *

################################################## CREER RELATION ############################################
def create_and_return_friendship(tx, name1,prenom1,email1,adresse1,profession1,sexe1,age1, name2,prenom2,email2,adresse2,profession2,sexe2,age2, knows_from):
        query = (
            "CREATE (p1:Friends { name: $name1,prenom:$prenom1,email:$email1,adresse:$adresse1,profession:$profession1,sexe:$sexe1,age:$age1 }) "
            "CREATE (p2:Parents { name: $name2,prenom:$prenom2,email:$email2,adresse:$adresse2,profession:$profession2,sexe:$sexe2,age:$age2 }) "
            "CREATE (p1)-[k:Parent { relation: $knows_from }]->(p2) "
            "RETURN p1, p2, k"
        )
        result = tx.run(query, name1=name1,prenom1=prenom1,email1=email1,adresse1=adresse1,profession1=profession1,sexe1=sexe1,age1=age1,name2=name2,prenom2=prenom2,email2=email2,adresse2=adresse2,profession2=profession2,sexe2=sexe2,age2=age2,knows_from=knows_from)
        try:
            return [{
                        "p1": row["p1"]["name"],
                        "p2": row["p2"]["name"],
                        "knows_from": row["k"]["relation"]}for row in result]

        # Capture any errors along with the query and data for traceability
        except SERVICE_UNAVAILABLE as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


def create(name1,prenom1,email1,adresse1,profession1,sexe1,age1, name2,prenom2,email2,adresse2,profession2,sexe2,age2, knows_from):
        with driver.session() as session:
            result = session.write_transaction(
                create_and_return_friendship,name1,prenom1,email1,adresse1,profession1,sexe1,age1, name2,prenom2,email2,adresse2,profession2,sexe2,age2, knows_from)
            for row in result:
                print("Created friendship between: {p1}, {p2} relation {knows_from}"
                      .format(p1=row['p1'],p2=row['p2'],knows_from=row["knows_from"]))