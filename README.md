Functions:

getanswersfromexampaper: Extracts the answer to a specific question from a PDF exam paper using the "gemini-1.5-pro-001" model.
getanswersfrommarkscheme: Extracts the correct answer and sub-answers for a question from a PDF markscheme using the "gemini-1.5-flash-001" model.
answerquestion: Feeds a question about the correctness of the AI's answer to the "gemini-1.5-pro-001" model and prints the response.
generate, generateflash: These functions handle the image and text input to the models.
Main Loop:

The code iterates through questions 1 to 22.
For each question, it:
Gets the correct answer from the markscheme using getanswersfrommarkscheme.
Gets the AI's answer from the exam paper using getanswersfromexampaper.
Forms a summary question comparing the two answers and asking for "TRUE/FALSE" and an explanation.
Uses answerquestion to ask the AI to evaluate the correctness of its own answer.
The loop handles potential errors (e.g., API rate limits) by sleeping for 2 seconds and retrying.

![diagram1](./diagram1.png)

