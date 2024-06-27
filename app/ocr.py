from PIL import Image
from io import BytesIO
from openbharatocr.ocr.aadhaar import extract_aadhaar, extract_dob, extract_name, extract_gender, extract_address, extract_fathers_name

import pytesseract

def process_results(results, img):
    extracted_data = {
        "aadharNo": "",
        "name": "",
        "dob": "",
        "gender": "",
        "address": ""
    }

    labels = ["aadharNo", "dob", "gender", "name", "address"]
    for result in results:
        for i, (bbox, cls) in enumerate(zip(result.boxes.xyxy, result.boxes.cls)):
            label = labels[int(cls)]
            x1, y1, x2, y2 = map(lambda x: int(x.item()), bbox)
            crop_img = img.crop((x1, y1, x2, y2))
            buffer = BytesIO()
            #if image format is jpg then save buffer according 
            if crop_img.format == 'JPEG':
                crop_img.save(buffer, format="JPEG")
            else:
                crop_img.save(buffer, format="PNG")
                
            buffer.seek(0)

            # OCR
            custom_config = r'--oem 3 --psm 6'
            ocr_result = pytesseract.image_to_string(Image.open(buffer), lang='eng', config=custom_config).replace('\n', ' ').strip()
            print(f"{label}: {ocr_result}")
            if label == "aadharNo":
                ocr_result = extract_aadhaar(ocr_result).replace(' ', '')
                
            if label == "name":
                ocr_result = extract_name(ocr_result)
                
            if label == "fathersName":
                ocr_result = extract_fathers_name(ocr_result)
                
            if label == "dob":
                ocr_result = extract_dob(ocr_result)
            extracted_data[label] = ocr_result

    return extracted_data
