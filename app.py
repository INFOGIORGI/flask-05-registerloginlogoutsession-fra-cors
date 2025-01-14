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



@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/personale")
def personale():
    return render_template('personale.html')

@app.route("/register", methods = ["GET","POST"])
def register():

    if request.method == "GET":
        return render_template('register.html') 
    
    
    else:
        nome = request.form.get('nome',None)
        cognome = request.form.get('cognome')
        username = request.form.get('username')
        password = request.form.get('password')
        c_password = request.form.get('c_password')
        
        print("aaaaaaaaa"+nome)
        if nome == None or cognome == None or username == None or password == None or c_password == None:
            return render_template('register.html', msg = "Tutti i campi devono essere riempiti")

        cursor = mysql.connection.cursor()
        query = "INSERT INTO users VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(nome,cognome,username,password))

        mysql.connection.commit()
        
        
        
    
        return redirect("/")
    

    
   


app.run()
