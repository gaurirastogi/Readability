import re

# This program calculates the flesch-kincaid reading ease and grade level for a given input text without any libraries

num_sentences = 0
num_syllables = 0
num_words = 0
words_per_sentence = 0
syll_per_word = 0

def count_syllables(word):
    """
    Count the number of syllables in a word.
    """
    word = word.lower()
    vowels = "aeiouy"
    num_syllables = 0   
    prev_char = ""
    
    if len(word) == 0:
        return 0

    if word[0] in vowels:
        num_syllables += 1

    # Iterate through each character in the word
    
    for char in word:
        # If the character is a vowel and the previous character was not a vowel, count it as a syllable
        if char in vowels and prev_char not in vowels:
                num_syllables += 1
        prev_char = char


    # Adjust for silent 'e' at the end of words
    
    if word.endswith("e") and len(word) > 1 and word[-2] not in vowels:
        num_syllables -= 1
     
         
    # Ensure at least one syllable
    if num_syllables == 0:
        num_syllables += 1
    
    return num_syllables

def flesch_kincaid(text):
    """
    Calculate the Flesch Reading Ease and Flesch-Kincaid Grade Level scores for a given text.
    """

    global num_sentences
    global num_words
    global num_syllables
    global words_per_sentence
    global syll_per_word

    # Split text into sentences based on periods
    sentences = re.split(r'.[!?]', text)
    # Remove empty sentences
    sentences = [sentence for sentence in sentences if sentence]
    
    # Split text into words
    words = text.split()
    # Remove punctuation from words
    words = [word.strip(".,!?;:()[]") for word in words]
    
    # Calculate the total number of syllables in the text
    syllables = sum(count_syllables(word) for word in words)

    # Number of sentences
    num_sentences = len(sentences)
    # Number of words
    num_words = len(words)
    # Number of syllables
    num_syllables = syllables

    words_per_sentence = num_words / num_sentences
    syll_per_word = num_syllables / num_words
    syll_per_word = round (syll_per_word, 1)
    
    # Avoid division by zero
    if num_sentences == 0 or num_words == 0:
        return 0, 0

    # Calculate Flesch Reading Ease score
    flesch_reading_ease = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)

    # Calculate Flesch-Kincaid Grade Level
    flesch_kincaid_grade = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59


    return round(flesch_reading_ease, 2), round(flesch_kincaid_grade,1)

# Example usage
def evaluate_question_readability(question):
    """
    Evaluate the readability of a given question using the Flesch-Kincaid scale.
    """
    # Calculate Flesch Reading Ease and Flesch-Kincaid Grade Level scores
    flesch_reading_ease, flesch_kincaid_grade = flesch_kincaid(question)
    

    return (f"Flesch-Kincaid Grade Level: {flesch_kincaid_grade}\n"
            f"Flesch Reading Ease: {flesch_reading_ease}\n"
            f"Number of Sentences: {num_sentences}\n"
            f"Number of Words: {num_words}\n"
            f"Number of Syllables: {num_syllables}\n"
            f"Average Number of Words per Sentence: {words_per_sentence}\n"
            f"Average Number of Syllables per word: {syll_per_word}\n")



# Evaluate the readability of all questions in a file

def process_file(file_path, output_file_path):
    """
    process a file contiaining sample questions one line at a time"
    """

    with open(file_path, 'r') as file, open(output_file_path, 'w') as output_file:
        for line in file:
            question = line.strip()
            if question:
                output_file.write(f"Evaluating: {question}\n")
                result = evaluate_question_readability(question)
                output_file.write(result)
                output_file.write('\n')


file_path = 'cc/sample_questions.txt'
output_file_path = 'cc/valuation_output.txt'
process_file(file_path, output_file_path)



