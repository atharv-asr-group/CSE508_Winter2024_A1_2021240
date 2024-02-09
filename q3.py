import os
import pickle
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download stopwords 
nltk.download('stopwords')
nltk.download('punkt')
# preprocess text
def preprocess_text(text):
    soup =BeautifulSoup(text, 'html.parser')
    text= soup.get_text()
    # Lowercase 
    text =text.lower()
    
    # Tokenize the text
    tokens=word_tokenize(text)
    # Remove stopwords
    stop_words=set(stopwords.words('english'))
    tokens=[token for token in tokens if token not in stop_words]
    # Remove punctuations
    tokens=[re.sub(r'[^\w\s]', '', token) for token in tokens]
    # Remove blank space tokens
    tokens=[token for token in tokens if token.strip() != '']
    return tokens

# create a positional index
def create_positional_index(dataset_path):
    positional_index = {}

    for filename in os.listdir(dataset_path):
        if filename.endswith("_preprocessed.txt"):
            # Extract document ID from filename
            match=re.match(r'file(\d+)_preprocessed.txt', filename)
            if match:
                document_id=int(match.group(1))
            else:
                continue  # Skip this file as not preprocessed
            
            file_path = os.path.join(dataset_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                tokens = file.read().split()
                for position, token in enumerate(tokens):
                    if token not in positional_index:
                        positional_index[token] = {document_id: [position]}
                    else:
                        if document_id not in positional_index[token]:
                            positional_index[token][document_id] = [position]
                        else:
                            positional_index[token][document_id].append(position)
    return positional_index


# save positional index to a file using pickle
def save_positional_index(positional_index, filename):
    print(positional_index)
    with open(filename, 'wb') as file:
        pickle.dump(positional_index, file)

# load positional index from a file using pickle
def load_positional_index(filename):
    with open(filename, 'rb') as file:
        positional_index=pickle.load(file)
    return positional_index

# main
def main():
    # Create positional index
    dataset_path="./dataset"
    positional_index=create_positional_index(dataset_path)

    # Save positional index using pickle
    save_filename="positional_index.pkl"
    save_positional_index(positional_index, save_filename)

    # Load positional index
    loaded_positional_index=load_positional_index(save_filename)

    # Read input queries
    N=int(input("Enter the number of queries: "))
    queries=[]
    for _ in range(N):
        query=input()
        queries.append(query)
    # Execute queries and print results
    for i, query in enumerate(queries, start=1):
        result = execute_query(query, loaded_positional_index)
        print(f"Number of documents retrieved for query {i} using positional index: {len(result)}")
        print(f"Names of documents retrieved for query {i} using positional index: {' '.join([f'file{doc}.txt' for doc in result])}")
# execute a phrase query
def execute_query(query, positional_index):
    query_terms=preprocess_text(query)
    result_docs=set()

    # Init result with the first term
    if query_terms[0] in positional_index:
        result_docs=set(positional_index[query_terms[0]].keys())
    # Iterate over the query terms
    for term in query_terms[1:]:
        if term in positional_index:
            result_docs=result_docs.intersection(positional_index[term].keys())
    # Check if the phrase exists
    for doc_id in result_docs:
        positions=[]
        for term in query_terms:
            # print(positional_index[term][doc_id])
            positions.append(positional_index[term][doc_id])
        for i in range(len(positions[0])):
            start_pos=positions[0][i]
            for j in range(1, len(positions)):
                if start_pos + j not in positions[j]:
                    break
            else:
                return result_docs
    return set()

if __name__ == "__main__":
    main()
