from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="webscraper"
)
cursor = cnx.cursor()


query = "INSERT INTO pricealerts (type_id, email, price) VALUES (1, 'zxc', 3)"

cursor.execute(query)
cnx.commit()
