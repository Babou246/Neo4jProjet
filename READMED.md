# Neo4j-Flask-App


Une application de tchat faites avec  Flask , Neo4j et Redis.

## Prerequis
Python3, Neo4j ,Redis et Flask installé.

## Project Structure


1. app.py 
2. templates 
3. requirements.txt 

## Steps to run the app:
Execute in Terminal

```
git clone https://github.com/bBabou246/Neo4jProjet.git
cd Neo4jProjet/   
pip3 install virtualenv   
virtualenv -p python3 env   
source <path>/env/bin/activate
pip install -r requirements.txt
```
**This will start the Neo4j server and you will be able to see the url similar to the one seen below:**

**Allez sur**:
[http://localhost:7474/browser/](http://localhost:7474/browser/)

Once you go to the above url, follow the below steps:

1.  url toi sur "neo4j://" 
2. username = neo4j !defaut
3. Password = neo4j !defaut
4. Clique sur connect

Execute ```python3 app.py```  là ou se trouve app.py

**Allez sur l'url ![port=5000] 
[http://0.0.0.0:5000/](http://0.0.0.0:5002/)**