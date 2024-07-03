# import datetime
from time import sleep
import pyttsx3
from gtts import gTTS
import playsound
import pyautogui
from pydub.generators import Sine
from pydub.playback import play
# import streamlit as st
import PyPDF2
import pdfplumber
import subprocess
import json
import random as random_shuff
import tiktoken
import openai
import os
from random import randint
import re
from langchain.document_loaders import PyPDFLoader
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory
# from langchain.llms import OpenAI
from flask import Flask, render_template, request, redirect, url_for
import time
import threading
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
from datetime import datetime
import json

openai.api_key = ''
GPT_MODEL = "gpt-4"
candidate_name = ""
bot_name = "Berry"

write_txt = True

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_pdfs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Opening JSON file
with open('config.json') as f:
    config = json.load(f)

BASIC_QUESTIONS = config["BASIC_QUESTIONS"]
TECHNICAL_QUESTIONS = config["TECHNICAL_QUESTIONS"]
bot_intro = config["BOT_INTRO"]
job_desc = config["JOB_DESC"]
end_note = config["END_NOTE"]
final_nt = "Your interview is over, you may leave now"

# tone config
# Define the frequency and duration of the tone
frequency = 500  # Frequency in Hz (A4 note)
duration_ms = 1000  # Duration in milliseconds
# Generate a sine wave tone with the given frequency and duration

prompt = ''' interview questions from the resume shared with the following conditions: 
            1. Find out the skill of the person who has shared this resume.
            2. Based on the skills Generate these types of questions ->  4 Easy Basic questions from resume mentioned, 4 Techinical Questions from the skills, 4 moderate level top skill focused Questions and 4 General Question's from skills which are not based on the resume and external.
            3. Output must be a dictionary where two key value pairs must present and keys are [ basic_questions, technical_questions, moderate_questions, general_questions ] The values are list of questions 4 each'''

intermediate_words = ["okay,  alright", "that's ok", "that's fine", "good", "noted that", "fine I've noted that",
                      "cool."]
basic_questions_promt = "Assume yourself as an interviewer and prepare 5 questions from the resume shared below with the following conditions. " \
                        "Output must be a list of questions."

technical_questions_promt = "generate 5 technical interview questions from the skill sets mentioned in the resume. output must be a list of questions"
promt_to_get_score = "Follow these conditions: \
            1. Assume yourself as an interviewer \
            2. candidate's answer must contain technical words related to the questions otherwise give low marks \
            3. give your result in a dictionary where value must be the score percentage"

evaluate_prompt = '''Assume yourself as an Interviewer. The dictionary shared here is the responses of a candidate 
                    who attended interview, where keys are questions and values are candidate's response.  dont display 
                    any coding. display only numbers, ie., scores in a list. Your response should have only list. 
                    dont display questions'''


def count_tokens(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def LLM_model(pdf_path, prompt):
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        questions_dict = {}
        if pages != []:
            embeddings = OpenAIEmbeddings(openai_api_key="")

            vectordb = Chroma.from_documents(pages, embedding=embeddings, persist_directory=".")
            # vectordb persist()

            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            pdf_qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.8), vectordb.as_retriever(),
                                                           memory=memory)

            query = "generate " + str(randint(1, 7)) + prompt
            result = pdf_qa({"question": query})
        else:
            result = "Could not parse your document. Make sure your PDF is a searchable PDF."
            print("Could not parse your document. Make sure your PDF is searchable.")
    except Exception as e:
        result = f"An error occurred: {str(e)}"
        print(f"An error occurred: {str(e)}")

    return result


def questions_gen(result):
    questions_dict = {}
    basic_que = result['answer'].split("technical_questions:")[0].replace("basic_questions:", ""). \
        replace("  ", "").split("\n")
    basic_que = [re.sub(r'\d+\.', '', question).strip() for question in basic_que if len(question) > 5]
    technical_que = result['answer'].split("technical_questions:")[1].replace("technical_questions:", "").replace(
        "  ", "").split("\n")
    technical_que = [re.sub(r'\d+\.', '', question).strip() for question in technical_que if len(question) > 5]
    questions_dict["basic_questions"] = basic_que
    questions_dict["technical_questions"] = technical_que
    return questions_dict


def play_tone(no_it):
    i = 0
    while (i < no_it):
        tone = Sine(frequency + 50)
        audio_segment = tone.to_audio_segment(duration=duration_ms)
        play(audio_segment)
        i += 1


