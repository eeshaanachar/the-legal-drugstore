import smtplib
import sqlite3
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from secrets import ServerCredentials, APP_SECRET

app = Flask(__name__)
app.secret_key = APP_SECRET

@app.route('/')
def home():
    with sqlite3.connect('database.db') as connection:
        results = connection.execute('select * from drugs').fetchall()
    keys = 'id name short_desc long_desc link'.split()
    products = [dict(zip(keys, result)) for result in results]
    return render_template('index.html', products=products)

@app.route('/api')
def api():
    response = {
        'endpoints' : {
            '/all' : 'get details of all drugs',
            '/<id>' : 'get details of drug with given id',
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
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    try:
        client_email = request.form.get("email")
        contact = request.form.get("number")
        name = request.form.get("name")
        message = request.form.get("message")
    except:
        response = jsonify({'message': 'required attributes missing'})
        response.status_code = 400
        return response
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as session:
        session.login(ServerCredentials.server_email, ServerCredentials.server_password)
        server_message = f'Subject: Somebody contacted you on your website\n\nName: {name}\nEmail: {client_email}\nContact Number: {contact}\nMessage: {message}'
        session.sendmail(ServerCredentials.server_email, ServerCredentials.server_email, server_message)
        client_message = f'Subject: Thank you for contacting The Legal Drugstore\n\nWe have received your message and a representative will contact you shortly'
        session.sendmail(ServerCredentials.server_email, client_email, client_message)
    flash('Message sent successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
