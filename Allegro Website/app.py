import os
import csv
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_SECRET'

# Set your admin password here
ADMIN_PASSWORD = "mysecurepass"

# Data for each car
data = {
    'cadillac': {
        'name': 'Escalade V‑SPORT',
        'description': '6.2 L supercharged V8 engine with 10‑speed auto transmission.',
        'pdf': None
    },
    'lexus': {
        'name': 'Lexus LX 700h Luxury',
        'description': 'Hybrid 3.4 L twin‑turbo V6, 10‑speed auto transmission.',
        'pdf': None
    },
    'bmw': {
        'name': 'BMW M850i',
        'description': '523 hp, Transmission Auto, Speed-250 km/h',
        'pdf': None
    },
    'toyota_trd': {
        'name': 'TOYOTA SEQUOIA',
        'description': 'Twin Turbo V6 Hybrid, 437 hp, Transmission 10-Speed Auto',
        'pdf': None
    },
    'bmw_m650': {
        'name': 'BMW X7 M650i',
        'description': '2025 BMW x7 M650i, Automatic Transmission',
        'pdf': None
    },
    'lexus_gx550': {
        'name': 'LEXUS GX 550 LUXURY',
        'description': 'Engine 3.4L, Twin-Turbo V6, 349 hp. Transmission 10-Speed Auto.',
        'pdf': None
    },
    'cadillac_sport': {
        'name': 'CADILLAC IQ SPORT',
        'description': 'Engine 3.4L, Twin-Turbo V6, 349 hp. Transmission 10-Speed Auto.',
        'pdf': None
    },
    'maybach_680': {
        'name': 'MERCEDES-MAYBACH S 680',
        'description': '',
        'pdf': None
    }
    # Add more cars here...
}

# Upload settings
UPLOAD_FOLDER = os.path.join('static', 'pdfs')
ALLOWED = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

# Home page with car list
@app.route('/')
def index():
    return render_template('index.html', cars=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Contact form handler
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

# Car details page
@app.route('/car/<car_id>')
def car_detail(car_id):
    car = data.get(car_id)
    if not car:
        return "Car not found", 404
    return render_template('car_detail.html', car=car, car_id=car_id)

# PDF download route
@app.route('/download/<car_id>')
def download(car_id):
    car = data.get(car_id)
    if not car or not car.get('pdf'):
        return "No PDF available", 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], car['pdf'], as_attachment=True)

# Admin upload page (password protected)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        car_id = request.form.get('car_id')
        file = request.files.get('file')

        if password != ADMIN_PASSWORD:
            flash("❌ Incorrect password.")
            return redirect(url_for('admin'))

        if car_id in data and file and allowed_file(file.filename):
            filename = secure_filename(f"{car_id}.pdf")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            data[car_id]['pdf'] = filename
            flash('✅ PDF uploaded successfully!')
        else:
            flash('❗ Invalid car or file type.')
        return redirect(url_for('admin'))

    return render_template('admin.html', cars=data.keys())
    
if __name__ == "__main__":
    app.run(debug=True)
