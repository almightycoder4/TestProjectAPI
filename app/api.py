from flask import Blueprint, request, jsonify
from .ocr import detect_and_crop

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/aadhaarOcr', methods=['POST'])
def aadhaar_ocr():
    data = request.get_json()
    image_url = data.get('imgUrl')

    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    try:
        extracted_data = detect_and_crop(image_url)
        return jsonify({"extractedData": extracted_data}), 200
    except Exception as e:
        print(e, "error")
        return jsonify({"error": str(e)}), 500
