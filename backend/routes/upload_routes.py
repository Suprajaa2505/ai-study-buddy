from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os, uuid, json

from models.database import create_session, get_all_sessions, get_session, delete_session
from utils.pdf_utils import extract_text_from_pdf, chunk_text
from utils.gemini_utils import generate_summary

upload_bp = Blueprint('upload', __name__)

CHUNKS_DIR = os.path.join(os.path.dirname(__file__), '..', 'chunks')

def save_chunks(session_id, chunks):
    os.makedirs(CHUNKS_DIR, exist_ok=True)
    with open(os.path.join(CHUNKS_DIR, f'{session_id}.json'), 'w') as f:
        json.dump(chunks, f)

def get_chunks(session_id):
    path = os.path.join(CHUNKS_DIR, f'{session_id}.json')
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)

def delete_chunks(session_id):
    path = os.path.join(CHUNKS_DIR, f'{session_id}.json')
    if os.path.exists(path):
        os.remove(path)


@upload_bp.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDFs allowed'}), 400

    session_id = str(uuid.uuid4())
    safe_name = f"{session_id}_{secure_filename(file.filename)}"
    folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_name)
    file.save(path)

    try:
        text, pages = extract_text_from_pdf(path)
    except Exception as e:
        os.remove(path)
        return jsonify({'error': str(e)}), 500

    if not text.strip():
        os.remove(path)
        return jsonify({'error': 'PDF is empty or image-only'}), 400

    chunks = chunk_text(text)
    save_chunks(session_id, chunks)
    create_session(session_id, safe_name, file.filename, pages, os.path.getsize(path))

    try:
        summary = generate_summary(chunks, file.filename)
    except:
        summary = f"Uploaded! {pages} pages ready. Ask me anything about it."

    return jsonify({'session_id': session_id, 'filename': file.filename,
                    'page_count': pages, 'summary': summary}), 201


@upload_bp.route('/sessions', methods=['GET'])
def list_sessions():
    return jsonify({'sessions': get_all_sessions()})


@upload_bp.route('/sessions/<sid>', methods=['DELETE'])
def remove_session(sid):
    s = get_session(sid)
    if not s: return jsonify({'error': 'Not found'}), 404
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], s['filename'])
    if os.path.exists(path): os.remove(path)
    delete_chunks(sid)
    delete_session(sid)
    return jsonify({'message': 'Deleted'})