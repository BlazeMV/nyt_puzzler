from flask import Flask, render_template, request
from itertools import permutations, product

app = Flask(__name__)

# Load a word list (ensure you have a valid word list file)
with open('wordlist.txt', 'r') as file:
    word_list = set(word.strip().lower() for word in file.readlines())


def is_valid_word(word, sides):
    """Check if a word is valid for the given sides."""
    for i in range(len(word) - 1):
        current_letter = word[i]
        next_letter = word[i + 1]
        # Check if consecutive letters are from the same side
        if any(current_letter in side and next_letter in side for side in sides):
            return False
    return True


def solve_letter_boxed(sides, word_list):
    """Solve the Letter Boxed puzzle."""
    all_letters = set(letter for side in sides for letter in side)
    valid_words = [word for word in word_list if
                   len(word) >= 3 and set(word).issubset(all_letters) and is_valid_word(word, sides)]

    # Try to find a sequence of words that uses all letters
    for word in valid_words:
        used_letters = set(word)
        print(all_letters)
        if used_letters == all_letters:
            return [word]
        remaining_letters = all_letters - used_letters
        # Recursively find the next word
        for next_word in valid_words:
            if next_word[0] == word[-1] and set(next_word).issubset(remaining_letters):
                result = solve_letter_boxed(sides, word_list)
                if result:
                    return [word] + result
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input from the form
        sides = [
            request.form['side1'].strip().lower().split(),
            request.form['side2'].strip().lower().split(),
            request.form['side3'].strip().lower().split(),
            request.form['side4'].strip().lower().split()
        ]
        # Solve the puzzle
        solution = solve_letter_boxed(sides, word_list)
        # Pass the input values and solution back to the template
        return render_template(
            'index.html',
            solution=" -> ".join(solution) if solution else "No solution found.",
            side1=" ".join(sides[0]),
            side2=" ".join(sides[1]),
            side3=" ".join(sides[2]),
            side4=" ".join(sides[3])
        )
    return render_template('index.html', solution=None, side1="", side2="", side3="", side4="")


if __name__ == '__main__':
    app.run(debug=True)