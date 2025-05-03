from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

@app.route('/recibo.jpeg')
def tracker():
    # Obtener IP real, puede venir como 'ip1, ip2, ip3'
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    if forwarded_for:
        ip = forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr  # fallback

    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()

    print(f"{now} - IP: {ip} - UA: {ua}")
    return send_file("recibo.jpeg", mimetype="image/jpeg")
