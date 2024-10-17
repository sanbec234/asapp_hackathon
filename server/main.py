from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import login
import json
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
import cassio
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

app = Flask(__name__)
CORS(app, origins='*')

def initialize_services():
    try:
        login(token="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")
        ASTRA_DB_APPLICATION_TOKEN = "AstraCS:cUIKsAZQgdsZUzMlAOJsnxbR:808bfd213aa188fd28cdf20bfda17a3ca87795965057c84e2d53b19cf04fce3c"
        ASTRA_DB_ID = "31282abc-868e-4c75-906e-adf466f86267"
        cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        astra_vector_store = Cassandra(embedding=embeddings, session=None, keyspace=None, table_name="Nurtura")
        astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

        return astra_vector_index
    except Exception as e:
        print(f"Error initializing services: {e}")
        return None

astra_vector_index = initialize_services()

@app.route('/api/question', methods=['POST'])
def receive_question():
    if not astra_vector_index:
        return jsonify({"error": "Service initialization failed."}), 500

    data = request.get_json()
    questions = data.get('question', '')
    
    if not questions:
        return jsonify({"error": "No question provided."}), 400

    print(f"Received question: {questions}")

    try:
        with open('paper_metadata.json', 'r') as file:
            auth_data = json.load(file)

        json_string = " ".join([f"{key}: {value}" for key, value in auth_data.items()]).strip()

        retriever = astra_vector_index.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.55, 'k': 10}
        )

        retrieved_docs = retriever.invoke(questions)

        rag_content = [f"Content: {doc.page_content} Source: {doc.metadata['source']}" for doc in retrieved_docs]
        print("Retrieved Chunks:\n", rag_content)

        llm = ChatGroq(groq_api_key="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", model_name="Llama-3.1-70b-Versatile")

        context = f"Context: {rag_content}"
        system_prompt = f"""
        You are an AI assistant specialized in providing expert answers based on the provided documents.
        
        If the user's input, "{questions}", is a greeting or general conversation (e.g., small talk or casual questions), respond in a friendly and conversational manner, like a normal chatbot.

        If the input is a question requiring expert knowledge, such as: "{questions}", follow these steps:
        1. Extract the most relevant information from the provided content: "{context}".
        2. Cite the author and title of the papers from the provided data: "{json_string}" where applicable.
        3. Always start your response by mentioning the source (title of the paper) before explaining the key information from the context.

        Ensure your response is:
        - Clear and concise and breif.
        - Directly answers the user's question based on the provided documents.
        - Well-structured with the relevant citations where necessary.
        """


        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=questions)
        ]

        output_generate = llm.invoke(messages)
        print("Generated Response:\n", output_generate)

        # Convert the output to a string if it's not already
        answer = str(output_generate) if isinstance(output_generate, str) else output_generate.content

        return jsonify({"message": "Question received!", "answer": answer})

    except Exception as e:
        print(f"Error processing the question: {e}")
        return jsonify({"error": "An error occurred while processing the question."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
