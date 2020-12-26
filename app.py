import sqlite3
import smtplib
from flask import Flask, jsonify, render_template, request
from forms import ContactForm

app = Flask(__name__)

@app.route('/')
def home():
    with sqlite3.connect('database.db') as connection:
        results = connection.execute('select * from drugs').fetchall()
    keys = 'id name short_desc long_desc link'.split()
    products = [dict(zip(keys, result)) for result in results]
    return render_template('index.html', products=products)

@app.route('/api')
def foo():
    response = {
        'endpoints' : {
            '/all' : 'get details of all drugs',
            '/<id>' : 'get details of drug with given id',
            '/images/<id>.jpg' : 'get image of drug with given id', # Must be served by NGINX
        }
    }
    return jsonify(response)

@app.route('/api/all')
def all_items():
    with sqlite3.connect('database.db') as connection:
        results = connection.execute('select * from drugs').fetchall()
    keys = 'id name short_desc long_desc link'.split()
    response = jsonify([dict(zip(keys, result)) for result in results])
    response.status_code = 201
    return response

@app.route('/api/<id>')
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
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app .route('/form', methods = ["POST"])
def form():
    email = request.form.get("email")
    ph_number = request.form.get("number")
    name = request.form.get("name")
    message = request.form.get("message")
    complete_message = "Email: " + email + "\nPhone Number: " + ph_number + "\nName: " + name + "\nMessage: " + message
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("legaldrugstore2020@gmail.com", 'LegalDrugstore@123')
    server.sendmail("legaldrugstore2020@gmail.com", "legaldrugstore2020@gmail.com", complete_message)
    return_message = "Message sent successfully!! Our staffs will contact you shortly.."
    return render_template('form.html', return_msg = return_message)


if __name__ == '__main__':
    app.run(debug=True)
