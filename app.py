from flask import Flask, request, session
from flask.templating import render_template
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL


app = Flask(__name__,
            template_folder='templates')
app.secret_key = "abba_s_secret"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '200series'
app.config['MYSQL_DATABASE_DB'] = 'bincom_test'

mysql = MySQL(app)
# conn = mysql.connect()
# cursor = conn.cursor()

def get_ward_name(ward_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT ward_name FROM ward where uniqueid like %s",(ward_id))
    ward = cur.fetchall()[0]
    conn.commit()
    cur.close()
    # names = []
    # for ward in wards:
    #     # print(ward)
    #     names.append(ward[0])
    # print(f"Ward name for id: {ward_id} is: {names}")
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
    # print(f"LGA name is: {len(name)}")#" and state is: {state}")
    return name, state

def get_state_name(state_id):
    conn = mysql.connect()
    cur = conn.cursor()
    # print(f"State id: {state_id}")
    cur.execute("SELECT state_name FROM states where state_id like %s",(state_id))
    name = cur.fetchall()[0]
    conn.commit()
    cur.close()
    # print(f"State name is: {name[0]}")
    return name[0]

def poll_unit_results(poll_unit_id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT party_abbreviation, party_score FROM announced_pu_results \
        WHERE polling_unit_uniqueid LIKE %s",(poll_unit_id))
    res = cur.fetchall()
    conn.commit()
    cur.close()
    # print(f"Response: {res}")
    return res

@app.route('/pollingunit', methods=['POST'])
def polling_units():
    try:
        polling_unit_name = request.form.get("search")
        # session["query"] = polling_unit_name

        # print(f"Query: {polling_unit_name}")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM polling_unit where polling_unit_name  like %s",
                        (polling_unit_name))
        # cursor.execute("Select polling_unit_id, ward_id, lga_id where polling_unit_name like %s ", 
        #                 (polling_unit_name))
        data = cursor.fetchall()[0]
        # session["answers"] = answers
        conn.commit()
        # data = {"query":session["search"], "response": session["answers"]}
        # uniqueid`, `polling_unit_id`, `ward_id`, `lga_id`, `uniquewardid`, 
        # `polling_unit_number`, `polling_unit_name`, `polling_unit_description`, 
        # `lat`, `long`, `entered_by_user`, `date_entered`, `user_ip_address` 
        # 
        # data = {"polling_unit_id":data[1], "ward_id":data[2], "lga_id":data[3], 
        #         "polling_unit_name":data[6]}
        # polling_unit_id = data[1]
        # ward = get_ward_name(data[2])
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
        # print(f"Data: {type(data)}")
        # cursor.execute("Select results from polling_units")
        # for entry in data:
        #     cursor.execute("Select * from announced_pu_results")
        #     data = cursor.fetchone()
        #     conn.commit()
        cursor.close()
        # session.pop("session_name", None)
        return render_template("polling_unit_template.html", data=data) # query=polling_unit_name, response=query)
    except Exception as fail:
        print(f"Exceptions: {fail}")
        return "Command failed to execute"
    # cursor.execute("Select * form Polling_unit_names")
    # data = cursor.fetchone()
    # return render_template("polling_unit_template.html", data=data)
    # return "End"

# @app.route('/search', METHODS=["post"])
# def search():
#     if request.method == "post":
#         polling_unit_name = request.form['search']
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("Select polling_unit_id, ward_id, lga_id where polling_unit_name like %s ", 
#                         (polling_unit_name))
#         conn.commit()
#         data = cursor.featchall()
#         return data
#     # return "Hello, world"
@app.route('/')
def index():
    # polling_unit_name = request.form.get('search')
    # session["search"] = polling_unit_name
    return render_template('index.html')
    # render_template('index.html')
    # polling_units_name = request.form.get("search")
    # return polling_units_name

# app.run(host='localhost', port=5000)
app.run(debug=True)

if '__name__' == '__main__':
    # app = Flask(__name__)
    # app.run(host='localhost', port=5000)
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = '200series'
    # app.config['MYSQL_DB'] = 'bincom_test'

    mysql = MySQL(app)
    conn = mysql.connect()
    cursor = conn.cursor()