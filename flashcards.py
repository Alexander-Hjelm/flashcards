import random
import argparse
import os

# USAGE: python3 .\flashcards.py C:\Users\Alexander\Documents\chinese\chinese.md

class Flashcard:
    def __init__(self, question, answer, description):
        self.question = question
        self.answer = answer
        self.description = description

    def __str__(self):
        return f"{self.question} -> {self.answer} | {self.description}"

class WordMetadata:
    def __init__(self, word, score, omitted):
        self.word = word
        self.score = score
        self.omitted = omitted

    def __str__(self):
        return f"{self.word}%%{self.score}%%{self.omitted}\n"
    
    def from_string(string):
        split = string.split("%%")
        return WordMetadata(split[0].strip(), split[1].strip(), split[2].strip())

# Define the command-line arguments
parser = argparse.ArgumentParser(description='Read a Markdown file and output its contents.')
parser.add_argument('words_file', metavar='words_file', type=str, help='the path to the Markdown file to read')

# Parse the command-line arguments
args = parser.parse_args()

words_file = args.words_file
meta_file = "metafile.txt"
meta_data = []
meta_file_created_this_run = False

# Check if the metafile already exists
if os.path.exists(meta_file):
    print("File already exists! Aborting save.")
else:
    # Write the file to disk
    with open(meta_file, 'w') as file:
        file.write("")
    meta_file_created_this_run = True
    print("File saved successfully!")

# Open the words file and read its contents line by line
with open(words_file, 'r', encoding='UTF8') as file:
    words_lines = file.readlines()

# Open the meta file and read its contents line by line
with open(meta_file, 'r', encoding='UTF8') as file:
    meta_file_contents = file.readlines()
    for meta_file_content in meta_file_contents:
        meta_data.append(WordMetadata.from_string(meta_file_content))

flashcards = []

# Initialize flashcards
for line in words_lines:
    if line.startswith("|"):
        line_formatted = line.strip()
        line_split = line_formatted.split("|")
        question = line_split[1].strip()
        description = line_split[2].strip()
        answer = line_split[3].strip()
        flashcard = Flashcard(question, answer, description)
        flashcards.append(flashcard)

# Initialize metadata
if meta_file_created_this_run:
    for flashcard in flashcards:
        meta_data_filtered = filter(lambda n: n.word == flashcard.question, meta_data)
        if len(list(meta_data_filtered)) == 0:
            meta_data.append(WordMetadata(flashcard.question, 0.0, 0))

# Remove flashcards not in metadata
flashcards_new = []
for meta in meta_data:
    flashcards_filtered = list(filter(lambda n: n.question == meta.word, flashcards))
    if len(flashcards_filtered) > 0 and meta.omitted == "0":
        flashcards_new.append(flashcards_filtered[0])

flashcards = flashcards_new

# Write meta data to disk
with open(meta_file, 'w', encoding='UTF8') as file:
    for meta in meta_data:
        file.write(str(meta))

# Function to start the flashcard quiz
def start_flashcards():
    print("Welcome to the Flashcard Quiz!")
    print("Type 'quit' at any time to exit.\n")
    correct_answers = 0
    total_questions = 0
    score_eval_attempts = 0
    score_eval_attempts_max = 999999
    while True:
        if score_eval_attempts > score_eval_attempts_max:
            print("You have already reached max score on all flash cards, good job!")
            break

        flashcard = random.choice(flashcards)
        meta_data_filtered = list(filter(lambda n: n.word == flashcard.question, meta_data))[0]

        # Evaluate previous score
        score = float(meta_data_filtered.score)
        random_float = random.random()
        if random_float < score:
            score_eval_attempts = score_eval_attempts + 1
            continue
        score_eval_attempts = 0

        total_questions += 1
        print("Question", total_questions, ":", flashcard.question)
        user_answer_1 = input("Think of an answer and press enter...")
        if user_answer_1.lower() == 'quit':
            break
        print(f"The correct answer was: {flashcard.answer} ({flashcard.description})", )
        user_answer_2 = ""
        while user_answer_2.lower() != "y" and user_answer_2.lower() != "n" and user_answer_2.lower() != "omit" and user_answer_2.lower() != "quit":
            user_answer_2 = input("Was you answer correct? (y/n/omit)")
        if user_answer_2.lower() == 'omit':
            print("Omitting card: ", flashcard.question)
            meta_data_filtered.omitted = 1
            flashcards_filtered = list(filter(lambda n: n.question == flashcard.question, flashcards))
            flashcards.remove(flashcards_filtered[0])
        elif user_answer_2.lower() == 'y':
            print("Good job!")
            score = score + 0.1
            score = max(score, 0)
            score = min(score, 1)
            meta_data_filtered.score = str(score)
            correct_answers = correct_answers + 1
        elif user_answer_2.lower() == 'n':
            print("Bad dog!")
            score = score - 0.1
            score = max(score, 0)
            score = min(score, 1)
            meta_data_filtered.score = str(score)
        elif user_answer_2.lower() == 'quit':
            break

        # Write meta data to disk
        with open(meta_file, 'w', encoding='UTF8') as file:
            for meta in meta_data:
                file.write(str(meta))

    print("Exiting flashcards...")
    print("You got", correct_answers, "out of", min(correct_answers, max(0, total_questions-1)), "correct.")

# Call the start_flashcards function to start the quiz
start_flashcards()
