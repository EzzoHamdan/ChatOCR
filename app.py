from flask import Flask, request, jsonify, render_template
from utils.task_handler import handle_file, generate_prompt, parse_quiz_response
from utils.chatgpt_utils import initialize_client, chatgpt_response
from config import Config, create_directories
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Flask app
app = Flask(__name__)
app.config.from_object(Config)
create_directories()

client = initialize_client()

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        query = request.form.get('query')
        task = request.form.get('task')
        file = request.files.get('file')
        pages_input = request.form.get('pages')

        if not query and not file:
            return jsonify({'error': 'Provide a query or file.'}), 400

        # Handle file and extract text
        extracted_text, filename = handle_file(file, app.config['UPLOAD_FOLDER'], pages_input)
        combined_text = query + "\n" + extracted_text if extracted_text else query

        # Generate the prompt
        prompt_to_send = generate_prompt(task, query, combined_text)

        # Call ChatGPT
        reply = chatgpt_response(client, prompt_to_send)
        return jsonify({'response': reply, 'prompt': prompt_to_send})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create-quiz', methods=['POST'])
def create_quiz():
    try:
        query = request.form.get('query')
        file = request.files.get('file')
        pages_input = request.form.get('pages')

        extracted_text, filename = handle_file(file, app.config['UPLOAD_FOLDER'], pages_input)
        combined_text = query + "\n" + extracted_text if extracted_text else query

        # Generate quiz-specific prompt
        prompt = f"Generate a multiple-choice quiz from the following text:\n{combined_text}\n\n" \
                 "Format each question as follows:\n" \
                 "Question: <Your question here>\n" \
                 "<Option 1>\n" \
                 "<Option 2>\n" \
                 "<Option 3>\n" \
                 "<Option 4>\n" \
                 "Correct: <Correct Option>\n" \
                 "NOTE: No need numbering the options, just write the options as they are.\n"

        # Get the response and parse it
        quiz_response = chatgpt_response(client, prompt)
        quiz_data = parse_quiz_response(quiz_response)
        return jsonify({'quizData': quiz_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
