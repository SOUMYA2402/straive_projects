from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

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

answers = {
    faqs[0]: "You can reset your password by clicking 'Forgot Password' on the login page and following the verification steps.",
    faqs[1]: "You can check your balance using the mobile app, internet banking, or by visiting an ATM.",
    faqs[2]: "Report the lost debit card immediately through the customer service helpline or the banking app.",
    faqs[3]: "You can apply for a personal loan online through the bank’s portal or by visiting your nearest branch.",
    faqs[4]: "International transactions can be activated via the mobile banking app or by contacting customer care."
}

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
# Step 4: Initialize Flask
# ----------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Banking FAQ Semantic Search API!"

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        user_query = data.get('question', '')
        if not user_query:
            return jsonify({"error": "Please provide a question in JSON format: {'question': 'your question here'}"}), 400

        # Encode user query
        query_embedding = model.encode([user_query])

        # Search FAISS index
        distances, indices = index.search(np.array(query_embedding), 1)
        first_match_index = indices[0][0]
        matched_faq = faqs[first_match_index]
        matched_answer = answers[matched_faq]

        return jsonify({
            "user_question": user_query,
            "matched_faq": matched_faq,
            "answer": matched_answer,
            "distance": float(distances[0][0])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

