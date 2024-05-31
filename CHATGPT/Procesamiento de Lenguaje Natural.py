from transformers import pipeline
nlp = pipeline("text-generation", model="gpt-3")

def complete_sentence(text):
    result = nlp(text, max_length=50)
    return result[0]['generated_text']

# Ejemplo de uso:
incomplete_text = "Hola, me llamo Juan y"
complete_text = complete_sentence(incomplete_text)
print(complete_text)
