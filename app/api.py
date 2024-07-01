from flask import Blueprint, request, jsonify, current_app
from PIL import Image
from io import BytesIO
import requests
from .ocr import process_results

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/aadhaarOcr', methods=['POST'])
def aadhaar_ocr():
    data = request.get_json()
    img_url = data.get('imgUrl')

    if not img_url:
        return jsonify({"error": "Image URL is required"}), 400

    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))

        # Check image format
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            return jsonify({"error": "Invalid image format. Only JPG and PNG are supported."}), 400

        # Run detection
        model = current_app.model
        results = model.predict(source=img, save=False)
        extracted_data = process_results(results, img)

        return jsonify(extracted_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
