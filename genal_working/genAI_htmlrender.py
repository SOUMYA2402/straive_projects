from flask import Flask, request, jsonify, render_template_string
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
import json

# ----------------------
# Step 1: Create Banking FAQs
# ----------------------
faqs = [
    "How can I reset my online banking password?",
    "How do I check my account balance?",
    "What should I do if my debit card is lost?",
    "How can I apply for a personal loan?",
    "How do I activate international transactions on my credit card?"
]

# ----------------------
# Step 2: Load Embedding Model
# ----------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
faq_embeddings = model.encode(faqs)

# ----------------------
# Step 3: Create FAISS Index
# ----------------------
dimension = faq_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(faq_embeddings))

# ----------------------
# Step 4: Initialize Flask and Gemini API
# ----------------------
app = Flask(__name__)

def get_gemini_answer(query: str, context: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY environment variable not set."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    prompt = f"""
You are a friendly and helpful banking assistant.
The user's question is: "{query}"
A relevant FAQ from our knowledge base is: "{context}"

Please provide a concise and conversational answer to the user's question,
using only the information provided by the relevant FAQ.
"""

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_json = response.json()

        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            candidate = response_json['candidates'][0]
            if 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                return candidate['content']['parts'][0]['text'], None

        return None, "Invalid API response format."

    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

@app.route('/')
def home():
    return "Welcome to the Banking FAQ Semantic Search API!"

@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'GET':
        return jsonify({
            "message": "Please POST a JSON payload with {'question': 'your question here'} to get an answer."
        })

    data = request.json
    if not data or 'question' not in data:
        return jsonify({"error": "Please provide a question in JSON format: {'question': 'your question here'}"}), 400

    user_query = data['question']
    query_embedding = model.encode([user_query])
    distances, indices = index.search(np.array(query_embedding), 1)
    first_match_index = indices[0][0]
    matched_faq = faqs[first_match_index]

    gemini_answer, error = get_gemini_answer(user_query, matched_faq)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({
        "user_question": user_query,
        "matched_faq": matched_faq,
        "answer": gemini_answer,
        "distance": float(distances[0][0])
    })

# ----------------------
# Step 5: Chat UI
# ----------------------
CHATBOT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Banking FAQ Chatbot</title>
<style>
    body {
        margin: 0;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-container {
        width: 420px;
        height: 600px;
        display: flex;
        flex-direction: column;
        border-radius: 20px;
        backdrop-filter: blur(12px);
        background: rgba(255, 255, 255, 0.85);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        overflow: hidden;
        transition: background 0.3s;
    }
    .dark .chat-container {
        background: rgba(25, 25, 25, 0.85);
        color: #f0f0f0;
    }
    /* Header */
    .chat-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 15px;
        background: #007bff;
        color: white;
        font-weight: bold;
    }
    .chat-header img {
        width: 35px;
        height: 35px;
        border-radius: 50%;
    }
    .status {
        font-size: 12px;
        color: #d4fdd4;
        font-weight: normal;
    }
    /* Chat Area */
    #chatbox {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .msg {
        display: flex;
        opacity: 0;
        transform: translateY(10px);
        animation: fadeIn 0.3s forwards;
    }
    .user-msg { justify-content: flex-end; }
    .bot-msg { justify-content: flex-start; }
    .user-msg span {
        background: #007bff;
        color: white;
        padding: 10px 14px;
        border-radius: 18px 18px 0 18px;
        max-width: 75%;
    }
    .bot-msg span {
        background: #e9ecef;
        color: #333;
        padding: 10px 14px;
        border-radius: 18px 18px 18px 0;
        max-width: 75%;
    }
    .dark .bot-msg span {
        background: #333;
        color: #f0f0f0;
    }
    /* Input Area */
    .chat-input {
        display: flex;
        align-items: center;
        padding: 10px;
        border-top: 1px solid #ddd;
        background: #fff;
    }
    .dark .chat-input { background: #1e1e1e; border-color: #444; }
    #question {
        flex: 1;
        padding: 12px;
        font-size: 15px;
        border: 1px solid #ccc;
        border-radius: 20px;
        outline: none;
        background: #fafafa;
    }
    .dark #question { background: #2b2b2b; color: #fff; border-color: #555; }
    #send-btn {
        background: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        width: 44px;
        height: 44px;
        margin-left: 8px;
        cursor: pointer;
        font-size: 18px;
    }
    #send-btn:hover { background: #0056b3; }
    /* Typing */
    .typing span {
        display: inline-block;
        animation: blink 1.5s infinite;
    }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink { 0%,100% {opacity:.2} 20% {opacity:1} }
    @keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
    /* Toggle */
    .toggle-btn {
        margin-left: auto;
        cursor: pointer;
        background: none;
        border: none;
        color: white;
        font-size: 18px;
    }
</style>
</head>
<body>
    <div class="chat-container" id="chat-container">
        <div class="chat-header">
            <img src="https://i.ibb.co/7Rj0rVp/bot-avatar.png" alt="Bot">
            <div>
                Banking Bot <div class="status">online</div>
            </div>
            <button class="toggle-btn" id="toggleTheme">🌙</button>
        </div>
        <div id="chatbox"></div>
        <div class="chat-input">
            <input type="text" id="question" placeholder="Type a message..." autocomplete="off" />
            <button id="send-btn">➤</button>
        </div>
    </div>

<script>
    const chatbox = document.getElementById('chatbox');
    const questionInput = document.getElementById('question');
    const sendBtn = document.getElementById('send-btn');
    const chatContainer = document.getElementById('chat-container');
    const toggleTheme = document.getElementById('toggleTheme');

    function appendMessage(sender, message) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'msg ' + (sender === 'user' ? 'user-msg' : 'bot-msg');
        const span = document.createElement('span');
        span.textContent = message;
        msgDiv.appendChild(span);
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function appendTyping() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'msg bot-msg typing-indicator';
        const span = document.createElement('span');
        span.className = 'typing';
        span.innerHTML = '<span>.</span><span>.</span><span>.</span>';
        msgDiv.appendChild(span);
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function removeTyping() {
        const typingDiv = document.querySelector('.typing-indicator');
        if (typingDiv) typingDiv.remove();
    }

    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) return;

        appendMessage('user', question);
        questionInput.value = '';
        questionInput.disabled = true;
        sendBtn.disabled = true;

        appendTyping();

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            removeTyping();

            if (!response.ok) {
                appendMessage('bot', "⚠️ Something went wrong. Try again.");
                return;
            }

            const data = await response.json();
            appendMessage('bot', data.answer);
        } catch (error) {
            removeTyping();
            appendMessage('bot', "⚠️ Server error.");
        } finally {
            questionInput.disabled = false;
            sendBtn.disabled = false;
            questionInput.focus();
        }
    }

    sendBtn.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') sendQuestion();
    });

    toggleTheme.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        toggleTheme.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
    });
</script>
</body>
</html>
"""


@app.route('/chat')
def chat():
    return render_template_string(CHATBOT_HTML)

if __name__ == '__main__':
    app.run(debug=True)
