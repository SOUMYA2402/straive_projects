# app_gemini.py

# Install before running:
# pip install Flask sentence-transformers faiss-cpu requests

from flask import Flask, request, jsonify
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


# Function to get answer from Gemini API
def get_gemini_answer(query: str, context: str):
    """
    Sends a prompt to the Gemini API and returns the generated text.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY environment variable not set."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # Build the prompt with context from the most relevant FAQ
    prompt = f"""
    You are a friendly and helpful banking assistant.
    The user's question is: "{query}"
    A relevant FAQ from our knowledge base is: "{context}"

    Please provide a concise and conversational answer to the user's question,
    using only the information provided by the relevant FAQ.
    """

    headers = {
        'Content-Type': 'application/json'
    }
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
        response.raise_for_status()  # Raise an exception for bad status codes
        response_json = response.json()

        # Check for candidates and content in the response
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


@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        user_query = data.get('question', '')
        if not user_query:
            return jsonify(
                {"error": "Please provide a question in JSON format: {'question': 'your question here'}"}), 400

        # Encode user query
        query_embedding = model.encode([user_query])

        # Search FAISS index
        distances, indices = index.search(np.array(query_embedding), 1)
        first_match_index = indices[0][0]
        matched_faq = faqs[first_match_index]

        # Get the Gemini-generated answer based on the retrieved FAQ
        gemini_answer, error = get_gemini_answer(user_query, matched_faq)

        if error:
            return jsonify({"error": error}), 500

        return jsonify({
            "user_question": user_query,
            "matched_faq": matched_faq,
            "answer": gemini_answer,
            "distance": float(distances[0][0])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
