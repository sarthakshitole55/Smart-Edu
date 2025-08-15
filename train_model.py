from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Set the padding token if it's not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained('gpt2')

# Load and preprocess the dataset
with open('cleaned_data.txt', 'r', encoding="utf-8") as file:
    text = file.read()

# Ensure the text is a single string
if not isinstance(text, str):
    raise ValueError("The loaded text is not a string.")

# Split the text into smaller chunks if necessary
def chunk_text(text, chunk_size=512):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

chunks = list(chunk_text(text))

# Tokenize each chunk and create a dataset
input_ids = []
attention_masks = []
labels = []

for chunk in chunks:
    encoded_dict = tokenizer(
        chunk,
        max_length=1000,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids.append(encoded_dict['input_ids'])
    attention_masks.append(encoded_dict['attention_mask'])
    labels.append(encoded_dict['input_ids'])  # Use input_ids as labels for language modeling

# Convert lists to tensors
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
labels = torch.cat(labels, dim=0)

# Create a dataset
dataset = Dataset.from_dict({'input_ids': input_ids, 'attention_mask': attention_masks, 'labels': labels})

# Split dataset into training and validation sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
    evaluation_strategy='epoch',  # Add evaluation strategy
    logging_steps=500,  # Add logging steps
    report_to='none'    # Disable reporting to avoid unnecessary output
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset  # Add validation dataset
)

# Train the model
trainer.train()

# Evaluate the model
eval_results = trainer.evaluate()
print(f"Evaluation results: {eval_results}")

# Save the trained model and tokenizer
model.save_pretrained('./trained_model')
tokenizer.save_pretrained('./trained_model')