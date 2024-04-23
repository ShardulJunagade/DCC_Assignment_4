from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
db=yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods = ["POST", "GET"])
def main():
    return render_template("index.html")

@app.route('/a_1', methods=["POST", "GET"])
def a_1():
    if request.method == "POST":
        bond_number = request.form["box"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM purchase_details WHERE `Bond Number` LIKE %s", (bond_number,))
        # data = cursor.fetchone()
        data = cursor.fetchall()
        cursor.close()
        print(data)
    return render_template("index.html", a_1_data=data)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80", debug = True)