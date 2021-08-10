import json

import mysql.connector as conn
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
from boltiot import Bolt
import cgi
import re
from urllib.parse import urlparse
from flask import Flask, render_template, request, url_for, redirect, jsonify


class db_conn:
   def insert(name_,description_):
    try:
        connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
        if connection.is_connected():
            print("For Write connected" )

            write_cursor = connection.cursor()
            statment = "INSERT INTO nomisma(name ,description) VALUES(%s,%s)"
            values = (str(name_),str(description_))
            write_cursor.execute(statment,values)
            connection.commit()

    except Error as ar:
        print("Error accured", ar)

   def insert_as_selected(name,discription,id):
       try:
           connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
           if connection.is_connected():
               print("For Write connected")

               write_cursor = connection.cursor()
               statment = "INSERT INTO entry(nomName,nomDisc,nomID) VALUES(%s,%s,%s)"
               values = (str(name),str(discription),id)
               write_cursor.execute(statment, values)
               connection.commit()

       except Error as ar:
           print("Error accured", ar)

       return True

   def read(self):
       connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
       if connection.is_connected():
           print("For read Connected")

       read_cursor = connection.cursor()
       statment = " SELECT * FROM nomisma "
       read_cursor.execute(statment)
       rows = read_cursor.fetchone()
       dataSet = []
       while rows is not None:
           dataSet.append(rows)
           rows = read_cursor.fetchone()

       return dataSet

   def read_entrys(self):
       connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
       if connection.is_connected():
           print("For read Connected")

       read_cursor = connection.cursor()
       statment = " SELECT * FROM entry "
       read_cursor.execute(statment)
       rows = read_cursor.fetchone()
       dataSet = []
       while rows is not None:
           dataSet.append(rows)
           rows = read_cursor.fetchone()

       return dataSet

   def clear_selection(self):
       connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
       if connection.is_connected():
           print("For Clear connected!")
           delete_cursor= connection.cursor()
           delete_cursor.execute(" DELETE FROM entry ")
           delete_cursor.execute(" DELETE FROM about")
           connection.commit()
           print('Deleted')
   def add_id(id_):
       try:
           connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
           if connection.is_connected():
               print("For Write connected")
               write_cursor = connection.cursor()
               statment = """INSERT INTO id(link) VALUES(%s)"""
               write_cursor.execute(statment,(id_,))
               connection.commit()

       except Error as ar:
           print("Error accured", ar)

       return True

   def getConnection(self):
       connection = conn.connect(host='127.0.0.1', database='maria', user='root', password='admin')
       if connection.is_connected():
           print("connected")
           return connection
   def get_id(self):
       try:
          connection = db_conn.getConnection(0)
          read_cursor = connection.cursor()
          read_cursor.execute(" SELECT * FROM id")
          rows = read_cursor.fetchone()
          list = []
          while rows is not None:
              list.append(rows)
              rows = read_cursor.fetchone()
          return list
       except Error as e:
           print("Error accurd!",e)

   def insert_id_link(nomName,nomID):
       try:
           connection = db_conn.getConnection(0)
           write_cursor = connection.cursor()
           statment = "UPDATE entry SET checknomIDLink = %s WHERE nomName like %s"
           values = (nomID,"%"+nomName+"%")
           write_cursor.execute(statment,values)
           connection.commit()
       except Error as e:
           print("An error has been accurd",e)

   def about(name_):
       try:
           connection = db_conn.getConnection(0)
           write_cursor = connection.cursor()
           statment = """INSERT INTO about(name) VALUES(%s)"""
           write_cursor.execute(statment,(name_,))
           connection.commit()

       except Error as e:
              print("Error accurd",e)


   def get_about(self):
       try:
           connection = db_conn.getConnection(0)
           read_cursor = connection.cursor()
           read_cursor.execute("SELECT * FROM about")
           about = read_cursor.fetchone()
       except Error as e:
              print("Error accur while retrieving about", e)
       return about

   def insert_Reference(name,reference):
       connection = db_conn.getConnection(0)
       write_cursor = connection.cursor()
       statment = statment = "INSERT INTO ontology(name,link) VALUES(%s,%s)"
       write_cursor.execute(statment,(name,reference))
       connection.commit()







# END of CLASS DB_Connection



# BEGIN of Method


app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        pass
    #db_conn.insert(3,'coin_3')
    names = db_conn.read(0)
    entrys = db_conn.read_entrys(0)
    id_list = db_conn.get_id(0)
    about = db_conn.get_about(0)

    return render_template('index.html',name=names,entrys=entrys,id_list = id_list,about = about)


@app.route('/add',methods=['GET','POST'])
def add():
     if request.method == 'POST':
         name = request.form['nomName']
         nameDisc = request.form['nomDisc']
         db_conn.insert(name,nameDisc)

     return render_template('add.html')

@app.route("/add_name",methods=['GET','POST'])
def add_name():
    if request.method== 'POST':
        name = request.form['pressd']
        discription = request.form['pressd_non']
        id = request.form['pressd_id']
        print(name)
        db_conn.insert_as_selected(name,discription,id)
    return index()


@app.route("/add_id",methods=['GET','POST'])
def add_id():
    if request.method =='POST':
        id = request.form['id_']
        db_conn.add_id(id)
        print('id added')
    return render_template('id.html')


@app.route("/rdfReference",methods=['GET','POST'])
def rdfReference():
    if request.method == 'POST':
        name = request.form['objectName']
        reference = request.form['objectReference']
        db_conn.insert_Reference(name,reference)
    return render_template('rdfReference.html')

@app.route("/clear_selection", methods=['GET','POST'])
def clear_selection():
    if request.method == 'GET':
        db_conn.clear_selection(0)
        print("Selection Cleard")
    return index()

@app.route("/pass_id_link", methods=['POST','GET'])
def pass_id_link():
    id = request.form['pressd_for_id']
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', id)
    clean_url = str(urls)[1:-1].replace(",","").replace('"',"").replace("'","")
    print(len(urls))
    print(type(urls))
    str_ = ""
    for i in clean_url:
        str_ += i
    print(len(str_))
    print(len(str_))
    nomID = str_
    nomName = id[len(str_)+2+5:-2]
    print(id[38+2+5:-2])
    db_conn.insert_id_link( nomName , nomID)
    return index()

@app.route("/about",methods=['GET','POST'])
def about():
    if request.method == 'POST':
        button_id = request.form['about_button']
        about_input = request.form['about']
        db_conn.about(about_input)
        return index()

@app.route('/add_id_byEnter/<string:name_>/<int:counter>',methods=['POST'])
def add_id_byEnter(name_,counter):
    if request.method == 'POST':
       nomName = str(name_)
       nomInput = "counter" + str(counter)
       input = request.form[nomInput]
       db_conn.insert_id_link(nomName,input)

    return index()

if __name__ =="__main__":
    app.run(debug=True)

