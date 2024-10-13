from transformers import BertTokenizer, BertForQuestionAnswering

# Download model and tokenizer online
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# Save the tokenizer and model to a local directory
tokenizer.save_pretrained('./bert-base-uncased/')
model.save_pretrained('./bert-base-uncased/')
