import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from lmqg import TransformersQG

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("lmqg/t5-large-squad-qg-ae")
# model = AutoModelForSeq2SeqLM.from_pretrained("lmqg/t5-large-squad-qg-ae")
model = TransformersQG(language='en', model='lmqg/t5-large-squad-qg-ae')
# Set the path to the folder containing the input text files
input_folder = '/Users/mounicaayalasomayajula/Desktop/DATA-298A/scrape/data2/http/monu'

# Create a list to hold the generated questions and answers
all_question_answer = []

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    # Skip any files that are not text files
    if not filename.endswith('.php'):
        continue
    # Read the input text from the file
    with open(os.path.join(input_folder, filename), 'r') as file:
        input_text = file.read()
    # Generate the questions and answers for the input text
    question_answer = model.generate_qa(input_text)
    # Add the generated questions and answers to the list
    all_question_answer.extend(question_answer)

# Write the generated questions and answers to an output file
with open('output.txt', 'w') as file:
    for question, answer in all_question_answer:
        file.write("Question: " + question + "\n")
        file.write("Answer: " + answer + "\n\n")