def SpeakText(command, output_file):
    mp3_fp = BytesIO()
    tts = gTTS(text=command, lang='en')
    # tts.save("output.mp3")
    tts.write_to_fp(mp3_fp)
    print(mp3_fp)  # output <_io.BytesIO object at 0x0000025F69047150>
    with open(output_file, "wb") as f:  # Open in binary write mode
        f.write(mp3_fp.getvalue())
    playsound.playsound(os.path.join(os.getcwd(), output_file))
    os.remove(output_file)
    return


def SpeakText_2(command):
    return SpeakText(command, "output_2.mp3")


def SpeakText_3(command):
    return SpeakText(command, "output_3.mp3")


def SpeakText_4(command):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    return SpeakText(command, filename)


def SpeakText_5(command):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    return SpeakText(command, filename)


def SpeakText_6(command):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    return SpeakText(command, filename)


def SpeakText_7(command):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    return SpeakText(command, filename)


def SpeakText_8(command):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    return SpeakText(command, filename)


def SpeakText_9(command):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"
    return SpeakText(command, filename)


def get_greeting():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good morning There, Myself " + bot_name + " your interviewer"
    elif 12 <= current_hour < 17:
        greeting = "Good noon There, Myself " + bot_name + " your interviewer"
    elif 17 <= current_hour < 20:
        greeting = "Good evening There, Myself " + bot_name + " your interviewer"
    else:
        greeting = "Hello There, Myself " + bot_name + " your interviewer"

    return greeting


def save_uploaded_file(uploaded_file, filepath):
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())


def read_pdf_content(uploaded_file):
    content = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    with pdfplumber.open(uploaded_file) as pdf:
        for page_num in range(len(pdf_reader.pages)):
            page = pdf.pages[page_num]
            content += page.extract_text()
    return content


def evaluate_answers(resp_dict, evaluate_prompt):
    resp_str = "\n".join([f"{key}: {value}" for key, value in resp_dict.items()])
    score = LLM_model(resp_str + "\n", evaluate_prompt)
    return score


def evaluate_question_answer_pairs(pairs_dict):
    reports = []

    for question, answer in pairs_dict.items():
        prompt = f"question = '{question}', Answer = '{answer}'"
        if len(answer) < 5:
            report = {
                "question": question,
                "answer": answer,
                "score": "0",
                "feedback": "The Given Answer is Incorrect/Incomplete",
            }
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are a tutor who scores the answers out of 10. for the questions answer pair based on the accuracy of the answer to the given question. Give marks leniently from 8- 10 when the answer is correct, rest from 3-8 and when incorrect give less then equal to 1 marks. give output containing 'Score' ex- 5/10 and 'feedback'."},
                    {"role": "user", "content": prompt},
                ]
            )
            
            report = {
                "question": question,
                "answer": answer,
                "score": None,
                "feedback": None,
            }
    
            if 'choices' in response and len(response['choices']) > 0:
                choice = response['choices'][0]
                assistant_message = choice['message']
                content = assistant_message['content']
                if 'Score' in content or "10" in content:
                    # Extract the score and feedback
                    score_feedback = content.split('\n')
                    report["score"] = score_feedback[0].replace("Score", "")
                    fdbk = content.replace(score_feedback[0], "")
                    fdbk = fdbk.replace("Feedback", " ")
                    report["feedback"] = fdbk.replace("\n\n", " ")
    
                else:
                    # Extract the explanation
                    report["feedback"] = content

        reports.append(report)

    print(reports)

    return reports


def questioning(questions_dict):
    technical_qa = {}
    global prompt, BASIC_QUESTIONS, TECHNICAL_QUESTIONS, basic_questions_promt, technical_questions_promt, evaluate_prompt
    # SpeakText("Please Make sure your webcam and microphone are turned on before starting the technical interview, "
    #           "for better quality voice, you may use headphone if needed.")

    # pdf_filename = "suresh_cv____" #uploaded_file.name
    # pdf_save_path = os.path.join("uploaded_pdfs", pdf_filename)
    # # save_uploaded_file(uploaded_file, pdf_save_path)
    # sleep(1)
    # SpeakText("Your resume received. Please wait a moment")

    # query = "generate " + prompt
    # response = LLM_model(uploaded_file, query)
    # response = questions_gen(response)

    # Generating Questions from the CV
    if len(BASIC_QUESTIONS) == 0:
        BASIC_QUESTIONS = questions_dict["basic_questions"]
    print("\n Basic interview questions = ", BASIC_QUESTIONS, "\n")

    if len(TECHNICAL_QUESTIONS) == 0:
        TECHNICAL_QUESTIONS = questions_dict["technical_questions"]
    print("TECHNICAL_QUESTIONS = ", TECHNICAL_QUESTIONS)

    resp_dict = {}
    SpeakText_3("Lets start with the interview now")
    sleep(3)
    next_que = ["moving to the next question", "hm, okay next ", "hm next I want to ask you is that  ", " well. ",
                "aand ", "and well, "]
    import random
    random.shuffle(BASIC_QUESTIONS)
    random.shuffle(TECHNICAL_QUESTIONS)
    for basic_que in BASIC_QUESTIONS:
        SpeakText_4(basic_que)
        print(basic_que)
        user_response = input("Your response: ")
        while not user_response:
            # Keep waiting for user input until it's provided
            user_response = input("Please enter your response: ")
        resp_dict[basic_que] = user_response

        # pyautogui.hotkey("win", "h")
        sleep(2)
        SpeakText_5(next_que[randint(0, len(next_que) - 1)])
        sleep(1)
        SpeakText_6(intermediate_words[randint(0, len(intermediate_words) - 1)])
        sleep(2)

    for question in TECHNICAL_QUESTIONS:
        SpeakText_7(question)
        print("\n", question)
        user_response = input("Your response:")
        while not user_response:
            # Keep waiting for user input until it's provided
            user_response = input("Please enter your response:")
        technical_qa[question] = user_response

        # pyautogui.hotkey("win", "h")
        sleep(2)

    SpeakText_8(end_note)

    candidate_report = evaluate_question_answer_pairs(technical_qa)
    # candidate_report_basic = evaluate_question_answer_pairs(resp_dict)
    return candidate_report


