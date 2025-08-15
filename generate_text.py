from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./trained_model')
tokenizer = GPT2Tokenizer.from_pretrained('./trained_model')

# Set the model to evaluation mode
model.eval()

# Function to generate text
def generate_text(input_text):
    # Replace this with your LLM's logic
    return f"Generated response for: {input_text}"
# Generate text
from transformers import pipeline

# Load your trained model
model_path = "trained_model"  # Path to your trained model directory
generator = pipeline('text-generation', model=model_path)

def generate_text(input_text):
    try:
        # Generate a response using the trained model
        result = generator(input_text, max_length=500, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Error generating text: {str(e)}"