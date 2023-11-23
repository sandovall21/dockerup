from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

# MySQL Connection
config = {
  'user' : 'root',
  'password' : 'root',
  'host' : 'db',
  'port' : '3306',
  'database' : 'registroscrud'
}

server = mysql.connector.connect(
        host = 'db',
        user = 'root',
        password = 'root'
)
curs = server.cursor()
curs.execute('CREATE DATABASE IF NOT EXISTS registroscrud')
server.close()
curs.close()
db = mysql.connector.connect(
        host = 'db',
        user = 'root',
        password = 'root',
        database = 'registroscrud'
)
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS contacts ( id INT(11) AUTO_INCREMENT PRIMARY KEY, fullname VARCHAR(40), phone VARCHAR(40), email VARCHAR(40))')

# Settings
app.secret_key = 'mysecreykey'

@app.route('/')
def Index():
  cur = db.cursor()
  cur.execute('SELECT * FROM contacts')
  data = cur.fetchall()
  return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    cur = db.cursor()
    cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
    db.commit()
    flash('Contact Added Succesfully')
    return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
  cur = db.cursor()
  cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
  data = cur.fetchall()
  return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = {'POST'})
def update_contact(id):
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    cur = db.cursor()
    cur.execute("""
      UPDATE contacts
      SET fullname = %s,
          email = %s,
          phone = %s
      WHERE id = %s
    """, (fullname, email, phone, id))
    db.commit()
    flash('Contact Update Succesfully')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
  cur = db.cursor()
  cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
  db.commit()
  flash('Contact Removed Succesfully')
  return redirect(url_for('Index'))

if __name__ == '__main__':
  app.run(port = 5000, debug = True)