import pandas as pd
from flask import Flask, request, jsonify, render_template, send_file
from models import db, Donor, FosterHome, Cat
from datetime import datetime
import matplotlib.pyplot as plt

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

# Função de exportação de dados aprimorada
@app.route('/export_data', methods=['GET'])
def export_data():
    # Query para todos os doadores
    donors = Donor.query.all()
    data = [{
        'name': donor.name,
        'email': donor.email,
        'contact': donor.contact,
        'donation_date': donor.donation_date
    } for donor in donors]

    # Criando o DataFrame
    df = pd.DataFrame(data)
    
    # Convertendo a coluna de data para datetime
    df['donation_date'] = pd.to_datetime(df['donation_date'])
    
    # Exemplo de análise: contagem de doações por mês
    df['donation_month'] = df['donation_date'].dt.to_period('M')
    donation_counts = df.groupby('donation_month').size()

    # Plotar um gráfico de barras
    plt.figure(figsize=(10, 6))
    donation_counts.plot(kind='bar')
    plt.title('Número de Doações por Mês')
    plt.xlabel('Mês')
    plt.ylabel('Número de Doações')
    plt.tight_layout()
    plt.savefig('donations_by_month.png')  # Salvar o gráfico como imagem

    # Exportando para Excel com várias planilhas
    file_path = 'donors_data.xlsx'
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Donors', index=False)
        donation_counts.to_excel(writer, sheet_name='Donation Analysis')
    
    # Enviando o arquivo para download
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
