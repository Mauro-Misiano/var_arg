
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from arch import arch_model

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    df = pd.read_csv(file)
    activos = df['Activo'].values
    pesos = df['Peso'].values

    dias = 252
    simulated_returns = np.zeros(dias)
    np.random.seed(42)
    
    for peso in pesos:
        simulated = np.random.normal(0, 0.015, dias)
        simulated_returns += peso * simulated

    am = arch_model(simulated_returns, vol='Garch', p=1, q=1)
    res = am.fit(disp='off')
    forecasts = res.forecast(horizon=1, reindex=False)
    sigma_forecast = forecasts.variance.values[-1, 0] ** 0.5

    simulated_total = np.random.normal(0, sigma_forecast, (100, dias))
    avg_path = simulated_total.mean(axis=0)
    capital = [100]
    for r in avg_path:
        capital.append(capital[-1] * (1 + r))

    lower_path = np.percentile(simulated_total, 2.5, axis=0)
    upper_path = np.percentile(simulated_total, 97.5, axis=0)

    lower = [100]
    upper = [100]
    for l, u in zip(lower_path, upper_path):
        lower.append(lower[-1] * (1 + l))
        upper.append(upper[-1] * (1 + u))

    sorted_returns = np.sort(avg_path)
    idx = int(len(sorted_returns) * 0.05)
    var_95 = sorted_returns[idx]
    cvar_95 = sorted_returns[:idx].mean()

    return jsonify({
        'var95': var_95 * 100,
        'cvar95': cvar_95 * 100,
        'capital': capital,
        'lower': lower,
        'upper': upper
    })

if __name__ == '__main__':
    app.run(debug=True)
