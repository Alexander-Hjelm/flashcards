import csv
import sys
from collections import Counter

# Usage:
# python3 word_frequency.py input.txt output.csv 100

def count_words(filename, num_words):
    with open(filename, 'r', encoding='utf-8') as file:
        words = file.read().lower().split()

    word_counts = Counter(words)
    common_words = word_counts.most_common(num_words)
    
    return common_words

def write_to_csv(common_words, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Word', 'Frequency'])

        for word, count in common_words:
            writer.writerow([word, count])

# Extract command-line arguments
if len(sys.argv) < 4:
    print("Usage: python word_frequency.py <input_file> <output_file> <num_words>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
num_words = int(sys.argv[3])

# Count words and write to CSV
word_counts = count_words(input_file, num_words)
write_to_csv(word_counts, output_file)
