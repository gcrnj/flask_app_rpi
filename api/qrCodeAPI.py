from flask import Blueprint, Flask, send_file
import qrcode
from io import BytesIO

qrCodeAPI = Blueprint('qrCodeAPI', __name__)
@qrCodeAPI.route('/generate/<device_id>')
def generate_qr(device_id):
    # Generate QR Code
    qr = qrcode.make(device_id)
    
    # Save to a BytesIO stream
    img_io = BytesIO()
    qr.save(img_io, format='PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')