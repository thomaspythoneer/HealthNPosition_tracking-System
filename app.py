from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_csv('health_log.csv')
    charts = {}

    for col in ['heart_rate', 'temperature_C', 'spo2']:
        fig, ax = plt.subplots(figsize=(10, 3))
        if 'predicted' in df.columns:
            colors = df['predicted'].map({0: 'green', 1: 'red'})
            ax.scatter(df.index, df[col], c=colors, label=col)
        else:
            ax.plot(df[col], label=col)
        ax.set_title(f"{col} with Anomalies" if 'predicted' in df.columns else col)
        ax.set_xlabel('Reading')
        ax.set_ylabel(col)
        ax.grid(True)
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_data = base64.b64encode(buf.read()).decode()
        charts[col] = chart_data
        plt.close()

    # Anomalies Table
    if 'predicted' in df.columns:
        df['anomaly_score'] = 1  # simulate score
        anomalies = df[df['predicted'] == 1].sort_values(by='timestamp', ascending=False).head(10)
    else:
        anomalies = pd.DataFrame()

    return render_template('index.html', charts=charts, anomalies=anomalies)

if __name__ == '__main__':
    app.run(debug=True)
