from ast import Name
from json import dumps
from flask_socketio import SocketIO, send
import time
import redis
from neo4j import GraphDatabase
from flask_login import login_user, logout_user, login_required,current_user,LoginManager
from flask import Flask, Response, flash,session, jsonify, redirect, render_template, request, url_for
import networkx as nx
import matplotlib


 
app = Flask(__name__)
app.config["SECRET_KEY"]= 'ffcgjvkjbkgyfuyjvh'
connect_to_redis = redis.Redis(host="127.0.0.1",port=6379,charset="utf-8", decode_responses=True) 
driver=GraphDatabase.driver(uri="neo4j://localhost:7687",auth=("neo4j","dev"))
Session=driver.session()


app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)


login_manager = LoginManager()
login_manager.login_view = 'Admin'
login_manager.init_app(app)
login_manager.login_message = "Veuiller vous connecter pour acceder aux autres pages"

from json import dumps
import logging
import os

from flask import (
    Flask,
    g,
    request,
    Response,
)
from neo4j import (
    GraphDatabase,
    basic_auth,
)






@app.route("/graph")
def get_graph():
    def work(tx, limit):
        return list(tx.run(
            "MATCH (m:PAPA)-[:Parenter]->(a:FRERE)"
            "MATCH (m:PAPA)-[:Parenter]->(s:SOEUR)"
            "MATCH (u:MAMAN)-[:Maman]->(s:SOEUR)"
            "RETURN m.prenom AS movie, collect(a.name) AS cast,collect(s.name) AS soeur "
            "LIMIT $limit",
            {"limit": limit}
        ))

   
    results = Session.read_transaction(work, request.args.get("limit", 100))
    print(results)
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["movie"], "label": "movie","prenom":record['soeur']})
        target = i
        i += 1
        for name in record["cast"]:
            actor = {"title": name, "label": "actor"}
            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
                source = i
                i += 1
            rels.append({"source": source, "target": target})
    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

################################# TRACER LES LIENS #############################################
def draw_graph(G, nodes_position, weight):
    nx.draw(G, nodes_position, with_labels=True, font_size=15,
            node_size=400, edge_color='gray', arrowsize=30)
    if weight:
        edge_labels=nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, nodes_position, edge_labels=edge_labels)






# ####################################### FONCTION ##############################################
#################################################################################################
def add(tx, name,prenom,telephone,email,adresse,profession,age,sexe,id):
    tx.run("create (a:Friends {name: $name,prenom: $prenom,telephone: $telephone,email: $email,adresse:$adresse,profession :$profession,age: $age,sexe: $sexe,id:$id}) return a",name=name,prenom=prenom,telephone=telephone,email=email,adresse=adresse,profession=profession,age=age,sexe=sexe,id=id)


def update(tx,id):
    tx.run(f"match(n:Friends) where n.id ={id} return n")

def deleted(tx,name):
    tx.run("match (a:Friends {name:$name}) DELETE a",name=name)


# ########################################### RECHERCHE ############################################
def find_and_return_person(tx, person_name):
        query = (
            "MATCH (a:Friends) "
            "WHERE a.prenom = $prenom "
            "RETURN a.prenom AS prenom"
        )
        result = tx.run(query, person_name=person_name)
        return [record["name"] for record in result]
def find_person(person_name):
        with driver.session() as session:
            result = session.read_transaction(find_and_return_person, person_name)
            for record in result:
                print("Found person: {record}".format(record=record))




# ########################################### CREATION API ###############################################
##########################################################################################################
@app.route('/update/<id>')
def update(id):
    try:
        with driver.session() as Session:
            Session.write_transaction(update,id)
            flash("Modifié avec succés")
    except Exception as e:
        print(e)
    return redirect(url_for('admin'))

# RECHERCHE TOUS LES NOEUDS
@app.route("/api/listes",methods=["GET","POST"])
def all_node():
    query="""
        match (n:Friends) return n
    """
    results = Session.run(query)
    data= results.data()
    return(jsonify(data))

# RECHERCHE PAR PRENOM
@app.route("/api/listes/<string:prenom>",methods=["GET","POST"])
def trouve_node(prenom):
    query="match (n:Friends {prenom:$prenom}) return n"
    results = Session.run(query,prenom=prenom)
    # print(results)
    data= results.data()
    # print(data)
    return(jsonify(data))

# SUPPRESSION D'UN USER
@app.route('/delete/<string:name>')
def delete(name):
    with driver.session() as Session:
        Session.write_transaction(deleted,name)    
    return redirect(url_for('creer_un_noeud'))


