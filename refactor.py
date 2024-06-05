import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import time

# Define constants for file paths and content types
EXAM_PAPER_FILENAME = "non_calc_foundation.pdf"
MARKSCHEME_FILENAME = "non_calc_foundation_markscheme.pdf"
FILETYPE = "application/pdf"

# Define generation configuration and safety settings
GENERATION_CONFIG = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Initialize Vertex AI
vertexai.init(project="nimble-volt-364008", location="us-central1")

# Load Gemini models
model = GenerativeModel("gemini-1.5-pro-001")
flashmodel = GenerativeModel("gemini-1.5-flash-001")

def generate_response(model, filename, question):
    """Generates a response using the given model, file, and question."""
    encoded_image = base64.b64encode(open(filename, "rb").read()).decode("utf-8")
    image1 = Part.from_data(data=base64.b64decode(encoded_image), mime_type=FILETYPE)
    
    responses = model.generate_content(
        [image1, question],
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
        stream=True,
    )

    response_text = ""
    for response in responses:
        response_text += response.text
    
    return response_text

def get_answer_from_exam_paper(question_number):
    """Gets the answer to a question from the exam paper."""
    question = f"Answer question {question_number} in the exam paper. Only give the answer, not the workings."
    return generate_response(model, EXAM_PAPER_FILENAME, question)

def get_answer_from_markscheme(question_number):
    """Gets the answer to a question from the markscheme."""
    question = f"In the document, extract the full answer and sub-answers for question {question_number}."
    return generate_response(flashmodel, MARKSCHEME_FILENAME, question)

def evaluate_question(question_number):
    """Evaluates the AI's answer against the markscheme answer."""
    markscheme_answer = get_answer_from_markscheme(question_number)
    ai_answer = get_answer_from_exam_paper(question_number)

    summary = f"The official answer in the markscheme was {markscheme_answer} and the AI answered {ai_answer}. Did the AI answer correctly? Return TRUE / FALSE followed by an explanation of the reason why."
    
    print("----------------")
    print(f"Question: {question_number}")
    print(summary)
    print("--------")

    answerquestion(summary)

def answerquestion(question_text):
    """Generates and prints a response to the given question."""
    responses = model.generate_content(
        [str(question_text)],
        generation_config=GENERATION_CONFIG,
        #safety_settings=safety_settings,
        stream=True,
    )
    
    for response in responses:
        print(response.text, end="")

# Loop through questions and evaluate each one
for i in range(1, 23):
    evaluated = False
    while not evaluated:
        try:
            evaluate_question(i)
            evaluated = True
        except Exception as e:
            print("Sleeping for 2 seconds ...")
            print(e)
            time.sleep(2)