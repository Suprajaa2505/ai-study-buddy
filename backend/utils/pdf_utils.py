import fitz

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    pages = len(doc)
    text = ""
    for i in range(pages):
        t = doc[i].get_text("text")
        if t.strip():
            text += f"\n[Page {i+1}]\n{t}"
    doc.close()
    return text.strip(), pages

def chunk_text(text, size=1500, overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        if end < len(text):
            b = text.rfind('. ', start, end)
            if b > start + size // 2:
                end = b + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def build_context(query, chunks, max_chunks=5):
    if not chunks:
        return ""
    words = set(query.lower().split()) - {
        'the','a','an','is','in','on','at','to','for','of','and','or',
        'it','this','what','how','why','when','where','are','was','were',
        'be','have','has','do','does','will','can','me','my','i','you'
    }
    scored = sorted(
        [(sum(1 for w in words if w in c.lower()), c) for c in chunks],
        reverse=True
    )
    relevant = [c for s, c in scored if s > 0][:max_chunks]
    return "\n\n---\n\n".join(relevant or chunks[:3])