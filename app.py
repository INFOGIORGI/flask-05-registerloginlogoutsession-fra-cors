from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('home.html')



@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    else: 
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "" or password == "" :
            return render_template('login.html', msg = "Tutti i campi devono essere riempiti")

        cursor = mysql.connection.cursor()
        query = "SELECT username, password FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        account = cursor.fetchone()
        cursor.close()

        if account == None:
            return render_template('login.html', msg = "L'account non esiste o le credenziali non sono corrette")

        return redirect("/personale")

@app.route("/personale")
def personale():
    return render_template('personale.html')

@app.route("/register", methods = ["GET","POST"])
def register():

    if request.method == "GET":
        return render_template('register.html') 
    
    
    else:
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        username = request.form.get('username')
        password = request.form.get('password')
        c_password = request.form.get('c_password')
        
   
        #Controllo tutti i campi riempiti
        if nome == "" or cognome == "" or username == "" or password == "" or c_password == "":
            return render_template('register.html', msg = "Tutti i campi devono essere riempiti")

        #Controllo password uguale a conferma password
        if password != c_password:
            return render_template('register.html', msg = "Le password non corrispondono")


        #Interrogazione per trovare username uguali
        cursor2 = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        cursor2.execute(query,(username))
        tupla = cursor2.fetchone();
        cursor2.close()

        if tupla != None:
            return render_template('register.html', msg= "Username già esistente")

        #Registrazione
        cursor = mysql.connection.cursor()
        query = "INSERT INTO users VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(nome,cognome,username,password))
        mysql.connection.commit()
        
        return redirect("/personale")
    

    
   


app.run()
