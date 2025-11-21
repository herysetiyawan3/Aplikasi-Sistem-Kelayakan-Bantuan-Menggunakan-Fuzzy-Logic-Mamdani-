from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Fuzzy Logic System
def create_fuzzy_system():
    # Input variables
    penghasilan = ctrl.Antecedent(np.arange(0, 11000000, 100000), 'penghasilan')
    tanggungan = ctrl.Antecedent(np.arange(0, 8, 1), 'tanggungan')
    kendaraan = ctrl.Antecedent(np.arange(0, 5, 1), 'kendaraan')
    
    # Output variable
    kelayakan = ctrl.Consequent(np.arange(0, 101, 1), 'kelayakan')
    
    # Membership functions
    penghasilan['rendah'] = fuzz.trimf(penghasilan.universe, [0, 0, 3000000])
    penghasilan['sedang'] = fuzz.trimf(penghasilan.universe, [2000000, 4000000, 6000000])
    penghasilan['tinggi'] = fuzz.trimf(penghasilan.universe, [5000000, 10000000, 10000000])
    
    tanggungan['sedikit'] = fuzz.trimf(tanggungan.universe, [0, 0, 2])
    tanggungan['sedang'] = fuzz.trimf(tanggungan.universe, [1, 3, 4])
    tanggungan['banyak'] = fuzz.trimf(tanggungan.universe, [3, 7, 7])
    
    kendaraan['tidak_ada'] = fuzz.trimf(kendaraan.universe, [0, 0, 0])
    kendaraan['sedikit'] = fuzz.trimf(kendaraan.universe, [0, 1, 1])
    kendaraan['banyak'] = fuzz.trimf(kendaraan.universe, [1, 5, 5])
    
    kelayakan['tidak_layak'] = fuzz.trimf(kelayakan.universe, [0, 0, 50])
    kelayakan['layak'] = fuzz.trimf(kelayakan.universe, [50, 100, 100])
    
    # Rules
    rules = [
        ctrl.Rule(penghasilan['rendah'] & tanggungan['banyak'] & kendaraan['tidak_ada'], kelayakan['layak']),
        ctrl.Rule(penghasilan['rendah'] & tanggungan['banyak'] & kendaraan['sedikit'], kelayakan['layak']),
        ctrl.Rule(penghasilan['rendah'] & tanggungan['sedang'], kelayakan['layak']),
        ctrl.Rule(penghasilan['sedang'] & tanggungan['banyak'], kelayakan['layak']),
        ctrl.Rule(penghasilan['tinggi'], kelayakan['tidak_layak']),
        ctrl.Rule(penghasilan['sedang'] & tanggungan['sedikit'], kelayakan['tidak_layak']),
        ctrl.Rule(kendaraan['banyak'], kelayakan['tidak_layak'])
    ]
    
    control_system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(control_system)
    return simulation

# Routes
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['is_admin'] = True
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json()
    simulation = create_fuzzy_system()
    
    simulation.input['penghasilan'] = float(data['penghasilan'])
    simulation.input['tanggungan'] = float(data['tanggungan'])
    simulation.input['kendaraan'] = float(data['kendaraan'])
    
    simulation.compute()
    result = simulation.output['kelayakan']
    
    return jsonify({
        'result': round(result, 2),
        'status': 'Layak' if result >= 50 else 'Tidak Layak'
    })

if __name__ == '__main__':
    app.run(debug=True) 