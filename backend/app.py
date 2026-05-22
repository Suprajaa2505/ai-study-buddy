from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from models.database import init_db
from routes.upload_routes import upload_bp
from routes.chat_routes import chat_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
app.register_blueprint(upload_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'key_set': bool(os.getenv('GEMINI_API_KEY'))})

if __name__ == '__main__':
    init_db()
    print("🚀 Running on http://localhost:5000")
    app.run(debug=True, port=5000)