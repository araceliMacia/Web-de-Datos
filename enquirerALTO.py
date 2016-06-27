"""
@author: U{Nines Sanguino}
@version: 0.2
@since: 20Jun2015
"""

__version__ = '0.2'
__modified__ = '20Jun2015'
__author__ = 'Nines Sanguino'
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDF
import xml.dom.minidom
OutFile=open('OutEnquire.txt','w')


def InsertarDatosRepositorio(sqlinsertar):

	#print "entrando en la funcion"
	#print sqlinsertar
	sparqlSesame = SPARQLWrapper("http://localhost:8080/openrdf-workbench/repositories/SocialNetwork/update",  returnFormat=XML)
	sparqlSesame.setQuery(sqlinsertar)
	sparqlSesame.method = 'POST'
	sparqlSesame.setReturnFormat(XML) #lo devuelvo en XML porque en JSON devuelve un warning
	OutFile.write("        ** Insertando valores en Sesamo **\n")
	OutFile.write("        > " + sqlinsertar +" \n")
	OutFile.write("\n")
	query   = sparqlSesame.query()
	results = query.convert()
	




def getLocalLabel (instancia):
 
 	#consulta el repositorio de sesame para obtener los datos de la instancia que se le pasa por parametro
 	sparqlSesame = SPARQLWrapper("http://localhost:8080/openrdf-sesame/repositories/SocialNetwork",  returnFormat=JSON)
	queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX sn:  <http://ciff.curso2015/ontologies/owl/socialNetwork#> SELECT ?label WHERE { sn:" + instancia + " rdfs:label ?label }"
	sparqlSesame.setQuery(queryString)
	sparqlSesame.setReturnFormat(JSON)
	query   = sparqlSesame.query()
	results = query.convert()
	devolver = []
	for result in results["results"]["bindings"]:
		label = result["label"]["value"]
		if 'xml:lang' in result["label"]:
			lang = result["label"]["xml:lang"]
		else:
			lang = None
		#print "The label: " + label
		#if 'xml:lang' in result["label"]:
		#	print "The lang: " + lang
		devolver.append((label, lang))
	return devolver


	
def getDBpediaResource (label, lang, endpoint):

	if (lang):
		OutFile.write("#########  INSTANCIA 1 ##### DATOS :" +  label + " Y " + lang + "\n")		
	else:
		OutFile.write("#########  INSTANCIA 1 ##### DATOS :" +  label + "\n")		 

	sparqlDBPedia = SPARQLWrapper(endpoint)
	if (lang):
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"@" +lang + " . ?s rdf:type foaf:Person} " 
	else:
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\" . ?s rdf:type foaf:Person } " 
	#print queryString 

	
	sparqlDBPedia.setQuery(queryString)
	sparqlDBPedia.setReturnFormat(JSON)
	query   = sparqlDBPedia.query()
	results = query.convert()
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		OutFile.write ("Encontrado The resource: " + resource  + "\n")
		
		#Estoy interesada en saber cuales son las propiedades que tienen relacion con la wikipedia.
		
		sqlWiki="PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
		sqlWiki=sqlWiki+"PREFIX foaf: <http://xmlns.com/foaf/0.1/> "
		sqlWiki=sqlWiki+"SELECT ?p ?o WHERE {  <" + resource + "> ?p ?o FILTER regex(str(?o), \"wikipedia\") }"
 		#print sqlWiki
 		sparqlDBPedia.setQuery(sqlWiki)
		sparqlDBPedia.setReturnFormat(JSON)
		query   = sparqlDBPedia.query()
		resultados = query.convert()
		for res in resultados["results"]["bindings"]:
			tipo = res["p"]["value"]
			valor = res["o"]["value"]
			OutFile.write( "   - propiedad :" +  tipo + " valor :" + valor  + "\n")
			#construyo la sql a insertar. Conozco los datos de la instancia a rellenar,y que lo que voy a insertar son URL en 
			#funcion de esto construyo la sentencia "
			sqlinsertar="PREFIX sn:  <http://ciff.curso2015/ontologies/owl/socialNetwork#> "
			sqlinsertar=sqlinsertar + "PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#> "
			sqlinsertar=sqlinsertar + " INSERT DATA { GRAPH sn: {  sn:instancia1 "
			sqlinsertar=sqlinsertar + "<" + tipo + ">  <" + valor + "> } }"
			rdofuncion = InsertarDatosRepositorio(sqlinsertar);




