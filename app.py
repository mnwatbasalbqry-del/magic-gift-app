from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('n')
    date = request.args.get('d')
    if name and date:
        return render_template('gift.html', name=name, date=date)
    return render_template('generator.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name')
    date = request.form.get('date')
    base_url = request.url_root
    final_url = f"{base_url}?n={name}&d={date}"
    
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(final_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#ff2b6b", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('result.html', name=name, url=final_url, qr_code=qr_base64)

if __name__ == '__main__':
    app.run(debug=True)
