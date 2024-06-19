from flask import Flask, request, jsonify
import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chromadb.config import Settings
from langchain_google_genai import GoogleGenerativeAI
from getKeywords import getKeyWords
from makeCluster import makeClusterDocs
from genateHypotheticalDocs import generateHypotheticalDocs
from langchain_core.prompts import PromptTemplate
import time
from flask_cors import CORS
import threading


GOOGLE_API_KEY = "XXXXX"
os.environ["GOOGLE_API_KEY"] = "XXXXXX"

app = Flask(__name__)
CORS(app)


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = GoogleGenerativeAI(model="gemini-pro")
# genai.configure(api_key=GOOGLE_API_KEY)
# llm = genai.GenerativeModel('gemini-pro')

ROOT_DIRECTORY = os.path.dirname(os.path.realpath('__file__'))

CHROMA_SETTINGS = Settings(
    anonymized_telemetry=False,
    is_persistent=True,
)

db = Chroma(
    persist_directory=f"{ROOT_DIRECTORY}/DB",
    embedding_function=embeddings,
    client_settings=CHROMA_SETTINGS
)

text_store = {}

def delete_text():
    while True:
        time.sleep(10) 
        for key in list(text_store.keys()):
            if text_store[key]['expiry'] + 1200 >= time.time():
                del text_store[key]

# Start the daemon thread
delete_thread = threading.Thread(target=delete_text)
delete_thread.daemon = True
delete_thread.start()


template = """
I want you to act as a senior software developer. If anything is outside of tech, please say I don't know.
You can take references from the documents below to answer user question.

Reference Documents: {ref_documents}

Chat History: {chat_history}

Question: {question}

Answer: If possible, answer in a step-by-step manner."""

def filter_docs(docs, keywords, hypo_params):
    
    remaining_docs_with_keywords = list()
    
    print(f"""\n>>> Checking {len(docs)} Docs """)
    
    for r in docs[hypo_params['baseline_k']:]:
        page_content = r[0].page_content.lower()
        for keyword in keywords:
            if keyword.lower() in page_content:
                remaining_docs_with_keywords.append(r)
                continue
    
    print(f">>> ...{len(docs)-len(remaining_docs_with_keywords)} neglected Docs identified\n")
    
    return remaining_docs_with_keywords

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello i am live !!!'})

@app.route('/chat', methods=['POST'])
def process_json():
    try:
        json_data = request.get_json()
        uuid = json_data.get("uuid", 1)
        hypo_params = json_data.get("hypo_params", {
            'baseline_k': 10,
            'exploration_multiplier': 10
        })

        text = json_data.get("query", "")
        if text == "":
            return jsonify({'error': 'Query is empty'}), 400
        
        k = hypo_params['baseline_k'] * hypo_params['exploration_multiplier']
        
        docs = db.similarity_search_with_score(
            text, 
            k=k
        )
        
        query_keywords = getKeyWords(llm, text)
        
        remaining_docs = filter_docs(docs, query_keywords, hypo_params)
        
        cluster_docs = makeClusterDocs(embeddings, remaining_docs)
        
        hypothetical_docs = generateHypotheticalDocs(llm, cluster_docs, text)
        
        answerllm = GoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=GOOGLE_API_KEY)
        
        prompt = PromptTemplate.from_template(template)
        
        chain = prompt | answerllm
        
        history = ""
        global text_store
        if(uuid in text_store):
            history = text_store[uuid]['chat_history']
        else:
            text_store = {
                uuid: {
                    'chat_history': "",
                    'expiry': time.time()
                }
            }
        print (history)
        response = chain.invoke({
            'chat_history': history,
            'ref_documents': hypothetical_docs,
            'question': text
        })
        
        text_store[uuid]['chat_history'] += f"\nUser: {text}\nAI: {response}\n"
        
        
        return jsonify({'response': response})
    except Exception as e:
        print (e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
