import re

def clean_text(text):
    # Remove special characters and digits
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize the text by splitting on whitespace
    tokens = text.split()
    
    # Remove single character tokens
    tokens = [word for word in tokens if len(word) > 1]
    
    return ' '.join(tokens)

# Example usage
with open("extracted_text.txt", "r", encoding="utf-8") as file:
    text = file.read()

cleaned_text = clean_text(text)
with open("cleaned_data.txt", "w", encoding="utf-8") as text_file:
    text_file.write(cleaned_text)