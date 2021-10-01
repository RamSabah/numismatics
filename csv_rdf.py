import csv
from decimal import *
from rdflib.graph import Graph
from csvwlib import CSVWConverter as GG
from rdflib import URIRef, BNode, Literal, Namespace
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO,OWL
from rdflib.namespace import NamespaceManager

def csvReader():
    csv_file = open("csv/query_OCRE.csv",'r')
    csv_content = csv.reader(csv_file,delimiter=',')

    header = csv_content.__next__()
    print(header)
    print(len(header))

    for row in csv_content:
        print(row)

    print("Done")
    return True

csvReader()
print('________________')
class RDF_BILD():

    def bilder(self):
        csv_file = open("csv/query_OCRE.csv",'r')
        csv_content = csv.reader(csv_file, delimiter=',')
        header = csv_content.__next__()


        G = Graph()
        G.bind('foaf',FOAF)
        G.bind('dcterms',DCTERMS)
        G.bind('nmo','http://nomisma.org/ontology')
        G.bind('owl',OWL)
        G.bind('un','http://www.owl-ontologies.com/Ontology1181490123.owl')
        G.bind('nm','http://nomisma.org/id/')
        NMO = Namespace('http://nomisma.org/ontology/')
        UN = Namespace('http://www.owl-ontologies.com/Ontology1181490123.owl')
        NM = Namespace('http://nomisma.org/id/')
        for row in csv_content:
            G.add((URIRef(row[0]),DCTERMS['identifier'],Literal(row[2])))
            G.add((URIRef(row[0]),DCTERMS['title'],Literal(row[1],lang='en')))
            if(row[12] ==''):
                G.add((URIRef(row[0]),UN['hasUncertainty'],NM['uncertain_value']))
            else:
                G.add((URIRef(row[0]),NMO['hasDiameter'],Literal(Decimal(float(row[12])),datatype='decimal')))
            G.add((URIRef(row[0]),NMO['hasAxis'],Literal(row[11],datatype='integer')))
            G.add((URIRef(row[0]), NMO['hasWeight'], Literal(row[10], datatype='decimal')))


        print(G.serialize(format='xml'))
        Query = " SELECT ?subject ?pradicate ?object WHERE { ?subject ?pradicate ?object} "
        query_resault = G.query(Query)
        for i in query_resault:
            print(i['subject'],"  ", i['pradicate'],"  ",i['object'])

        return G.serialize(format('xml'))

RDF_BILD.bilder(0)