from flask import Flask, render_template, request

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

    def backtrack(sequence, remaining_letters):
        """Recursive backtracking to find a valid sequence of words."""
        if not remaining_letters:
            return sequence  # All letters have been used
        last_letter = sequence[-1][-1] if sequence else None
        for word in valid_words:
            if (not sequence or word[0] == last_letter) and set(word).intersection(remaining_letters):
                result = backtrack(sequence + [word], remaining_letters - set(word))
                if result:
                    return result
        return None

    return backtrack([], all_letters)


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