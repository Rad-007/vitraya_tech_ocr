import requests
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import base64
import io

app = Flask(__name__)
CORS(app)


# PostgreSQL database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    bold_words = db.Column(db.Text, nullable=False)

# Create the database tables within the application context
with app.app_context():
    db.create_all()

OCR_API_KEY = 'K81602001788957'  # Replace with your OCR.space API key

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

        # Perform OCR using OCR.space API
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={file.filename: buffered.getvalue()},
            data={
                'apikey': OCR_API_KEY,
                'language': 'eng'
            }
        )

        if response.status_code != 200:
            return jsonify({'error': 'OCR API request failed'}), 500

        result = response.json()
        extracted_text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')

        # Identify bold words (for demonstration, we'll consider uppercase words as bold)
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