def My_LLM_interviewer(pdf_path):
    print('Speaking')
    SpeakText(get_greeting(), "output.mp3")
    print('Spoken')

    pdf_filename = str(datetime.now()) + "__" + str(randint(0, 1000)) + ".pdf"
    # pdf_save_path = "/Users/HP/Downloads/ezyzip 2" + pdf_filename #os.path.join("uploaded_pdfs", pdf_filename)
    # save_uploaded_file(uploaded_file, pdf_save_path)

    SpeakText("Thank you. I've received your Resume, Please wait, Resume is being Loaded", "output1.mp3")
    loader = PyPDFLoader(pdf_path)
    # SpeakText("Thank you. I've received your Resume")
    # SpeakText("Please Make sure your webcam and microphone are turned on before starting the interview, \
    #           for better quality voice, you may use headphone if needed.")

    pages = loader.load_and_split()
    questions_dict = {}
    if pages != []:
        # embeddings = OpenAIEmbeddings(openai_api_key="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")
        sleep(1)
        page_contents = [document.page_content for document in pages]
        # vectordb = Chroma.from_texts(page_contents, embedding=embeddings, persist_directory=".")
        # vectordb.persist()
        sleep(1)
        # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        # pdf_qa = ConversationalRetrievalChain.from_llm(OpenAI(openai_api_key="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",temperature=0.8), vectordb.as_retriever(), memory=memory)
        # sleep(1)
        query = "generate " + str(randint(5, 10)) + prompt
        result = response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": query},
                {"role": "user", "content": (' ').join(page_contents)},
            ]
        )
        if 'choices' in response and len(response['choices']) > 0:
            choice = response['choices'][0]
            assistant_message = choice['message']
            content = json.loads(assistant_message['content'])
            result = {}

            result['answer'] = content

        print(type(content))
        print(content)

        try:
            """if type(eval(result['answer'])) == dict:
                technical_que = list(result['answer']["basic_questions"])
            else:
                basic_que = result['answer'].split("technical_questions:")[0].replace("basic_questions:", "").replace("  ", "").split("\n")
            #basic_que = [re.sub(r'\d+\.', '', question).strip() for question in basic_que if len(question)>5]

            if type(eval(result['answer'])) == dict:
                technical_que = list(result['answer']["technical_questions"])
            else:
                technical_que = result['answer'].split("technical_questions:")[1].replace("technical_questions:", "").replace("  ", "").split("\n")

            #technical_que = [re.sub(r'\d+\.', '', question).strip() for question in technical_que if len(question) > 5]
            questions_dict["basic_questions"] = basic_que
            questions_dict["technical_questions"] = technical_que
            print(questions_dict)
            print("DEBG"*10)
            #questioning(questions_dict)
            print("ALL QUESTIONS")
            print(questions_dict)"""
            technical_que = result['answer']['technical_questions']
            basic_que = result['answer']['basic_questions']
            questions_dict["moderate_questions"] = result['answer']['moderate_questions']
            questions_dict["general_questions"] = result['answer']['general_questions']
            questions_dict["basic_questions"] = basic_que
            questions_dict["technical_questions"] = technical_que
        except Exception as e:
            print(str(e))
            questions_dict = "Issue at question generation"
    else:
        questions_dict = "Could not parse your document. Make sure your pdf is searchable pdf or try again after sometime."

    return questions_dict


