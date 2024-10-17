from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route('/api/question', methods=['POST'])
def receive_question():
    data = request.get_json()
    question = data.get('question', '')
    print(f"Received question: {question}")

    # Temporary answer
    answer = "This is a temporary answer."

    return jsonify({"message": "Question received!", "answer": answer})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
