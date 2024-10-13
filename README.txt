pip install SpeechRecognition pocketsphinx nltk transformers torch

from transformers import BertTokenizer, BertForQuestionAnswering

# Download model and tokenizer online
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# Save the tokenizer and model to a local directory
tokenizer.save_pretrained('./bert-base-uncased/')
model.save_pretrained('./bert-base-uncased/')

import nltk

# Ensure NLTK tokenizer resources are available
nltk.download('punkt')
nltk.download('stopwords')

output:
Recognizing...
Recognized Text: Paris is the capital of France.
Processed Text: ['Paris', 'capital', 'France', '.']
Assistant Answer: paris is the capital of france
