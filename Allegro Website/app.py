from flask import Flask, render_template, request, redirect, url_for, flash
import csv

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_SECRET'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    number = request.form['whatsapp']
    with open('submissions.csv', 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([name, email, message, number])
    flash('Message received!')
    return redirect(url_for('contact'))


if __name__ == "__main__":
    app.run()
