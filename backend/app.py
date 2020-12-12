import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    response = {
        'message' : 'backend is live!',
        'endpoints' : {
            '/all' : 'get a list of all drugs',
            '/<id>' : 'get details of drug with given id',
            '/images/<id>.jpg' : 'get image of drug with given id', # Must be served by NGINX
        }
    }
    return jsonify(response)

@app.route('/all')
def all_items():
    keys = 'id name short_desc link'.split()
    with sqlite3.connect('database.db') as connection:
        results = connection.execute('select ' + ', '.join(keys) + ' from drugs').fetchall()
    response = jsonify([dict(zip(keys, result)) for result in results])
    response.status_code = 201
    return response

@app.route('/<id>')
def particular_item(id):
    with sqlite3.connect('database.db') as connection:
        result = connection.execute('select * from drugs where id = ?', (id, )).fetchone()
    if result:
        response = jsonify(dict(zip('id name short_desc long_desc link'.split(), result)))
        response.status_code = 201
    else:
        response = jsonify({'message' : 'invalid id'})
        response.status_code = 400
    return response

if __name__ == '__main__':
    app.run(debug=True)
