from flask import Flask, render_template, request, redirect
from flask.ext.mysql import MySQL
import yaml
import mysql
import mysql.connector


app = Flask(__name__)

# Configure db
db = yaml.load(open('/Users/geraldine/Projects/myappflask/db.yaml'))
app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']
app.config['MYSQL_DATABASE_USER'] = db['mysql_user'] 
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']

mysql = MySQL(app)
mysql.init_app(app)

connection = mysql.connect() # Abrir una conexion guardar la conexion en una variable

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form 
        name = userDetails['name']
        email = userDetails['email']
        try:
            cur = connection.cursor() # Cargar un cursorr asginar un cursor a esa conexion ( nada de get db)
            cur.execute("INSERT INTO users(name, email) VALUES(%s,%s)", (name, email) ) #  se le carga un comando al cursor
            # Ese comando solo se queda pendinete de ejecucion
            # En el commit se envia el comando a la conexion 
            connection.commit()       # y cargar el commit a la conexion no a otra cosa
        except Exception as e:
            print(str(e))
            return redirect('/users')
    return  render_template('index.html')

@app.route('/users')
def users():
    cur=connection.cursor()
    resultValue=cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


if __name__ == '__main__':
    app.run(debug = True)

