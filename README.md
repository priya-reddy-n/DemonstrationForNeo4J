# DemonstrationForNeo4J

This is the API to perform at most functions on web applications. Developed the backend web framework using Python.
The backend application connected to Neo4j-a graph DBMS developed by Neo4j, inc. (https://neo4j.com).
To test the backend web framework, you must use API platforms such as Postman API Platform(https://www.postman.com).
The CSV file (netflix_titles.csv-Movie and Show on Netflix) is provided with the column names including: 
show_id
type
title
director
cast
country
date_added
release_year
rating
duration
description

First, setup Neo4j Database on local and cloud using Neo4j Desktop and Neo4j Aura(https://console.neo4j.io) and import this csv file to create graph database on Neo4j DBMS. 


API: Implemented the following in the API
1.	Insert the new movie and show. 
@app.route('/title', methods=['POST'])

2.	Update the movie and show information using title. (By update only title, description, and rating)
@app.route('/title/<string:fname>', methods=['PATCH'])

3.	Delete the movie and show information using title.
@app.route('/title/<string:fname>', methods=['DELETE'])

4.	Retrieve all the movies and shows in database.
@app.route('/title', methods=['GET'])

5.	Display the movie and show’s detail includes actors, directors and distributed country using title.
@app.route('/title/<string:fname>', methods=['GET'])


