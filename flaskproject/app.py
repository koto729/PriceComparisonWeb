from flask import Flask, render_template, request, jsonify, g, url_for, redirect, session
import mysql.connector

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='ko.wingto.11@gmail.com', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']


        if username == "ko.wingto.11@gmail.com" and password == password:
            session['user_id'] = 1
            return redirect(url_for('/'))

        return redirect(url_for('login'))

    return render_template('test2.html')

# Connect to MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="webscraper"
)
cursor = cnx.cursor()

# Define a route for displaying product data


@app.route('/')
def home():

    cursor.execute("SELECT product_name, price, date, type_id, supermarket_id FROM productprice")

    product = cursor.fetchall()

    return render_template('index.html', products=product)

@app.route('/products', methods=['GET', 'POST'])
def products():
    type_id = request.args.get('type_id', 1)

    query = "SELECT date FROM productprice WHERE type_id = %s AND supermarket_id = %s ORDER BY date"
    cursor.execute(query, (type_id, 1,))
    date = cursor.fetchall()

    query = "SELECT product_name, price, date, type_id, supermarket_id FROM productprice WHERE type_id = %s AND supermarket_id = %s ORDER BY date"
    cursor.execute(query, (type_id, 1,))
    product1 = cursor.fetchall()

    query = "SELECT product_name, price, date, type_id, supermarket_id FROM productprice WHERE type_id = %s AND supermarket_id = %s ORDER BY date"
    cursor.execute(query, (type_id, 2,))
    product2 = cursor.fetchall()

    query = "SELECT product_name, price, date, type_id, supermarket_id FROM productprice WHERE type_id = %s AND supermarket_id = %s ORDER BY date"
    cursor.execute(query, (type_id, 3,))
    product3 = cursor.fetchall()

    #rank function
    query = "SELECT supermarket.name,productprice.price " \
            "FROM productprice " \
            "JOIN supermarket ON productprice.supermarket_id = supermarket.id WHERE productprice.type_id = %s AND date = (SELECT MAX(date) FROM productprice) ORDER BY productprice.price ASC"

    cursor.execute(query, (type_id,))
    rank = cursor.fetchall()
    if len(rank) < 3:
        rank2 = rank[1]
        rank1 = rank[0]
        rank3 = [0,0]
    elif rank[0][1] == 0:
        rank3 = list(rank[0])
        rank3[1] = "sold"
        rank3 = tuple(rank3)
        rank2 = rank[2]
        rank1 = rank[1]
    else:
        rank3 = rank[2]
        rank2 = rank[1]
        rank1 = rank[0]

    if request.method == 'POST':
        email = request.form['email']
        price = request.form['price']

        query = "INSERT INTO pricealerts (type_id, email, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (type_id, email, price,))
        cnx.commit()

    return render_template('products1.html', date=date, product1=product1, product2=product2, product3=product3, rank3=rank3, rank2=rank2, rank1=rank1)



if __name__ == '__main__':
    app.run(debug=True)