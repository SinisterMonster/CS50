# Get text and convert to lowercase
text = input("Text: ").lower()

# Finding word count
word_count = len(text.split())

# Fiding letter and sentence count
letter_count = 0
count = 0
sentence_count = 0

for i in text:
    if i.isalpha():
        letter_count += 1
    if i in ['?', '.', '!']:
        sentence_count += 1

# Calculating grade
L = letter_count*100 / word_count
S = sentence_count*100 / word_count

grade = round((0.0588 * L) - (0.296 * S) - 15.8)

# Print grade
if (grade >= 16):
    print(f"Grade 16+")
elif (grade < 1):
    print(f"Before Grade 1")
else:
    print(f"Grade: {grade}")
