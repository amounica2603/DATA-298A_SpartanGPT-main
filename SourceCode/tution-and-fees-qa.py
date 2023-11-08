import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from lmqg import TransformersQG
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained("lmqg/t5-large-squad-qg-ae")
# model = AutoModelForSeq2SeqLM.from_pretrained("lmqg/t5-large-squad-qg-ae")
model = TransformersQG(language='en', model='lmqg/t5-large-squad-qg-ae')

input_folder = '/Users/mounicaayalasomayajula/Desktop/DATA-298A/prompt/dataset/wellness'

all_question_answer = []
files = os.listdir(input_folder)

progress_bar = tqdm(iterable=files, total=len(files), desc="Processing files", unit="file", dynamic_ncols=True)
for filename in files:
    with open(os.path.join(input_folder, filename), 'r',encoding='utf-8', errors='ignore') as file:
        input_text = file.read()
        # Truncate the input text to 512 tokens
        input_text = input_text[:512]

        # Generate the questions and answers for the truncated input text
        question_answer = model.generate_qa(input_text)
        all_question_answer.extend(question_answer)

    # Write the generated questions and answers to an output file
    with open('output_wellness2.txt', 'a', encoding='utf-8') as file:
        for question, answer in question_answer:
            file.write("Question: " + question + "\n")
            file.write("Answer: " + answer + "\n\n")

# comment this loop for smaller directories - redundant loop

with open('output_wellness2_duplicate.txt', 'w', encoding='utf-8') as file:
    for question, answer in all_question_answer:
        file.write("Question: " + question + "\n")
        file.write("Answer: " + answer + "\n\n")

#    progress_bar.update(1)

#progress_bar.close()
