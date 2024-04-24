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



@app.route('/searchbondnumber', methods=["POST", "GET"])
def search_bond_number():
    if request.method == "POST":
        bond_number = request.form["bond"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM purchase_details WHERE `Bond Number` LIKE %s", (bond_number,))
        # data = cursor.fetchone()
        bond_number_purchase_data = cursor.fetchall()
        print(bond_number_purchase_data)
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM redemption_details WHERE `Bond Number` LIKE %s", (bond_number,))
        bond_number_redemption_data=cursor.fetchall()
        print(bond_number_redemption_data)
        cursor.close()
        return render_template("q1.html", bond_number_purchase_data=bond_number_purchase_data, bond_number_redemption_data=bond_number_redemption_data)
    return render_template("q1.html")




@app.route('/searchcompany',  methods=["POST", "GET"])
def search_company():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT `Name of the Purchaser` FROM purchase_details ORDER BY `Name of the Purchaser` ASC")
    raw_data = cursor.fetchall()
    cursor.close()
    company_names = []
    for i in raw_data:
        company_names.append(i[0])
    # print(company_names)

    if request.method == "POST":
        if 'company' in request.form:
            company_name = request.form["company"]
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM purchase_details WHERE `Name of the Purchaser` LIKE %s", (f"%{company_name}%",))
            company_purchase_data = cursor.fetchall()
            cursor.close()

            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT SUBSTRING(`Date of Purchase`, -4), COUNT(`Bond Number`), SUM(CAST(REPLACE(`Denominations`, ',', '') AS UNSIGNED))
                           FROM purchase_details WHERE `Name of the Purchaser` LIKE %s GROUP BY SUBSTRING(`Date of Purchase`, -4) """, (f"%{company_name}%",))
            company_purchase_data_by_year = cursor.fetchall()
            cursor.close()
            year=[]
            bond_count=[]
            total_amount=[]
            for i in company_purchase_data_by_year:
                year.append(i[0])
                bond_count.append(i[1])
                total_amount.append(i[2])
            # print(year)
            # print(bond_count)
            # print(total_amount)
            return render_template("q2.html",
                                   company_names = company_names,
                                   company_name = company_name,
                                   company_purchase_data=company_purchase_data,
                                   company_purchase_data_by_year=company_purchase_data_by_year,
                                   year=year,
                                   bond_count=bond_count,
                                   total_amount=total_amount)
    return render_template("q2.html", company_names=company_names)







@app.route('/searchparty',  methods=["POST", "GET"])
def search_party():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT `Name of the Political Party` FROM redemption_details ORDER BY `Name of the Political Party` ASC")
    raw_data = cursor.fetchall()
    cursor.close()
    party_names = []
    for i in raw_data:
        party_names.append(i[0])
    # print(party_names)

    if request.method == "POST":
        if 'party' in request.form:
            party_name = request.form["party"]
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM redemption_details WHERE `Name of the Political Party` LIKE %s", (f"%{party_name}%",))
            party_bonds_data = cursor.fetchall()
            cursor.close()

            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT SUBSTRING(`Date of Encashment`, -4), COUNT(`Bond Number`), SUM(CAST(REPLACE(`Denominations`, ',', '') AS UNSIGNED))
                           FROM redemption_details WHERE `Name of the Political Party` LIKE %s GROUP BY SUBSTRING(`Date of Encashment`, -4) """, (f"%{party_name}%",))
            party_bonds_data_by_year = cursor.fetchall()
            cursor.close()
            year=[]
            bond_count=[]
            total_amount=[]
            for i in party_bonds_data_by_year:
                year.append(i[0])
                bond_count.append(i[1])
                total_amount.append(i[2])
            # print(year)
            # print(bond_count)
            # print(total_amount)
            return render_template("q3.html",
                                   party_names = party_names,
                                   party_name = party_name,
                                   party_bonds_data=party_bonds_data,
                                   party_bonds_data_by_year=party_bonds_data_by_year,
                                   year=year,
                                   bond_count=bond_count,
                                   total_amount=total_amount)
    return render_template("q3.html", party_names=party_names)




@app.route('/partydonations',methods=["GET","POST"])
def party_donations():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT `Name of the Political Party` FROM redemption_details ORDER BY `Name of the Political Party` ASC")
    raw_data = cursor.fetchall()
    cursor.close()
    party_names = []
    for i in raw_data:
        party_names.append(i[0])
    if request.method=="POST":
        if 'party' in request.form:
            party_name=request.form["party"]
            cursor=mysql.connection.cursor()
            cursor.execute("""SELECT purchase_details.`Name of the Purchaser`, SUM(CAST(REPLACE(purchase_details.`Denominations`, ',', '') AS DECIMAL)) 
                            FROM purchase_details
                            JOIN redemption_details ON purchase_details.`Bond Number` = redemption_details.`Bond Number`
                            WHERE redemption_details.`Name of the Political Party` LIKE %s
                            GROUP BY purchase_details.`Name of the purchaser`
                            """, (party_name,))
            raw_data = cursor.fetchall()
            party_donations_data=[]
            total_donation=0
            for i in raw_data:
                party_donations_data.append(i)
            print(party_donations_data)
            for i in party_donations_data:
                total_donation+=int(i[1])
            print(total_donation)
            cursor.close()
            return render_template('q4.html',
                                   party_donations_data=party_donations_data,
                                   party_names=party_names,
                                   party_name=party_name,
                                   total_donation=total_donation)
    return render_template('q4.html', party_names=party_names)






@app.route('/companydonations',methods=["GET","POST"])
def company_donations():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT `Name of the Purchaser` FROM purchase_details ORDER BY `Name of the Purchaser` ASC")
    raw_data = cursor.fetchall()
    cursor.close()
    company_names = []
    for i in raw_data:
        company_names.append(i[0])
    if request.method=="POST":
        if 'company' in request.form:
            company_name=request.form["company"]
            cursor=mysql.connection.cursor()
            cursor.execute("""SELECT redemption_details.`Name of the Political Party`, SUM(CAST(REPLACE(redemption_details.`Denominations`, ',', '') AS DECIMAL))
                            FROM purchase_details
                            JOIN redemption_details ON purchase_details.`Bond Number` = redemption_details.`Bond Number`
                            WHERE purchase_details.`Name of the Purchaser` LIKE %s
                            GROUP BY redemption_details.`Name of the Political Party`""", (company_name,))
            raw_data = cursor.fetchall()
            company_donations_data=[]
            total_donation=0
            for i in raw_data:
                company_donations_data.append(i)
            print(company_donations_data)
            for i in company_donations_data:
                total_donation+=int(i[1])
            print(total_donation)
            cursor.close()
            return render_template('q5.html',
                                   company_donations_data=company_donations_data,
                                   company_names=company_names,
                                   company_name=company_name,
                                   total_donation=total_donation)
    return render_template('q5.html', company_names=company_names)




if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80", debug = True)
