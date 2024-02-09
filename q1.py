import os
import re
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download stopwords 
nltk.download('stopwords')
nltk.download('punkt')
def preprocess_text(text):
    soup=BeautifulSoup(text, 'html.parser')
    text=soup.get_text()
    
    # Lowercase
    text=text.lower()
    
    # Tokenize
    tokens= word_tokenize(text)
    # Remove stopwords
    stop_words= set(stopwords.words('english'))
    tokens =[token for token in tokens if token not in stop_words]
    
    # Remove punctuations
    tokens=[re.sub(r'[^\w\s]', '', token) for token in tokens]
    # Remove blank space tokens
    tokens=[token for token in tokens if token.strip() != '']
    return tokens

# Function to print file contents before and after preprocessing
def print_before_and_after(file_path, preprocessed_text):
    print("File:", file_path)
    print("Before preprocessing:")
    with open(file_path, 'r',encoding='utf-8') as file:
        print(file.read())
    print("\nAfter preprocessing:")
    print(preprocessed_text)
    print("\n"+ "="*50 +"\n")

# Preprocess files
dataset_path = "./dataset"  
sample_files = [f for f in os.listdir(dataset_path) if f.endswith(".txt")][:990]

for filename in sample_files:
    file_path = os.path.join(dataset_path, filename)
    with open(file_path,'r',encoding='utf-8') as file:
        text = file.read()
        preprocessed_text = preprocess_text(text)
        print_before_and_after(file_path, preprocessed_text)
        # print above

    # Save preprocessed text
    preprocessed_file_path= os.path.join(dataset_path, filename.split(".")[0] + "_preprocessed.txt")
    with open(preprocessed_file_path, 'w',encoding='utf-8') as preprocessed_file:
        preprocessed_file.write(" ".join(preprocessed_text))

    print(f"Preprocessed text saved to: {preprocessed_file_path}\n")