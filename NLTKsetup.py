import nltk
from nltk.corpus import stopwords  # Make sure to import stopwords

# Download necessary resources
nltk.download('punkt')  # For tokenization
nltk.download('stopwords')  # For stopwords
nltk.download('punkt_tab')
print(nltk.data.path)



# Check punkt tokenizer
try:
    punkt = nltk.data.load('tokenizers/punkt/english.pickle')
    print("Punkt tokenizer is available.")
except LookupError:
    print("Punkt tokenizer is not found. Please download it.")

# Check stopwords for English
try:
    stop_words = stopwords.words('english')
    print("English stopwords are available.")
except LookupError:
    print("English stopwords are not found. Please download them.")

# Check stopwords for Persian
# try:
#     persian_stopwords = stopwords.words('persian')
#     print("Persian stopwords are available.")
# except LookupError:
#     print("Persian stopwords are not found. Please download them.")