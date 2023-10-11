import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from lmqg import TransformersQG
from tqdm import tqdm
import re


# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("lmqg/t5-large-squad-qg-ae")
# model = AutoModelForSeq2SeqLM.from_pretrained("lmqg/t5-large-squad-qg-ae")
model = TransformersQG(language='en', model='lmqg/t5-large-squad-qg-ae')

input_folder = '/Users/mounicaayalasomayajula/Desktop/DATA-298A/prompt/dataset/wellness'

# Create a list to hold the generated questions and answers
all_question_answer = []
files = os.listdir(input_folder)
sentence_delimiters = r'[.?!]\s+|;+\s+|[.?!]-+'

# Loop through all the files in the input folder
for filename in tqdm(os.listdir(input_folder), desc="Processing Files"):
    with open(os.path.join(input_folder, filename), 'r') as file:
        input_text = file.read()

    sentences = re.split(sentence_delimiters, input_text) # You can adjust the sentence delimiter as per your input text
    # Loop through each sentence
    for sentence in sentences:
        try:
            # Split sentence into chunks of 512 tokens
            chunked_text = tokenizer.batch_encode_plus([sentence], max_length=512, truncation=True, return_overflowing_tokens=True)
            for chunk in chunked_text['input_ids']:
                # Decode the chunked text back into string form
                chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
                question_answer = model.generate_qa(chunk_text, batch_size=1)
                all_question_answer.extend(question_answer)
        except:
            print("Answer not found for sentence: ", sentence)
            continue


    with open('output_wellness.txt', 'a') as file:
        for question, answer in question_answer:
            file.write("Question: " + question + "\n")
            file.write("Answer: " + answer + "\n\n")

# comment this for smaller directories - redundant loop
    
with open('output_wellness_duplicate.txt', 'w') as file:
        for question, answer in all_question_answer:
            file.write("Question: " + question + "\n")
            file.write("Answer: " + answer + "\n\n")

