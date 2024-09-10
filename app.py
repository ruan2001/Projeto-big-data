from flask import Flask, request, jsonify, render_template, send_file
from openpyxl.reader.excel import load_workbook
from openpyxl.drawing.image import Image

from models import db, Donor, FosterHome, Cat, Dog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

file_path_for_export = 'data_export.xlsx'


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
    quantidade = request.form['quantidade']
    idade_pet = request.form['idade_pet']
    idade = request.form['idade']

    new_donor = Donor(
        name=name,
        email=email,
        contact=contact,
        quantidade=quantidade,
        idade_pet=idade_pet,
        idade=idade_pet,
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
        available_spots=int(capacity) - 7
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


@app.route('/dog', methods=['POST'])
def add_dog():
    name = request.form['name']
    age = request.form['age']
    breed = request.form['breed']
    new_dog = Dog(
        name=name,
        age=age,
        breed=breed,
        status="available"
    )
    db.session.add(new_dog)
    db.session.commit()
    return jsonify({"message": "Cat added successfully!"}), 201


@app.route('/export_data', methods=['POST'])
def export_data():
    donor_data = get_donor_data()
    foster_home_data = get_foster_home_data()
    cat_data = get_cat_data()
    dog_data = get_dog_data()

    save_data_to_excel(donor_data, foster_home_data, cat_data, dog_data, file_path_for_export)

    df_donors = pd.DataFrame(donor_data)
    df_fosters = pd.DataFrame(foster_home_data)

    df_cats = pd.DataFrame(cat_data)

    df_dogs = pd.DataFrame(dog_data)

    generate_and_save_plot_doador(df_donors)
    generate_and_save_plot_foster(df_fosters)
    generate_and_save_plot_cat(df_cats)
    generate_and_save_plot_dog(df_dogs)

    return send_file(file_path_for_export, as_attachment=True)


def get_donor_data():
    donors = Donor.query.all()
    return [{
        'name': donor.name,
        'email': donor.email,
        'contact': donor.contact,
        'donation_date': donor.donation_date,
        'idade_pet': donor.idade_pet,
        'idade': donor.idade,
        'quantidade': donor.quantidade
    } for donor in donors]


def get_foster_home_data():
    foster_homes = FosterHome.query.all()
    return [{
        'name': home.name,
        'location': home.location,
        'capacity': home.capacity,
        'available_spots': home.available_spots
    } for home in foster_homes]


def get_cat_data():
    cats = Cat.query.all()
    return [{
        'name': cat.name,
        'age': cat.age,
        'breed': cat.breed,
        'status': cat.status
    } for cat in cats]


def get_dog_data():
    dogs = Dog.query.all()
    return [{
        'name': dog.name,
        'age': dog.age,
        'breed': dog.breed,
        'status': dog.status
    } for dog in dogs]


def insert_plot_into_excel(excel_file, plot_file, wb_name, init):
    wb = load_workbook(excel_file)
    ws = wb[wb_name]  # Selecionar a planilha 'Donors'

    img = Image(plot_file)
    ws.add_image(img, init)  # Ajuste a célula de destino conforme necessário

    wb.save(excel_file)


def save_data_to_excel(donor_data, foster_home_data, cat_data, dog_data, file_path='data_export.xlsx'):
    df_donors = pd.DataFrame(donor_data)
    df_foster_homes = pd.DataFrame(foster_home_data)
    df_cats = pd.DataFrame(cat_data)
    df_dogs = pd.DataFrame(dog_data)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_donors.to_excel(writer, sheet_name='Donors', index=False)
        df_foster_homes.to_excel(writer, sheet_name='Foster Homes', index=False)
        df_cats.to_excel(writer, sheet_name='Cats', index=False)
        df_dogs.to_excel(writer, sheet_name='Dogs', index=False)


def generate_and_save_plot_foster(df_fosters):
    file_path = 'grafico_foster.png'
    fig, axs = plt.subplots(2, 1)

    sns.barplot(x='name', y='capacity', data=df_fosters, ax=axs[0])
    axs[0].set_title('Capacidade do Abrigo')
    axs[0].set_xlabel('Abrigo')
    axs[0].set_ylabel('Capacidade')

    sns.lineplot(x='name', y='available_spots', data=df_fosters, ax=axs[1])
    axs[1].set_title('Vagas disponíveis')
    axs[0].set_xlabel('Abrigo')
    axs[0].set_ylabel('Vagas')

    plt.tight_layout()

    fig.savefig(file_path)  # Salva no formato PNG com resolução de 300 DPI

    insert_plot_into_excel(file_path_for_export, file_path, wb_name='Foster Homes', init='K1')


def generate_and_save_plot_doador(df_donors):
    file_path = 'grafico_doador.png'
    fig, axs = plt.subplots(3, 1)

    sns.barplot(x='name', y='quantidade', data=df_donors, ax=axs[0])
    axs[0].set_title('Quantidade de doação por doarores')
    axs[0].set_xlabel('Doadores')
    axs[0].set_ylabel('Quantidade')

    sns.lineplot(x='name', y='idade', data=df_donors, ax=axs[1])
    axs[1].set_title('Idade dos Doadores')
    axs[1].set_xlabel('Doadores')
    axs[1].set_ylabel('idade')

    sns.lineplot(x='name', y='idade_pet', data=df_donors, ax=axs[2])
    axs[2].set_title('Idade dos pets doados')
    axs[2].set_xlabel('name')
    axs[2].set_ylabel('idade_pet')

    plt.tight_layout()

    fig.savefig(file_path)  # Salva no formato PNG com resolução de 300 DPI

    insert_plot_into_excel(file_path_for_export, file_path, wb_name='Donors', init='K1')


def generate_and_save_plot_cat(df_cats):
    file_path = 'grafico_cat.png'
    plt.figure()

    sns.barplot(x='name', y='age', data=df_cats)
    plt.title('Idade dos gatos')
    plt.xlabel('Gato')
    plt.ylabel('Idade')

    plt.tight_layout()

    plt.savefig(file_path)  # Salva no formato PNG com resolução de 300 DPI

    insert_plot_into_excel(file_path_for_export, file_path, wb_name='Cats', init='K1')


def generate_and_save_plot_dog(df_dogs):
    file_path = 'grafico_dog.png'
    plt.figure()

    sns.barplot(x='name', y='age', data=df_dogs)
    plt.title('Idade dos cachorros')
    plt.xlabel('Gato')
    plt.ylabel('Idade')

    plt.tight_layout()

    plt.savefig(file_path)  # Salva no formato PNG com resolução de 300 DPI

    insert_plot_into_excel(file_path_for_export, file_path, wb_name='Dogs', init='K1')


if __name__ == '__main__':
    app.run(debug=True)
