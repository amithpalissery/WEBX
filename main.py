from flask import Flask, render_template, request, redirect, url_for
import os
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import HuggingFaceEndpoint

app = Flask(__name__)

# Load the HuggingFace model
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=512, temperature=0.5, token='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'
)

# Global variable to store embeddings
vectorindex_openai = None

# Store chat history
chat_history = []

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    global vectorindex_openai
    try:
        urls = [request.form[f'url{i}'] for i in range(1, 4)]

        # Load data
        loader = WebBaseLoader(urls)
        data = loader.load()

        # Split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=800,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(data)
        # Create embeddings and save to FAISS index
        embeddings = HuggingFaceHubEmbeddings()
        vectorindex_openai = FAISS.from_documents(docs, embeddings)

        return redirect(url_for('chatbot'))

    except Exception as e:
        return render_template('index.html', main_placeholder=f"Error: {e}")

@app.route('/chatbot', methods=['POST', 'GET'])
def chatbot():
    global chat_history, vectorindex_openai
    if request.method == 'POST':
        try:
            question = request.form.get('question')
            chat_response = ""

            if question and vectorindex_openai:
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorindex_openai.as_retriever())
                result = chain({"question": question}, return_only_outputs=True)
                chat_response = result.get("answer", "")
                chat_history.append({'sender': 'user', 'message': question})
                chat_history.append({'sender': 'bot', 'message': chat_response})
            else:
                chat_response = "No vectorstore available. Please process URLs first."

            return render_template('question.html', chat_response=chat_response, chat_history=chat_history)

        except Exception as e:
            print("Error occurred:", e)  # Add this line for debugging
            return render_template('index.html', chat_response=f"Error: {e}")
    else:
        return render_template('question.html', chat_history=chat_history)


@app.route('/process_urls', methods=['POST'])
def process_urls():
    # Process URLs here
    return render_template('question.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run()