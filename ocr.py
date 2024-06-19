from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import base64
import io
import json
import requests

app = Flask(__name__)
CORS(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    bold_words = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file and file.filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'tiff']:
        img = Image.open(file)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Call OCR API
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzIyYjAyZDktMWU0OC00Nzg0LThiNGItOGQyMzgzNWZhN2Q2IiwidHlwZSI6ImFwaV90b2tlbiJ9.WvgvhNN2knhsxLbyyFJlznsGHvmVtc1wwbvR18kBDOU"}
        url = "https://api.edenai.run/v2/ocr/ocr"
        data = {
            "providers": "google",
            "language": "en",
        }
        files = {"file": (file.filename, file, 'image/png')}
        response = requests.post(url, data=data, files=files, headers=headers)
        result = response.json()

        extracted_text = result['google']['text']
        bold_words = ' '.join([word for word in extracted_text.split() if word.isupper()])

        new_image_data = ImageData(image=img_str, text=extracted_text, bold_words=bold_words)
        db.session.add(new_image_data)
        db.session.commit()

        return jsonify({'text': extracted_text, 'bold_words': bold_words, 'image': img_str})
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/images', methods=['GET'])
def get_images():
    images = ImageData.query.all()
    return jsonify([{'id': img.id, 'text': img.text, 'bold_words': img.bold_words, 'image': img.image} for img in images])

if __name__ == '__main__':
    app.run(debug=True)
