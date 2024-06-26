from flask import Flask

def create_app():
    app = Flask(__name__)

    from .api import ocr_bp
    app.register_blueprint(ocr_bp, url_prefix='/')

    return app
