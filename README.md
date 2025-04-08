# HealthNPosition_tracking-System

Health and Position Monitoring System
This system uses a Raspberry Pi as the central processor, integrating sensors like a heart rate sensor, temperature sensor (LM35), and SpO2 sensor to monitor vital health parameters. The collected data is transmitted over Wi-Fi to a local device, where a data logger stores the readings. An Isolated Forest Autoencoder (ML model) analyzes the data for anomalies, such as irregular heart rates or abnormal temperature patterns. The results are displayed on a Flask-based dashboard, allowing real-time monitoring.

With an initial accuracy of 88% and an ROC of 0.68, the system continuously improves through iterative training. This setup provides a reliable, low-cost solution for remote health monitoring, making it ideal for hospitals, homes, or elderly care facilities
