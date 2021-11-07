from flask import Flask, request, session
from flask.templating import render_template
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL


app = Flask(__name__,
            template_folder='templates')
app.secret_key = ""
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bincom_test'

mysql = MySQL(app)

def get_ward_name(ward_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT ward_name FROM ward where uniqueid like %s",(ward_id))
    ward = cur.fetchall()[0]
    conn.commit()
    cur.close()
    return ward[0]

def get_lga_and_state(lga_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT lga_name, state_id FROM lga where lga_id like %s",(lga_id))
    res = cur.fetchall()[0]
    name = res[0]
    state = get_state_name(res[1])
    conn.commit()
    cur.close()
    return name, state

def get_state_name(state_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT state_name FROM states where state_id like %s",(state_id))
    name = cur.fetchall()[0]
    conn.commit()
    cur.close()
    return name[0]

def poll_unit_results(poll_unit_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT party_abbreviation, party_score FROM announced_pu_results \
        WHERE polling_unit_uniqueid LIKE %s",(poll_unit_id))
    res = cur.fetchall()
    conn.commit()
    cur.close()
    return res

@app.route('/pollingunit', methods=['POST'])
def polling_units():
    try:
        polling_unit_name = request.form.get("search")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM polling_unit where polling_unit_name  like %s",
                        (polling_unit_name))
        data = cursor.fetchall()[0]
        conn.commit()
        ward = get_ward_name(data[4]) 
        lga, state = get_lga_and_state(data[3]) 
        polling_unit_name = data[6]
        results = poll_unit_results(data[0])
        data = {
                "name": polling_unit_name,
                "ward": ward,
                "lga": lga,
                "state": state,
                "results": results
            }
        cursor.close()
        return render_template("polling_unit_template.html", data=data) # query=polling_unit_name, response=query)
    except Exception as fail:
        print(f"Exceptions: {fail}")
        return "Command failed to execute"
   
@app.route('/')
def index():
    return render_template('index.html')
   
app.run(debug=True)
