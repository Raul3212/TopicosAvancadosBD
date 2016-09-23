create table vertices (id_vertice integer primary key, latitude float, longitude float)
create table rotas(id_edge integer primary key, id_source integer, id_target integer, cost float, FOREIGN KEY (id_source) references vertices (id_vertice), FOREIGN KEY (id_target) references vertices (id_vertice))
create table taxistas (id_driver integer, tempo timestamp, longitude float, latitude float)