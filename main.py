from flask import Flask, render_template
from puzzles.letter_boxed import letter_boxed_bp

app = Flask(__name__)

# Register blueprints for each puzzle
app.register_blueprint(letter_boxed_bp)

@app.route('/')
def home():
    return render_template('home.html')  # Render the home-specific template

if __name__ == '__main__':
    app.run(debug=True, port=3000)