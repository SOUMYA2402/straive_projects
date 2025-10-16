from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

faqs=["How can I reset my online banking password ?", "How do I check my account balance ?", "What should I do if my debit card is lost", "How can I apply for personal loan?", "How do I activate international transactions on my credit card"]
answers={
    faqs[0]: "You can reset your password by clicking 'Forgot Password' on the login page and following the verification steps",
    faqs[1]:"You can check your balance using mobile app, internet banking ot by visiting an ATM",
    faqs[2]:"Report the lost debit card immediately through customer service or banking app",
    faqs[3]:"You can apply for a personal loan online through bank's portal or visiting nearest branch",
    faqs[4]:"International Transaction can be activated via the mobile banking app or by customer care"
}

model=SentenceTransformer('all-MiniLM-L6-v2')
faq_embeddings=model.encode(faqs)

dimension=faq_embeddings.shape[1]
index=faiss.IndexFlatL2(dimension)
index.add(np.array(faq_embeddings))

user_query='How do I reset my online banking password ?'
query_embedding=model.encode([user_query])
number_of_results=1
distances, indices=index.search(np.array(query_embedding), number_of_results)

first_match_index=indices[0][0]
matched_faq=faqs[first_match_index]
matched_answer=answers[matched_faq]

print("User question:", user_query)
print("Matched FAQ:" , matched_faq)
print("Answer:" , matched_answer)
