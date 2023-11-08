from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textsum.summarize import Summarizer

tokenizer = AutoTokenizer.from_pretrained("pszemraj/led-large-book-summary")

model = AutoModelForSeq2SeqLM.from_pretrained("pszemraj/led-large-book-summary")
summarizer = Summarizer() 
# Read the input text from a file
with open('highlighted_housing-options.txt', 'r') as file:
    input_text = file.read()

out_str = summarizer.summarize_string(input_text)
print(f'summary: {out_str}')
#with open('output.txt', 'w') as file:
#    for question, answer in question_answer:
#        file.write("Question: " + question + "\n")
#        file.write("Answer: " + answer + "\n\n")

