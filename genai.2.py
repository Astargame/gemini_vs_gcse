import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import os

answer = open("answers.txt", "a")
def generate():
  vertexai.init(project="nimble-volt-364008", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
  )
  responses = model.generate_content(
      [image1, """solve question only give answer"""],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  for response in responses:
    print(response.text, end="")
    answer.write( response.text,)
answer.write("\n")


directory = 'workexperience'
 

for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.path)


    
encoded_image = base64.b64encode(open("question_9_non_calc.png", "rb").read()).decode("utf-8")
image1 = Part.from_data(
    data=base64.b64decode(encoded_image), mime_type="image/png"
)



    
    
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

generate()

