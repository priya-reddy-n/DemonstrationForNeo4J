from flask import Flask, Response, request, render_template, jsonify
from py2neo import Graph,Node, Relationship
import pymongo
import json
import jsonpickle
from bson.objectid import ObjectId

app=Flask(__name__)

from neo4j import GraphDatabase

class Netflix:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

        
    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_read(self._create_and_return_greeting, message)
            print(greeting)
            return str(greeting)
        
    def getall(self, message):
        with self.driver.session() as session:
            greeting = session.execute_read(self._getall, message)
            print(greeting)
            return str(greeting)
        
    def getone(self, title):
        with self.driver.session() as session:
            greeting = session.execute_read(self._getone, title)
            print(greeting)
            return str(greeting)
        
    def insertone(self,title,show_id,types,director,cast,country,date_added,release_year,rating,duration,listed_in,description):
        with self.driver.session() as session:
            greeting = session.execute_write(self._insertone, title,show_id,types,director,cast,country,date_added,release_year,rating,duration,listed_in,description)
            print(greeting)
            return str(greeting)
        
    def updateone(self,fname,title,description,rating):
        with self.driver.session() as session:
            greeting = session.execute_write(self._updateone, fname,title,description,rating)
            print(greeting)
            return str(greeting)

    def deleteone(self,fname):
        with self.driver.session() as session:
            greeting = session.execute_write(self._deleteone, fname)
            print(greeting)
            return str(greeting)
        
        
    @staticmethod
    def _create_and_return_greeting(tx, message):
         collections_Data = []
         result = tx.run("MATCH (n) RETURN n", message=message)
         data=result.data()
         for movie_collection in data:
                collections_Data.append(movie_collection["n"])

         return collections_Data


    @staticmethod
    def _getall(tx, message):
         collections_Data = []
         result = tx.run("MATCH (n) RETURN n", message=message)
         data=result.data()
         for movie_collection in data:
                collections_Data.append(movie_collection["n"])

         return collections_Data
        

    @staticmethod
    def _getone(tx, title):
        
        query=("MATCH (a:Movie {title: '"+title+"'}) RETURN a")
        result = tx.run(query, message=title)
        return tuple(result)
       
    @staticmethod
    def _insertone(tx,title,show_id,types,director,cast,country,date_added,release_year,rating,duration,listed_in,description):
        query=("CREATE (n:Movie {title: '"+title+"', show_id: '"+show_id+"', rating:'"+rating+"', description:'"+description+"', release_year:'"+release_year+"',type:'"+types+"',duration:'"+duration+"',cast:"+cast+",country:"+country+",listed_in:"+listed_in+",date_added:'"+date_added+"',director:'"+director+"'})")
        result = tx.run(query, message=title)
        return "Created Successfully!!"
    
    @staticmethod
    def _updateone(tx, fname,title,description,rating):
        
        query=("MATCH (n:Movie {title: '"+fname+"'}) SET n.rating = '"+rating+"', n.title='"+title+"', n.description = '"+description+"' RETURN n.title")
        result = tx.run(query, message=fname)
        return "Updated Movie Successfully!!"

    @staticmethod
    def _deleteone(tx, fname):
        
        query=("MATCH (n:Movie {title: '"+fname+"'}) DELETE n")
        result = tx.run(query, message=fname)
        return "Deleted Movie Successfully!!"


    ####Retrieve all the movies and shows in database.
    @app.route('/title', methods=['GET'])
    def getmovie():
        try:
            result= greeter.getall("hey")
            #ans=jsonify(result)
            return Response(result.lstrip())
            
        except Exception as ex:
            return ex

    ###Display the movie and show’s detail includes actors, directors and distributed country using title
    @app.route('/title/<string:fname>', methods=['GET'])
    def getmoviedetailsbytitle(fname):
     try:
        
        result=greeter.getone(fname)
        return Response(result)
     except Exception as ex:
        response = Response("From GetMovieByTitle - No movies found in colletion",status=500,mimetype='application/json')
        return ex

    ###Insert the new movie and show
    @app.route('/title', methods=['POST'])
    def addmovie():
      try:
        data = request.get_json()
        
        title=data["title"]
        show_id=data["show_id"]
        types=data["type"]
        director=data["director"]
        cast=data["cast"]
        country=data["country"]
        date_added=data["date_added"]
        release_year=data["release_year"]
        rating=data["rating"]
        duration=data["duration"]
        listed_in=data["listed_in"]
        description=data["description"]


        result=greeter.insertone(str(title),str(show_id),str(types),str(director),cast,country,str(date_added),str(release_year),str(rating),str(duration),listed_in,str(description))
        return Response(result)
      except Exception as ex:
        response = Response("From AddMovie - No movies found in colletion",status=500,mimetype='application/json')
        return response


    ###Update the movie and show information using title. (By update only title, description, and rating)
    @app.route('/title/<string:fname>', methods=['PATCH'])
    def updatemovie(fname):
      try:
          data = request.get_json()
        
          title=data["title"]
          rating=data["rating"]
          description=data["description"]
          result=greeter.updateone(fname,str(title),str(description),str(rating))
          return Response(result)
       
      except Exception as ex:
        response = Response("From DeleteMovie - No movies found in colletion",status=500,mimetype='application/json')
        return response


    ###Delete the movie and show information using title
    @app.route('/title/<string:fname>', methods=['DELETE'])
    def deletemovie(fname):
      try:
          result=greeter.deleteone(fname)
          return Response(result)
       
      except Exception as ex:
        response = Response("No movies found in colletion",status=500,mimetype='application/json')
        return response



    ###########################################################################################       
    ##Connected to AuraDB hosted on cloud

if __name__ == "__main__":
    greeter = Netflix("neo4j+s://13506786.databases.neo4j.io", "neo4j", "_YCXF6SJI-SHpRAjruku36cSDXZ82cxme-5ypmiaDpI")
    app.run(port=5001, debug=True)



