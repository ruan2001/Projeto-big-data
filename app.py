from flask import Flask, request, jsonify, render_template, send_file
from models import db, Donor, FosterHome, Cat
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donor', methods=['POST'])
def add_donor():
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    
    new_donor = Donor(
        name=name,
        email=email,
        contact=contact,
        donation_date=datetime.now()
    )
    
    db.session.add(new_donor)
    db.session.commit()
    
    return jsonify({"message": "Donor added successfully!"}), 201

@app.route('/foster_home', methods=['POST'])
def add_foster_home():
    name = request.form['name']
    location = request.form['location']
    capacity = request.form['capacity']
    new_home = FosterHome(
        name=name,
        location=location,
        capacity=capacity,
        available_spots=capacity
    )
    db.session.add(new_home)
    db.session.commit()
    return jsonify({"message": "Foster Home added successfully!"}), 201

@app.route('/cat', methods=['POST'])
def add_cat():
    name = request.form['name']
    age = request.form['age']
    breed = request.form['breed']
    new_cat = Cat(
        name=name,
        age=age,
        breed=breed,
        status="available"
    )
    db.session.add(new_cat)
    db.session.commit()
    return jsonify({"message": "Cat added successfully!"}), 201

@app.route('/export_data', methods=['GET'])
def export_data():
    # Coletando dados dos doadores
    donors = Donor.query.all()
    donor_data = [{
        'name': donor.name,
        'email': donor.email,
        'contact': donor.contact,
        'donation_date': donor.donation_date
    } for donor in donors]

    # Coletando dados dos lares de acolhimento
    foster_homes = FosterHome.query.all()
    foster_home_data = [{
        'name': home.name,
        'location': home.location,
        'capacity': home.capacity,
        'available_spots': home.available_spots
    } for home in foster_homes]

    # Coletando dados dos gatos
    cats = Cat.query.all()
    cat_data = [{
        'name': cat.name,
        'age': cat.age,
        'breed': cat.breed,
        'status': cat.status
    } for cat in cats]

    # Criando dataframes
    df_donors = pd.DataFrame(donor_data)
    df_foster_homes = pd.DataFrame(foster_home_data)
    df_cats = pd.DataFrame(cat_data)

    # Salvando dataframes em arquivos Excel
    file_path = 'data_export.xlsx'
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_donors.to_excel(writer, sheet_name='Donors', index=False)
        df_foster_homes.to_excel(writer, sheet_name='Foster Homes', index=False)
        df_cats.to_excel(writer, sheet_name='Cats', index=False)

    # Enviando o arquivo como resposta
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
