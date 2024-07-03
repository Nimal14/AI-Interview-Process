# AI-Interview-Process
Sure! Here's an overview of the automated interview process based on the function and code snippets provided, along with the key modules involved:

### Overview of the Automated Interview Process

The automated interview process aims to streamline and enhance the initial phase of interviewing candidates by leveraging AI technologies, particularly Large Language Models (LLMs). This process involves extracting relevant information from candidates' resumes and generating tailored interview questions. It also uses text-to-speech (TTS) for interactions and evaluates candidate responses.

### Key Modules and Components

1. **Input Handling**
   - **PDF Upload:** The candidate uploads their resume in PDF format.
   - **File Handling:** The system generates a unique filename for the uploaded PDF based on the current date and time.

2. **Text Extraction**
   - **PDF Loading:** The system uses the `PyPDFLoader` from the `langchain` library to extract text content from the uploaded PDF.
   
3. **Language Model Interaction**
   - **LLM Configuration:** The system initializes settings for accessing the LLM (e.g., setting API keys and specifying the model version).
   - **Question Generation:** The LLM generates interview questions based on the extracted text from the resume. These questions are categorized into different types:
     - Basic Questions
     - Technical Questions
     - Moderate Questions
     - General Questions
   
4. **Text-to-Speech (TTS)**
   - **Greeting:** The system uses TTS to generate an audio greeting for the candidate, introducing itself as the interviewer.
   - **Interaction:** TTS can be used to read out the questions to the candidate during the interview process.

5. **Error Handling and Output**
   - **Error Messages:** If there are issues with loading the PDF or interacting with the LLM, the system generates appropriate error messages.
   - **Question Output:** Successfully generated questions are structured into a dictionary format for further processing or display.

6. **Interview Execution (Not Fully Covered in Provided Snippets)**
   - **Question Presentation:** The system presents the generated questions to the candidate, possibly using a combination of text and TTS.
   - **Response Collection:** The candidate's responses can be collected via text or voice input.
   - **Evaluation:** The system evaluates the responses based on predefined criteria and scoring metrics.

