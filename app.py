from flask import Flask, render_template, request
# import sqlite3
from flaskext.mysql import MySQL

app = Flask(__name__)

# Connect to the SQLite database
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']= 'flask'

mysql=MySQL()
mysql.init_app(app)

cur=mysql.connect().cursor()

with app.open_resource('bincom.sql', mode='r') as f:
    script = f.read()
    cur.execute(script)


@app.route('/')
def index():
    # Fetch the list of polling units
    cur.execute('SELECT * FROM polling_unit WHERE state_id = 25')
    polling_units = cur.fetchall()
    return render_template('index.html', polling_units=polling_units)

@app.route('/polling_unit/<int:unit_id>')
def get_polling_unit_result(unit_id):
    # Fetch the results for the given polling unit
    cur.execute('SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = {}'.format(unit_id))

    results = cur.fetchall()
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
