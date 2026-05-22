from flask import Blueprint, request, jsonify
from models.database import save_message, get_messages, get_session, get_db
from utils.pdf_utils import build_context
from utils.gemini_utils import ask_gemini
from routes.upload_routes import get_chunks

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/<sid>', methods=['POST'])
def chat(sid):
    if not get_session(sid):
        return jsonify({'error': 'Session not found'}), 404
    data = request.get_json()
    msg = data.get('message', '').strip()
    if not msg: return jsonify({'error': 'Empty message'}), 400

    chunks = get_chunks(sid)
    if not chunks:
        return jsonify({'error': 'Document not found. Please re-upload your PDF.'}), 404

    context = build_context(msg, chunks)
    history = get_messages(sid)

    try:
        reply = ask_gemini(msg, context, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    save_message(sid, 'user', msg)
    save_message(sid, 'assistant', reply)
    return jsonify({'response': reply, 'session_id': sid})

@chat_bp.route('/chat/<sid>/history', methods=['GET'])
def history(sid):
    if not get_session(sid): return jsonify({'error': 'Not found'}), 404
    return jsonify({'messages': get_messages(sid)})

@chat_bp.route('/chat/<sid>/clear', methods=['DELETE'])
def clear(sid):
    conn = get_db()
    conn.execute('DELETE FROM messages WHERE session_id=?', (sid,))
    conn.commit(); conn.close()
    return jsonify({'message': 'Cleared'})