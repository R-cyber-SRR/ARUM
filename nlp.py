from utils.transformers import pipeline

def generate_text(prompt):
    nlp = pipeline("text-generation")
    response = nlp(prompt, max_length=50)
    return response[0]['generated_text']
