from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

@app.route('/recibo.jpeg')
def tracker():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()

    # Guardar log
    with open("logs.txt", "a") as f:
        f.write(f"{now} - IP: {ip} - UA: {ua}\n")

    # Devolver la imagen
    return send_file("recibo.jpeg", mimetype="image/jpeg")
