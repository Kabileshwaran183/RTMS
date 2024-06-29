from flask import Flask, render_template, jsonify
import pymysql
import random
import time

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='kabi',
        password='Kabi@183',
        database='monitoring'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/readings')
def get_readings():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM meter_readings')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)

@app.route('/update_readings')
def update_readings():
    connection = get_db_connection()
    cursor = connection.cursor()
    for i in range(1, 6):  # Assuming there are 5 branches
        meter1 = round(random.uniform(0, 100), 2)
        meter2 = round(random.uniform(0, 100), 2)
        meter3 = round(random.uniform(0, 100), 2)
        cursor.execute('UPDATE meter_readings SET meter1=%s, meter2=%s, meter3=%s WHERE id=%s',
                       (meter1, meter2, meter3, i))
    connection.commit()
    cursor.close()
    connection.close()
    return '', 204  # No content to return

if __name__ == '__main__':
    app.run(debug=True)

