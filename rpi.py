import time
import json
import board
import busio
import adafruit_max30100
import spidev
import serial
import socket
import RPi.GPIO as GPIO

i2c = busio.I2C(board.SCL, board.SDA)
max30100 = adafruit_max30100.MAX30100(i2c)
max30100.enable_spo2()

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_temp(raw_adc):
    voltage = raw_adc * 3.3 / 1023.0
    return voltage * 100 

gps_serial = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

def read_gps():
    while True:
        line = gps_serial.readline().decode("utf-8", errors="ignore")
        if line.startswith("$GPGGA"):
            parts = line.split(",")
            try:
                lat = float(parts[2]) / 100.0
                lon = float(parts[4]) / 100.0
                return {"lat": lat, "lon": lon}
            except:
                return {"lat": 0, "lon": 0}

server_ip = '192.168.1.100' 
port = 5050

while True:
    try:
        max30100.refresh()
        hr = max30100.heart_rate
        spo2 = max30100.spO2
        temp_adc = read_channel(0)
        temp_c = round(convert_temp(temp_adc), 2)
        gps_data = read_gps()

        data = {
            "heart_rate": hr,
            "temperature_C": temp_c,
            "spo2": spo2,
            "gps": gps_data,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        msg = json.dumps(data).encode('utf-8')
        s = socket.socket()
        s.connect((server_ip, port))
        s.send(msg)
        s.close()
        print("Sent:", data)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
