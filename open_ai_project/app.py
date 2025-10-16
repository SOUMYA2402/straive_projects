import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline

llm_pipeline=pipeline("text2text-generation", model='google/flan-t5-large')

def get_answer(question, docs):
    context=" ".join([doc.page_content for doc in docs])
    input_text=f"question : {question} context : {context}"
    result=llm_pipeline(input_text, max_length=256)
    return result[0]['generated_text']


#Upload PDF files
st.header("My first Chatbot")


with  st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader(" Upload a PDf file and start asking questions", type="pdf")


#Extract the text
if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
        #st.write(text)


#Break it into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=10000,
        chunk_overlap=750,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    #st.write(chunks)
    # generating embedding
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # creating vector store - FAISS
    vector_store = FAISS.from_texts(chunks, embeddings)


    # get user question
    user_question = st.text_input("Type Your question here")


    # do similarity search
    if user_question:
        match = vector_store.similarity_search(user_question,k=3)
        #st.write(match)

        answer=get_answer(user_question, match)

        st.subheader('Answer: ')
        st.write(answer)