############################################## INSERTION UTILISATEURS ###################################
#########################################################################################################
@app.route("/create",methods=["GET","POST"])
def creer_un_noeud():
    if request.method == "POST":
        name      =request.form["name"]
        prenom    =request.form["prenom"]
        telephone =request.form["telephone"]
        email     =request.form["email"]
        adresse   =request.form["adresse"]
        profession=request.form["profession"]
        age       =request.form["age"]
        sexe      =request.form["sexe"]
        id        =request.form["id"]
        
        try:
            with driver.session() as Session:
                Session.write_transaction(add,name, prenom, telephone, email, adresse, profession,age,sexe,id)
                flash("Noeud ajouté avec succés")
        except Exception as e:
            print(e)
    return redirect(url_for('admin'))




# ################################################################################################
#                             FAIRE UN TCHAT
##################################################################################################
# from cache import client

def user_counter():
    sub = connect_to_redis.pubsub()
    sub.subscribe('usernames')
    for message in sub.listen():
        if message is not None and isinstance(message, dict):
            username = message.get('data')
        connect_to_redis.zincrby('username_scoreboard', 1, username)





def count():
    retry = 5
    while True:
        try:
            return connect_to_redis.incr('count')
        except redis.exceptions.ConnectionError as errcon:
            if retry == 0:
                raise errcon
            retry -= 1
            time.sleep(0.5)
@app.route('/message',methods=['GET','POST'])
def home():
    
    counting_page = count()
    # receive = connect_to_redis.subscribe("tchat")
    
    
    return redirect(url_for('admin',receive = counting_page))
    
import redis
import time
import traceback




# ################################################################################################
#           LA PAGE DE CONNEXION
##################################################################################################
@app.route('/',methods=["POST","GET"])
@login_manager.user_loader
def login():

    if request.method == 'POST':
        inputname = request.form['name']
        email= request.form['email']
        session['name'] = request.form['name']

        query="""
            match (n:Friends) return n
        """
        results = Session.run(query)
        data = results.data()
        
        emailList = []
        userList =[]
        Liste_sexes= []
        for d in range(len(data)):
            email = data[d]['n'].get('email')
            prenom = data[d]['n'].get('prenom')
            sexe = data[d]['n'].get('sexe')
            # print(sexe)
            
            id = data[d]['n'].get('id')
            emailList.append(email)
            userList.append(prenom)
            Liste_sexes.append(sexe)
        # print(Liste_sexes)
        if inputname == 'admin' or inputname in userList and email in emailList:
            return redirect(url_for('admin',name=current_user,sexes=Liste_sexes))
        else:
            flash('Les données rentrées sont incorrects')
    return render_template('connexion.html',current_user = current_user)

# ###################################################################################################
#                                           LA PAGE DE L'ADMIN
#####################################################################################################
@app.route('/admin')
def admin():
    # ARBRE
    G = nx.Graph()
    V = {'Paris', 'Dublin','Milan', 'Rome','babacar'}
    E = [('Paris','Dublin', 11), ('Paris','Milan', 8),('Milan','Rome', 5), ('Milan','Dublin', 19),('babacar','Milan',18)]
    G.add_nodes_from(V)
    G.add_weighted_edges_from(E)
    nodes_position = {"Paris": [0,0], "Dublin": [0,1], "Milan":[1,0], "Rome": [1,1],"babacar":[1,-1]}
    arbre = draw_graph(G, nodes_position, True)
    print(arbre)

    query="""
        match (n:Friends) return n
    """
    results = Session.run(query)
    data= results.data()
    liste ={}
    dico =[]
    for d in range(len(data)):
        
        liste.update({'name' : data[d].get('n').get('name'),
            'prenom' : data[d].get('n').get('prenom'),
            'email' : data[d].get('n').get('email'),
            'telephone' : data[d].get('n').get('telephone'),
            'adresse' : data[d].get('n').get('adresse'),
            'profession' : data[d].get('n').get('profession'),
            'age' : data[d].get('n').get('age'),
            'sexe' : data[d].get('n').get('sexe')})
        dico.append(liste)
    print(dico)
    if 'name' in session:
        name = session['name']
    return render_template('index.html',data=data,countData=len(data),dico=dico,countFriends=len(dico),current_user = name,arbre=arbre)

# ###################################################################################################
#                                                 LA PAGE DES USERS
#####################################################################################################
@app.route('/user')
def user():
    return render_template('user.html',user=current_user)

# ###################################################################################################
#                                                     LOGOUT
######################################################################################################
@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))

######################################################################################################"#"
#                                                     RECHERCHER 
########################################################################################################

@app.route('/recherche')
def recherche():
    if request.method == "POST":
        recherche = request.form['recherche']
        SearchPrenom =find_person(recherche)
        return redirect(url_for('admin',SearchPrenom))
    return redirect(url_for('admin')) 


if __name__ == "__main__":
    socketio.run(app)
    app.run(host="0.0.0.0", debug=True,port=5002)