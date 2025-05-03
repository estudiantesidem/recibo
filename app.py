from flask import Flask, request, send_file
import datetime

app = Flask(__name__)

@app.route('recibo.jpeg')
def tracker():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    now = datetime.datetime.now().isoformat()
    print(f"{now} - IP: {ip} - UA: {ua}")
    return send_file("recibo.jpeg", mimetype="image/jpeg")

