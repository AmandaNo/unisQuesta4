from flask import Flask, render_template, request, jsonify
import pyodbc

app = Flask(__name__)

# Configure your SQL Server connection
conn = pyodbc.connect('DRIVER={SQL Server};Server=LAPTOP-VOGQQ4ME\\SQLSERVER2022;Database=imcBanco;Trusted_Connection=True;TrustServerCertificate=True')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    # Extract data from the HTML form
    patient_name = request.form['patient_name']
    full_address = request.form['full_address']
    weight = float(request.form['weight'])
    height = float(request.form['height'])

    # Perform BMI calculation
    bmi = ((weight * 100) / (height ** 2)) * 100

    # Determine the BMI category
    if bmi < 17:
        situation = "Muito abaixo do peso"
    elif 17 <= bmi < 18.5:
        situation = "Abaixo do peso"
    elif 18.5 <= bmi < 25:
        situation = "Peso normal"
    elif 25 <= bmi < 30:
        situation = "Acima do peso"
    elif 30 <= bmi < 35:
        situation = "Obesidade I"
    elif 35 <= bmi < 40:
        situation = "Obesidade II (severa)"
    else:
        situation = "Obesidade III (mórbida)"

    # Save the data to the database
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO BMIData (PatientName, FullAddress, Weight, Height, BMI, Situation)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (patient_name, full_address, weight, height, bmi, situation))
    conn.commit()

    # Return the result as JSON
    result = {
        'patient_name': patient_name,
        'bmi': bmi,
        'situation': situation,
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
