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


def solve_letter_boxed(sides, word_list, excepted_words):
    """Solve the Letter Boxed puzzle and return all solutions with 7 words or less."""
    all_letters = set(letter for side in sides for letter in side)
    valid_words = [word for word in word_list if
                   len(word) >= 3 and set(word).issubset(all_letters) and is_valid_word(word, sides) and
                   word not in excepted_words]

    solutions = []

    def backtrack(sequence, remaining_letters, word_limit):
        """If 10 solutions are found, stop the backtracking."""
        if len(solutions) >= 10:
            return
        """Recursive backtracking to find all valid sequences of words."""
        if len(sequence) > word_limit:  # Stop if the sequence exceeds 7 words
            return
        if not remaining_letters:
            solutions.append(sequence.copy())  # Add the solution to the list
            return
        last_letter = sequence[-1][-1] if sequence else None
        for word in valid_words:
            if (not sequence or word[0] == last_letter) and set(word).intersection(remaining_letters):
                sequence.append(word)
                backtrack(sequence, remaining_letters - set(word), word_limit)
                sequence.pop()  # Backtrack

    """keep calling backtrack with increasing word limit (wl) until 10 solutions is found or wl exceeds 7."""
    wl = 2
    while len(solutions) < 10 and wl <= 7:
        backtrack([], all_letters, wl)
        wl += 1

    return solutions


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input from the form
        sides = [
            [request.form[f'side1-{i}'].strip().lower() for i in range(1, 4)],  # Top
            [request.form[f'side2-{i}'].strip().lower() for i in range(1, 4)],  # Right
            [request.form[f'side3-{i}'].strip().lower() for i in range(1, 4)],  # Bottom
            [request.form[f'side4-{i}'].strip().lower() for i in range(1, 4)]  # Left
        ]
        # Get the excepted words strip and convert to lowercase
        excepted_words = [word.strip().lower() for word in request.form['excepted_words'].split() if word and len(word.strip()) >= 3]
        print(excepted_words)
        # Solve the puzzle and get all solutions
        solutions = solve_letter_boxed(sides, word_list, excepted_words)
        # Sort solutions by the number of words used (ascending order)
        solutions.sort(key=lambda x: len(x))
        # Pass the input values and solutions back to the template
        return render_template(
            'index.html',
            solutions=solutions,
            side1=[request.form[f'side1-{i}'].strip().lower() for i in range(1, 4)],
            side2=[request.form[f'side2-{i}'].strip().lower() for i in range(1, 4)],
            side3=[request.form[f'side3-{i}'].strip().lower() for i in range(1, 4)],
            side4=[request.form[f'side4-{i}'].strip().lower() for i in range(1, 4)],
            excepted_words=request.form['excepted_words']
        )
    return render_template('index.html', solutions=None, side1=["", "", ""], side2=["", "", ""], side3=["", "", ""],
                           side4=["", "", ""], excepted_words="")


if __name__ == '__main__':
    app.run(debug=True, port=3000)