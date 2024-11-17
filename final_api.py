from flask import Flask, request, jsonify
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import CTransformers
from langchain.llms import LlamaCpp

app = Flask(__name__)

#MODEL_PATH = r"/Users/Guest/Desktop/innovative/Meta-Llama-3.1-8B-Instruct.IQ3_M.gguf"
DB_FAISS_PATH = "vectorDB"

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

llama_model_path = r"/Users/Guest/Desktop/innovative/Meta-Llama-3.1-8B-Instruct.IQ3_M.gguf"
llm = LlamaCpp(
    model_path=llama_model_path,
    temperature=0,
    n_gpu_layers=-1,
    n_batch=512,
    n_ctx=8000,
    verbose=False
)
#llm = CTransformers(model=MODEL_PATH, model_type="llama", config={'max_new_tokens': 1024, 'temperature': 0.3, 'context_length': 2048})

def load_pdf_data(file_name: str):
    try:

        loader = PyPDFLoader(file_name)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
        text_chunks = text_splitter.split_documents(documents)
        docsearch = FAISS.from_documents(text_chunks, embeddings)
        retriever = docsearch.as_retriever()
        qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)
        return qa_chain, docsearch, documents
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

@app.route("/query", methods=["POST"])
def query_pdf():
    try:
        input_data = request.json
        file_name = input_data.get('file_name')
        query = request.args.get('query')

        if not file_name or not query:
            return jsonify({"error": "File name and query are required"}), 400
        qa_chain, docsearch, documents = load_pdf_data(file_name)
        chat_history = []
        query += " answer only related to the document you have, do not add any more sentences to the answer by yourself, answer in a concise and effective manner with no useless sentences"
        response = qa_chain({"question": query, "chat_history": chat_history})
        return jsonify({"message": response['answer']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/summarize", methods=["POST"])
def summarize_pdf():
    try:
        input_data = request.json
        file_name = input_data.get('file_name')

        if not file_name:
            return jsonify({"error": "File name is required"}), 400

        qa_chain, docsearch, documents = load_pdf_data(file_name)
        text_content = " ".join([doc.page_content for doc in documents])
        summary = llm("Summarize the following content:\n" + text_content)
        return jsonify({"message": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8000)
