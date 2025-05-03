from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

# Página principal que muestra la IP al visitante
@app.route('/')
def index():
    forwarded = request.headers.get('X-Forwarded-For', '')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    return f"""
        <h2>👋 Hola, tu IP es: {ip}</h2>
        <p>Tu visita ha sido registrada.</p>
        <img src='/recibo.jpeg' width='1' height='1'>
    """

# Imagen rastreadora que captura IP + UA
@app.route('/recibo.jpeg')
def tracker():
    forwarded = request.headers.get('X-Forwarded-For', '')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr

    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()

    print(f"{now} - IP: {ip} - UA: {ua}")
    return send_file("recibo.jpeg", mimetype="image/jpeg")
