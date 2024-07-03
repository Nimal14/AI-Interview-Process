from flask import Flask, render_template, request
from app import evaluate_question_answer_pairs, My_LLM_interviewer
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

all_question = []
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return "No file part"

    pdf = request.files['pdf']

    if pdf.filename == '':
        return "No selected file"

    # Save the uploaded PDF file
    pdf.save(pdf.filename)

    questions = My_LLM_interviewer(pdf.filename)

    global all_question
    all_question = []
    all_question.extend(questions['basic_questions'])
    all_question.extend(questions['technical_questions'])
    all_question.extend(questions['moderate_questions'])
    all_question.extend(questions['general_questions'])
    return render_template('success.html', questions=all_question)

from flask import jsonify
answers = []
feedback = []

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    global answers, feedback
    answers = request.form.getlist('answers[]')  # Get all answers as a list
    print(answers)

    dict = {}
    for i in range(len(all_question)):
        dict[all_question[i]] = answers[i]

    feedback = evaluate_question_answer_pairs(dict)
    return "ok"


@app.route('/result')
def results():
    return render_template('result.html', feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

