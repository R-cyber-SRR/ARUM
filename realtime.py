from flask import request
from ai.nlp import generate_text  # Import the generate_text function

def process_input():
    user_input = request.form.get('input_text')
    if user_input:  # Check if user_input is not None or empty
        return generate_text(user_input)
    else:
        return "No input provided", 400  # Handle case where no input is received