def getLinkedmdbResource (label, lang, endpoint):
 	
 	if (lang):
		OutFile.write( "#########  INSTANCIA 3 ##### DATOS :" +  label + " Y " + lang + "\n")
	else:
		OutFile.write( "#########  INSTANCIA 3 ##### DATOS :" +  label + "\n")

	PrefixString="PREFIX owl: <http://www.w3.org/2002/07/owl#>"
	PrefixString=PrefixString+"PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"
	PrefixString=PrefixString+"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
	PrefixString=PrefixString+"PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
	PrefixString=PrefixString+"PREFIX db: <http://data.linkedmdb.org/resource/>"
	PrefixString=PrefixString+"PREFIX movie: <http://data.linkedmdb.org/resource/movie/>"
	PrefixString=PrefixString+"PREFIX lang: <http://www.lingvoj.org/lingvo/>"


	sparqlLinkedmdb = SPARQLWrapper(endpoint)

	#"SELECT ?s WHERE { ?s rdfs:label "Batman" } " sin idioma
	#SELECT ?s WHERE { ?s rdfs:label "Batman" .?s movie:language lang:en}  con idioma

	if (lang):
		queryString = PrefixString +  "SELECT ?s WHERE { ?s rdfs:label \"" + label + "\". ?s movie:language lang:"+ lang +"}" 	
									 
	else:
		queryString = PrefixString + "SELECT ?s WHERE { ?s rdfs:label \"" + label + "\" }  " 
	 
	#print queryString

	sparqlLinkedmdb.setQuery(queryString)
	sparqlLinkedmdb.setReturnFormat(JSON)
	query   = sparqlLinkedmdb.query()
	results = query.convert()
	i = 0
	for result in results["results"]["bindings"]:
		i= i+1
		resource = result["s"]["value"]
		OutFile.write( "Encontrado ->The resource: " + resource +"\n")
		#En cada recurso acceder a mostrar las propiedades que sean literales.
		sqlDatos=PrefixString + "SELECT ?s ?p ?o WHERE { <" + resource+ ">  ?p  ?o FILTER ( ISLITERAL(?o)) } "
 		#print queryString 				
		sparqlLinkedmdb.setQuery(sqlDatos)
		sparqlLinkedmdb.setReturnFormat(JSON)
		query   = sparqlLinkedmdb.query()
		resultado = query.convert()
		#print "-> Datos de :>" + resource
		for res in resultado["results"]["bindings"]:
			tipo = res["p"]["value"]
			valor = res["o"]["value"]
			OutFile.write( "   - propiedad :" +  tipo + " valor :" + valor + "\n")
			if (i==1): #solo inserto los datos en sesame del primer recurso encontrado
				sqlinsertar="PREFIX sn:  <http://ciff.curso2015/ontologies/owl/socialNetwork#> "
				sqlinsertar=sqlinsertar + "PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#> "
				sqlinsertar=sqlinsertar + " INSERT DATA { GRAPH sn: { sn:instancia3 "
				sqlinsertar=sqlinsertar + "<" + tipo + ">  \"" + valor + "\" } }"
				rdofuncion = InsertarDatosRepositorio(sqlinsertar);
	

def getWebenemasunoResource (label, lang, endpoint):

	if (lang):
		OutFile.write( "#########  INSTANCIA 4 ##### DATOS :" +  label + " Y " + lang + "\n")
	else:
		OutFile.write( "#########  INSTANCIA 4 ##### DATOS :" +  label + "\n")
	
	PrefixString="PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
	PrefixString=PrefixString+ "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" 
	PrefixString=PrefixString+ "PREFIX opmopviajero: <http://webenemasuno.linkeddata.es/ontology/OPMO/>"
	PrefixString=PrefixString+ "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"

    
	#SELECT ?s WHERE { ?s sioc:title "Un vino cosmopolita"  }   Sin Idioma
 	#SELECT ?s  WHERE { ?s sioc:title "Un vino cosmopolita" . ?s opmopviajero:language "es"}  con idioma

	sparqlWebenemasuno = SPARQLWrapper(endpoint)
	if (lang):
		queryString = PrefixString + "SELECT ?s WHERE { ?s sioc:title \"" + label + "\". ?s opmopviajero:language \""+lang+"\"} " 
	else:
		queryString = PrefixString + "SELECT ?s WHERE { ?s sioc:title \"" + label + "\" }  " 
	
	#print queryString
	sparqlWebenemasuno.setQuery(queryString)
	sparqlWebenemasuno.setReturnFormat(JSON)
	query   = sparqlWebenemasuno.query()
	results = query.convert()

	#de este articulo lo que me interesa es el creador.	
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		OutFile.write( "->The resource: " + resource+ "\n")
		sqlDatos=PrefixString + "SELECT  ?creador WHERE {<" + resource + ">sioc:has_creator ?creador } "
 		#print queryString 				
		sparqlWebenemasuno.setQuery(sqlDatos)
		sparqlWebenemasuno.setReturnFormat(JSON)
		query   = sparqlWebenemasuno.query()
		resultado = query.convert()
		#print "-> Datos de :>" + resource
		for res in resultado["results"]["bindings"]:
			valor = res["creador"]["value"]
			OutFile.write("   - Creador es  :" + valor + "\n")
			sqlinsertar="PREFIX sn:  <http://ciff.curso2015/ontologies/owl/socialNetwork#> "
			sqlinsertar=sqlinsertar + "PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#> "
			sqlinsertar=sqlinsertar + "PREFIX sioc: <http://rdfs.org/sioc/ns#>"
			sqlinsertar=sqlinsertar + " INSERT DATA { GRAPH sn: { sn:instancia4 "
			sqlinsertar=sqlinsertar + "sioc:has_creator  <" + valor + "> } }"
			rdofuncion = InsertarDatosRepositorio(sqlinsertar);
	
		

if __name__ == '__main__':

	# getLocalLabel devuelve una lista con todas las instancias que haya con sus label y lang
	# y luego se hace la llamada al repositorio externo para enriquecer cada combinacion de label-lang recibida
	lista = getLocalLabel("instancia1");
	#print  lista
	endpoint = 'http://dbpedia.org/sparql';
	for result in lista:
		(label, lang) = result
		resource = getDBpediaResource (label, lang, endpoint);

	OutFile.write("\n---------------------------------------------------------\n")
	
	# Descomentar las siguientes lineas y modificar en cada 
	lista = getLocalLabel("instancia3");
	#print lista
	#por la web me ha dejado con esta: http://www.linkedmdb.org/snorql/?
	endpoint = 'http://data.linkedmdb.org/sparql';

	for result in lista:
		(label, lang) = result
		resource = getLinkedmdbResource (label, lang, endpoint);

	OutFile.write("\n---------------------------------------------------------\n")

	lista = getLocalLabel("instancia4");
	#print lista
	endpoint = 'http://webenemasuno.linkeddata.es/sparql';
	for result in lista:
		(label, lang) = result
		resource = getWebenemasunoResource (label, lang, endpoint);

	OutFile.close()  #cierro fichero de salida.
	

		
