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
		print "The label: " + label
		if 'xml:lang' in result["label"]:
			print "The lang: " + lang
		devolver.append((label, lang))
	return devolver


	
def getDBpediaResource (label, lang, endpoint):

	sparqlDBPedia = SPARQLWrapper(endpoint)
	if (lang):
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"@" +lang + " . ?s rdf:type foaf:Person} " 
	else:
		queryString = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT ?s WHERE { ?s rdfs:label \"" + label + "\" . ?s rdf:type foaf:Person } " 
	
	
	sparqlDBPedia.setQuery(queryString)
	sparqlDBPedia.setReturnFormat(JSON)
	query   = sparqlDBPedia.query()
	results = query.convert()
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		print "The resource: " + resource

def getLinkedmdbResource (label, lang, endpoint):

	PrefixString="PREFIX owl: <http://www.w3.org/2002/07/owl#>"
	PrefixString=PrefixString+"PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"
	PrefixString=PrefixString+"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
	PrefixString=PrefixString+"PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
	PrefixString=PrefixString+"PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
	PrefixString=PrefixString+"PREFIX oddlinker: <http://data.linkedmdb.org/resource/oddlinker/>"
	PrefixString=PrefixString+"PREFIX map: <file:/C:/d2r-server-0.4/mapping.n3#>"
	PrefixString=PrefixString+"PREFIX db: <http://data.linkedmdb.org/resource/>"
	PrefixString=PrefixString+"PREFIX dbpedia: <http://dbpedia.org/property/>"
	PrefixString=PrefixString+"PREFIX skos: <http://www.w3.org/2004/02/skos/core#>"
	PrefixString=PrefixString+"PREFIX dc: <http://purl.org/dc/terms/>"
	PrefixString=PrefixString+"PREFIX movie: <http://data.linkedmdb.org/resource/movie/>"


	sparqlLinkedmdb = SPARQLWrapper(endpoint)

	if (lang):
		queryString = PrefixString +  "SELECT ?s WHERE { ?s rdfs:label \"" + label + "\"@" +lang + "} " 	
									 
	else:
		queryString = PrefixString + "SELECT ?s WHERE { ?s rdfs:label \"" + label + "\" }  " 
	 
	print queryString 
	sparqlLinkedmdb.setQuery(queryString)
	sparqlLinkedmdb.setReturnFormat(JSON)
	query   = sparqlLinkedmdb.query()
	results = query.convert()
	print
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		print "->The resource: " + resource
		

def getWebenemasunoResource (label, lang, endpoint):

	PrefixString="PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
	PrefixString=PrefixString+ "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" 
	PrefixString=PrefixString+ "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"

	#SELECT ?s WHERE { ?s sioc:title "Un vino cosmopolita"  }  


	sparqlWebenemasuno = SPARQLWrapper(endpoint)
	if (lang):
		queryString = PrefixString + "SELECT ?s WHERE { ?s sioc:title \"" + label + "\"@" +lang + "} " 
	else:
		queryString = PrefixString + "SELECT ?s WHERE { ?s sioc:title \"" + label + "\" }  " 
	
	sparqlWebenemasuno.setQuery(queryString)
	sparqlWebenemasuno.setReturnFormat(JSON)
	query   = sparqlWebenemasuno.query()
	results = query.convert()
	print
	for result in results["results"]["bindings"]:
		resource = result["s"]["value"]
		print "->The resource: " + resource
		

if __name__ == '__main__':

	# getLocalLabel devuelve una lista con todas las instancias que haya con sus label y lang
	# y luego se hace la llamada al repositorio externo para enriquecer cada combinacion de label-lang recibida
	lista = getLocalLabel("instancia1");
	print  lista
	endpoint = 'http://dbpedia.org/sparql';
	for result in lista:
		(label, lang) = result
		resource = getDBpediaResource (label, lang, endpoint);

	print "\n---------------------\n"
	
	# Descomentar las siguientes lineas y modificar en cada 
	lista = getLocalLabel("instancia3");
	print lista
	#por la web me ha dejado con esta: http://www.linkedmdb.org/snorql/?
	endpoint = 'http://data.linkedmdb.org/sparql';

	for result in lista:
		(label, lang) = result
		resource = getLinkedmdbResource (label, lang, endpoint);

	print "\n---------------------\n"

	lista = getLocalLabel("instancia4");
	print lista
	endpoint = 'http://webenemasuno.linkeddata.es/sparql';
	for result in lista:
		(label, lang) = result
		resource = getWebenemasunoResource (label, lang, endpoint);
	

		
