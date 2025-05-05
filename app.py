from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

# Página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener IP real
        forwarded = request.headers.get('X-Forwarded-For', '')
        ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
        ua = request.headers.get('User-Agent')
        msg = request.form.get('mensaje', '').strip()
        now = datetime.datetime.now().isoformat()

        print(f"{now} - IP: {ip} 🙂 - MENSAJE: {msg} - UA: {ua}")

        return "<h2>✅ Gracias, tu mensaje ha sido enviado.</h2>"

    return """
        <h2>💬 Deja un mensaje </h2>
        <form method="POST">
            <textarea name="mensaje" rows="4" cols="40" placeholder="Escribe aquí..." required></textarea><br><br>
            <button type="submit">Enviar</button>
        </form>
        <!-- Imagen rastreadora -->
        <img src="/recibo.jpeg" alt="recibo" width="1" height="1" style="display:none;">
    """

# Imagen rastreadora
@app.route('/recibo.jpeg')
def tracker():
    forwarded = request.headers.get('X-Forwarded-For', '')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()
    print(f"{now} - IP: {ip} 🙂 - UA: {ua}")
    return send_file("recibo.jpeg", mimetype="image/jpeg")
