import csv
import json

# File path for the input CSV file
input_csv_file = 'words.csv'  # Update this path as necessary

# Initialize a list to hold the translated words
translated_words = []

# Read the CSV file
with open(input_csv_file, mode='r', encoding='latin1') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if len(row) == 2:  # Ensure there are exactly two elements in the row
            english, spanish = row
            translated_words.append({"english": english, "spanish": spanish})

# Format the output as required
output = {"words": translated_words}

# Save the output to a JSON file with UTF-8 encoding
output_file = 'translated_words.json'  # Update this path as necessary
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(output, file, ensure_ascii=False, indent=2)

print(f'Translated words have been saved to {output_file}')
