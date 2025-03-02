import matplotlib
matplotlib.use('Agg')  # Prevents GUI-related errors
import matplotlib.pyplot as plt
import numpy as np
import os
import math
from flask import Flask, render_template, request

app = Flask(__name__)

# Speed of light in meters per second
c = 299792458

def lorentz_factor(v):
    if v >= c:
        return None  # Prevent division by zero for v >= c
    return 1 / math.sqrt(1 - (v**2 / c**2))

def time_dilation(t, v):
    gamma = lorentz_factor(v)
    return t * gamma if gamma else None

def length_contraction(L, v):
    gamma = lorentz_factor(v)
    return L / gamma if gamma else None

def relativistic_kinetic_energy(m, v):
    gamma = lorentz_factor(v)
    return (gamma - 1) * m * c**2 if gamma else None

def generate_mass_plot():
    v_values = np.linspace(0, 0.99 * c, 100)  # Speeds from 0 to 99% of light speed
    gamma_values = 1 / np.sqrt(1 - (v_values ** 2 / c ** 2))  # Lorentz factor
    mass_values = gamma_values  # Mass increases with gamma

    plt.figure(figsize=(6, 4))
    plt.plot(v_values / c, mass_values, label="Relativistic Mass Increase", color="red")
    plt.axvline(x=1, linestyle="--", color="black", label="Speed of Light (Unreachable)")
    plt.xlabel("Velocity as a Fraction of Speed of Light (v/c)")
    plt.ylabel("Relative Mass Increase")
    plt.title("Why We Can’t Reach the Speed of Light")
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join("static", "mass_plot.png")
    plt.savefig(plot_path)
    plt.close()
    return plot_path

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        try:
            v = float(request.form['velocity'])
            t = float(request.form['time']) if request.form['time'] else None
            L = float(request.form['length']) if request.form['length'] else None
            m = float(request.form['mass']) if request.form['mass'] else None
            
            if v >= c:
                result['error'] = "Velocity cannot be equal to or exceed the speed of light."
            else:
                if t is not None:
                    result['time_dilation'] = time_dilation(t, v)
                if L is not None:
                    result['length_contraction'] = length_contraction(L, v)
                if m is not None:
                    result['kinetic_energy'] = relativistic_kinetic_energy(m, v)
        except ValueError:
            result['error'] = "Invalid input. Please enter numerical values."
    
    plot_path = generate_mass_plot()
    return render_template('index.html', result=result, plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
