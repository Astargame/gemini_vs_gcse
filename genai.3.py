import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import time

def getanswersfromexampaper (questionnumber):
  filename = "non_calc_foundation.pdf"
  filetype = "application/pdf"
  question = "Answer question " + str(questionnumber) + " in the exam paper.  Only give the answer not the workings"
  answer =  generate(filename,filetype,question)
  return answer

def getanswersfrommarkscheme (questionnumber):
  filename = "non_calc_foundation_markscheme.pdf"
  filetype = "application/pdf"
  question = "In the document extract the full answer and sub answers for question "+ str(questionnumber)  + ".  "
  answer = generateflash(filename,filetype,question)
  return answer

def answerquestion (questiontext): 
   #print("about to evaluate")
   #print(questiontext)
   responses = model.generate_content(
      [str(questiontext)],
      generation_config=generation_config,
      #safety_settings=safety_settings,
      stream=True,
   )

   for response in responses:
    print(response.text, end="")


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

   
def generateflash(filename,filetype,question):
    responsetext=""
    #print("about to evaluate")
    #print(question)
    encoded_image = base64.b64encode(open(filename, "rb").read()).decode("utf-8")
    image1 = Part.from_data(
        data=base64.b64decode(encoded_image), mime_type=filetype
    )

    responses = flashmodel.generate_content(
      [image1,question ],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
    )

    for response in responses:
        #print(response.text, end="")
        responsetext += response.text
    return responsetext



def generate(filename,filetype,question):
    responsetext=""
    #print("about to evaluate")
    #print(question)
    encoded_image = base64.b64encode(open(filename, "rb").read()).decode("utf-8")
    image1 = Part.from_data(
        data=base64.b64decode(encoded_image), mime_type=filetype
    )

    responses = model.generate_content(
      [image1,question ],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
    )

    for response in responses:
        #print(response.text, end="")
        responsetext += response.text
    return responsetext

    
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
vertexai.init(project="nimble-volt-364008", location="us-central1")
model = GenerativeModel(
    "gemini-1.5-pro-001",

)
flashmodel = GenerativeModel(
    "gemini-1.5-flash-001",

)

i = 0 
while i < 22:
    i = i+1
    evaluated = False
    while not evaluated:
        try:
            print("----------------")
            print("Question: " + str(i))
            markschemeanswer = getanswersfrommarkscheme(i)
            aianswer = getanswersfromexampaper(i)
            summary= "The official answer in the markscheme was ",markschemeanswer," and the ai answered ",aianswer,". Did the AI answer correctly?  Return TRUE / FALSE followed and an explanation of the reason why."

            print(summary)
            print("--------")
            answerquestion(summary)

            #print("The ai answered: \n", aianswer ,"\n  \n Whereas the correct answer from the mark scheme is: \n",markschemeanswer)
        except Exception as e:
            print("sleeping for 2 seconds ...")
            print(e)
            time.sleep(2)
        else:
            evaluated = True
        
