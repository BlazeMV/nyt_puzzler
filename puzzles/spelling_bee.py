from flask import Blueprint, render_template, request

spelling_bee_bp = Blueprint('spelling_bee', __name__)

# Load a word list (ensure you have a valid word list file)
with open('wordlist.txt', 'r') as file:
    word_list = set(word.strip().lower() for word in file.readlines())


def solve_spelling_bee(input_letters, word_list):
    # Extract the required first letter
    required_letter = input_letters[0]

    # Create a set of allowed letters
    allowed_letters = set(input_letters)

    # Filter words that meet the criteria
    valid_words = []
    for word in word_list:
        # Check if the word contains the required letter
        if required_letter not in word:
            continue

        # Check if all letters in the word are in the allowed letters
        if all(letter in allowed_letters for letter in word):
            valid_words.append(word)

    # Sort the valid words by length in descending order
    valid_words.sort(key=lambda x: len(x), reverse=True)

    # Return the top 10 longest words
    return valid_words[:10]

@spelling_bee_bp.route('/spelling-bee', methods=['GET', 'POST'])
def letter_boxed():
    if request.method == 'POST':
        # Get the input from the form
        input_letters = [request.form[f'letter{i}'].strip().lower() for i in range(1, 8)]
        # Solve the puzzle and get all solutions
        solutions = solve_spelling_bee(input_letters, word_list)
        # Pass the input values and solutions back to the template
        return render_template(
            'spelling_bee.html',
            solutions=solutions,
            letters=[None]+[request.form[f'letter{i}'].strip().lower() for i in range(1, 8)],
        )
    return render_template('spelling_bee.html', solutions=None, letters=[None, "", "", "", "", "", "", ""])