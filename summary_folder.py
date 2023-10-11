## This is to have a folder as input and summarize all text files in it.
## This will also address any unicode-decode error for utf-8 encoding.

import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textsum.summarize import Summarizer

# Set the path to the input folder containing text files
input_folder_path = '/Users/mounicaayalasomayajula/Desktop/DATA-298A/prompt/dataset/chhs'

# Set the path to the output folder for summarized text files
output_folder_path = '/Users/mounicaayalasomayajula/Desktop/DATA-298A/prompt/dataset/chhs/summarized_chhs/'

# Create the output folder if it does not exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Load the summarizer model
tokenizer = AutoTokenizer.from_pretrained("pszemraj/led-large-book-summary")
model = AutoModelForSeq2SeqLM.from_pretrained("pszemraj/led-large-book-summary")
summarizer = Summarizer(tokenizer=tokenizer, model=model)

# Get a list of all files in the input folder
all_files = os.listdir(input_folder_path)

# Loop through the files
for filename in all_files:
    # Construct the full file path for the input file
    input_file_path = os.path.join(input_folder_path, filename)
    
    # Skip directories and non-text files
    if os.path.isdir(input_file_path) or not filename.endswith('.txt'):
        continue
    
    # Read the input text from the input file
    with open(input_file_path, 'r', encoding="ISO-8859-1") as file:
        input_text = file.read()
    
    # Summarize the input text
    summarized_text = summarizer.summarize_string(input_text)
    
    # Construct the filename for the output summarized file
    output_filename = f'summarized_{filename}'
    # Construct the full file path for the output summarized file
    output_file_path = os.path.join(output_folder_path, output_filename)
    
    # Save the summarized text to the output summarized file
    with open(output_file_path, 'w') as file:
        file.write(summarized_text)
        
    print(f'Summarized file saved: {output_file_path}')
