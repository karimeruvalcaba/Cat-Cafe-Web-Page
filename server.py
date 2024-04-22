from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_secret_key'  

CORS(app)

# Simulated user data (replace this with your actual user authentication logic)
valid_username = "admin"
valid_password = "mypass"


def connect_db():
    conn = sqlite3.connect('CatData.sqlite3')
    return conn

def get_all_cats():
    conn = sqlite3.connect('CatData.sqlite3')  # Replace 'your_database.db' with the path to your SQLite database
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, informacion, imagen FROM gatos')
    cats = cursor.fetchall()
    conn.close()
    return cats

def get_all_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

@app.route("/admin", methods=["GET"])
def admin():
    # Connect to the database
    connection = sqlite3.connect("CatData.sqlite3")
    cursor = connection.cursor()

    # Fetch data from the tables
    cursor.execute("SELECT * FROM Solicitante")
    solicitante_data = cursor.fetchall()

    cursor.execute("SELECT * FROM Productos")
    productos_data = cursor.fetchall()

    cursor.execute("SELECT * FROM gatos")
    gatos_data = cursor.fetchall()

    # Close the connection
    connection.close()

    # Render the HTML template and pass the data to it
    return render_template('Admin.html', solicitante_data=solicitante_data, productos_data=productos_data, gatos_data=gatos_data, navbar='navbar_admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == valid_username and password == valid_password:
            session['logged_in'] = True  # Mark the user as logged in
            return redirect(url_for('admin'))  # Redirect to the admin page
        else:
            return render_template('login.html',navbar=navbar)
    else:
        return render_template('login.html', navbar=navbar)


@app.route('/')
def index():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'
    return render_template('inicio.html', navbar=navbar)

@app.route("/adoptar", methods=["GET"])
def adoptar():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'
    # Fetch cat names from the database
    connection = sqlite3.connect("CatData.sqlite3")
    cursor = connection.cursor()
    cursor.execute("SELECT nombre FROM gatos")
    cat_names = [row[0] for row in cursor.fetchall()]
    connection.close()

    # Render the template with cat names passed as context
    return render_template('Adoptar.html', cat_names=cat_names, navbar=navbar)

@app.route('/menu', methods=['GET'])
def menu():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'
    
    # Connect to the SQLite database
    connection = sqlite3.connect("CatData.sqlite3")
    cursor = connection.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM Productos")
    products = cursor.fetchall()

    # Close the connection
    connection.close()

    return render_template('Menu.html', products=products, navbar=navbar)

@app.route('/michis', methods=['GET'])
def michis():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'

    cats = get_all_cats()  # Fetch data from the database
    return render_template('Michis.html', cats=cats, navbar=navbar)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove the 'logged_in' session variable
    return redirect(url_for('index'))  # Redirect to the index page

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        nombre = request.json.get('nombre')
        edad = int(request.json.get('edad'))
        ocupacion = request.json.get('ocupacion')
        direccion = request.json.get('direccion')
        email = request.json.get('correo')  # 'correo' seems to be a typo, should be 'email' as per the subsequent lines
        no_tel = request.json.get('telefono')  # Corrected syntax to use parentheses instead of square brackets
        gato_nombre = request.json.get('gato')
        motivo_adopcion = request.json.get('razon')
        response = {'nombre': nombre, 'edad': edad, 'ocupacion': ocupacion, 'direccion': direccion, 'email': email, 'no_tel': no_tel, 'gato_nombre': gato_nombre, 'motivo_adopcion': motivo_adopcion}
        print("Received POST request with Nombre:", nombre, "and Email:", email)  # Print received data
        cursor.execute('''INSERT INTO Solicitante (nombre, edad, ocupacion, direccion, email, no_tel, gato_nombre, motivo_adopcion)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (nombre, edad, ocupacion, direccion, email, no_tel, gato_nombre, motivo_adopcion))
        conn.commit()  # Moved commit and close to the correct indentation level
        conn.close()
        if cursor.rowcount > 0:  # Check if any rows were affected by the insert operation
            return jsonify({"message": "success"})
        else:
            return jsonify({"message": "error", "reason": "Failed to insert data into database"}), 500  # Internal Server Error
    else:
        return jsonify({"message": "error", "reason": "Method Not Allowed"}), 405

@app.route('/modify_cat', methods=['POST'])
def modify_cat():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'
    cat_id = request.form['cat_id']
    cat_name = request.form['cat_name']
    cat_info = request.form['cat_info']
    cat_imagen = request.form['cat_imagen']

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Update the cat information in the database using proper placeholder syntax
    cursor.execute("UPDATE gatos SET nombre=?, informacion=?, imagen=? WHERE id=?", (cat_name, cat_info, cat_imagen, cat_id))
    conn.commit()

    # Fetch all cats again after the update
    cats = get_all_cats()
    
    conn.close()

    # Render the HTML page with updated data
    return render_template('Michis.html', cats=cats, navbar=navbar)


@app.route('/modify_product', methods=['POST'])
def modify_product():
    navbar = 'navbar_admin.html' if 'logged_in' in session else 'navbar.html'
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_imagen = request.form['product_imagen'] # Added line

        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()

        # Update product in the database
        cursor.execute('''UPDATE Productos SET nombre = ?, precio = ?, imagen = ? WHERE id = ?''', (product_name, product_price, product_imagen, product_id))
        conn.commit()

        # Fetch all products again after the update
        products = get_all_products()

        conn.close()

        # Redirect back to the index page after modification
        return render_template('Menu.html', products=products, navbar=navbar)


if __name__ == '__main__':
    app.run()

