import mysql.connector as conn
from mysql.connector import Error
#from dicttoxml import dicttoxml
from dict2xml import dict2xml


# END of Import

#class for RDF File Database access
class db_connector:
    def get_connection(self):
        try:
            connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
            if connection.is_connected():
                print("Connection success")
                return connection
            else:print("No Connection!")
        except Error as e:
            print("Connection problem",e)
#get all Entrys from the database Table (for Headder only)
    def get_header_info(self):
        connection = db_connector.get_connection(0)
        read_cursor = connection.cursor()
        read_cursor.execute(" SELECT * FROM entry")
        rows = read_cursor.fetchone()
        ontology_list = []
        while rows is not None:
            print(rows)
            ontology_list.append(rows[0])
            rows = read_cursor.fetchone()
        return ontology_list
#get all Entrys from the Database Table( for Body only)
    def get_body_info(self):
        connection = db_connector.get_connection(0)
        read_cursor = connection.cursor()
        read_cursor.execute(" SELECT * FROM entry")
        rows = read_cursor.fetchone()
        ontology_list = []
        while rows is not None:
            ontology_list.append(rows)
            rows = read_cursor.fetchone()
        return ontology_list
    def get_about(self):
        connection = db_connector.get_connection(0)
        read_cursor = connection.cursor()
        read_cursor.execute(" SELECT * FROM about")
        return read_cursor.fetchone()
#get the Reference of Ontology that use in the RDF File
    def get_references(self):
        try:
          list = []
          connection = db_connector.get_connection(0)
          read_cursor = connection.cursor()
          read_cursor.execute(" SELECT * FROM ontology")
          rows = read_cursor.fetchone()
          while rows is not None:
              list.append(rows)
              rows = read_cursor.fetchone()
          return list
        except Error as e:
            print("Error reading References",e)










#class for creating header by ontology
class header_creator:
    def header_bilder(self):
        header = ""
        header += "<?xml version=" +'"'+ str(1.0) + '"'+ "?>\n"
        header += "<rdf:RDF \n"
        header += "    xmlns:rdf='""http://www.w3.org/1999/02/22-rdf-syntax-ns'" + "\n"
        header += ""
        if header_creator.if_ontology_exist('nmo'):
            header += "    xmlns:nmo='""http://nomisma.org/ontology#'" + "\n"
        if header_creator.if_ontology_exist('skos'):
            header += "    xmlns:skos='""http://www.w3.org/2004/02/skos/core#'" + "\n"
        if header_creator.if_ontology_exist('meta'):
            header += "    xmlns:meta='""http://www4.wiwiss.fu-berlin.de/bizer/d2r-server/metadata#'" + "\n"
        if header_creator.if_ontology_exist('foaf'):
            header += "    xmlns:foaf='""http://xmlns.com/foaf/0.1/'" + "\n"
        if header_creator.if_ontology_exist('xsd'):
            header += "    xmlns:xsd='""http://www.w3.org/2001/XMLSchema#'" +"\n"
        if header_creator.if_ontology_exist('owl'):
            header += "    xmlns:owl='""http://www.w3.org/2002/07/owl#'" + ""
        header += ">" + "\n"
        print(header)
        return header
#check if the entry have his ontology
    def if_ontology_exist(ontology):
       ontology_list =  db_connector.get_header_info(0)
       for i in ontology_list:
           if (i.find(str(ontology))) == 0:
               return True
       return False
#create the file directory(for headder only)
    def hedder(self):
        file = open("xmlFile.xml","w+")
        file.write(header_creator.header_bilder(0))
        file.close()



#class for creating the rest of the file
class body:
    def body_writer(self):
        file = open("xmlFile.xml","a")
        file.write(body.body_bilder(0))
        file.write(body.body_close(0))
        file.close()

#method create the givin entry
    def body_bilder(self):
        forbidden_list = []
        body = ""
        body += "  <rdf:Description rdf:about="+'"#'+str(db_connector.get_about(0)[0]) +'"'+">\n"
        entrys = db_connector.get_body_info(0)
        references = db_connector.get_references(0)
        for i in entrys:
            for j in references:
                if(str(i[0]) == str(j[1])):
                    if(i[0] not in forbidden_list):
                        body+= "    <"+i[0]+ " " +j[2] + "=" + '"' + i[3] + '"' + "/>\n"
                    else:
                      print("ok, item in forbidden_list")
        body +="  </rdf:Description>" + "\n"
        body +="\n"
        return body

#for closing the file (not Finished!)
    def body_close(self):
        body = "\n \n"
        body ="</rdf:RDF>" + "\n"
        return body
# for rewrite the file (still open!)
    def body_close_remove(self):
        file = open("xmlFile.xml","r")
        ready_file = file.read()[:-11]
        return ready_file






header_creator.hedder(0)
body.body_writer(0)
body.body_bilder(0)
#body.body_close_remove(0)
