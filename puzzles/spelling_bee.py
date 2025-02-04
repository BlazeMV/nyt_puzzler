from flask import Blueprint, render_template, request

spelling_bee_bp = Blueprint('spelling_bee', __name__)

# Load a word list (ensure you have a valid word list file)
with open('wordlist.txt', 'r') as file:
    word_list = set(word.strip().lower() for word in file.readlines())

@spelling_bee_bp.route('/spelling-bee', methods=['GET', 'POST'])
def letter_boxed():
    if request.method == 'POST':
        # Solve the puzzle and get all solutions
        solutions = None
        # Pass the input values and solutions back to the template
        return render_template(
            'spelling_bee.html',
            solutions=solutions,
            letters=[request.form[f'side1-{i}'].strip().lower() for i in range(1, 4)],
        )
    return render_template('spelling_bee.html', solutions=None, letters=["", "", ""])