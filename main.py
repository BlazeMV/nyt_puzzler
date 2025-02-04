from flask import Flask, render_template
from puzzles.letter_boxed import letter_boxed_bp
from puzzles.spelling_bee import spelling_bee_bp
import argparse

app = Flask(__name__)

# Register blueprints for each puzzle
app.register_blueprint(letter_boxed_bp)
app.register_blueprint(spelling_bee_bp)

@app.route('/')
def home():
    return render_template('home.html')  # Render the home-specific template

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask app on')
    parser.add_argument('--debug', action='store_true', help='Run Flask in debug mode')

    # Parse arguments
    args = parser.parse_args()

    # Run the app with the specified port and debug mode
    app.run(port=args.port, debug=args.debug)