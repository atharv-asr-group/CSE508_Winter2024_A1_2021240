import os
import re
import pickle
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')
nltk.download('punkt')
# Function to preprocess text
def preprocess_text(text):
    soup =BeautifulSoup(text, 'html.parser')
    text= soup.get_text()
    
    # Lowercase
    text=text.lower()
    
    # Tokenize
    tokens=word_tokenize(text)
    # Remove stopwords
    stop_words=set(stopwords.words('english'))
    tokens=[token for token in tokens if token not in stop_words]
    
    # Remove punctuations
    tokens=[re.sub(r'[^\w\s]', '', token) for token in tokens]
    # Remove blank space tokens
    tokens=[token for token in tokens if token.strip() != '']
    return tokens

# create unigram inverted index
import re
def create_inverted_index(dataset_path):
    inverted_index={}

    for filename in os.listdir(dataset_path):
        if filename.endswith("_preprocessed.txt"):
            # get file number from filename
            match=re.match(r'file(\d+)_preprocessed.txt', filename)
            if match:
                document_id=int(match.group(1))
            else:
                continue  # Skip file as file is not preprocessed file
            
            file_path=os.path.join(dataset_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                tokens=file.read().split()
                for token in tokens:
                    if token not in inverted_index:
                        inverted_index[token]={document_id}
                    else:
                        inverted_index[token].add(document_id)
    print(inverted_index)
    return inverted_index
# perform AND operation
def perform_AND(op1, op2):
    return op1.intersection(op2)

# perform OR operation
def perform_OR(op1, op2):
    return op1.union(op2)

# perform AND_NOT operation
def perform_AND_NOT(op1, op2):
    return op1.difference(op2)

# perform OR_NOT operation
def perform_OR_NOT(op1, op2, total_docs):
    not_op2 = set(range(1, total_docs+1)).difference(op2)
    return op1.union(not_op2)

# Function to execute a query
def execute_query(query, inverted_index, total_docs):
    print(query)
    print('*********')
    query_terms = preprocess_text(query[0])
    operations = query[1].split(', ')
    
    # Init result set with documents having first term
    result=inverted_index.get(query_terms[0], set())
    # print(result)
    # print('result print')
    # Iterate over query terms and operations
    for i in range(1, len(query_terms)):
        term = query_terms[i]
        if term in inverted_index:
            if operations[i - 1] == "AND":
                # print('from and')
                result = perform_AND(result, inverted_index[term])
            elif operations[i - 1] == "OR":
                # print('from or')
                # print(inverted_index[term])
                result = perform_OR(result, inverted_index[term])
            elif operations[i - 1] == "AND NOT":
                result = perform_AND_NOT(result, inverted_index[term])
            elif operations[i - 1] == "OR NOT":
                result = perform_OR_NOT(result, inverted_index[term], total_docs)
    return result
# save inverted index using pickle
def save_inverted_index(inverted_index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(inverted_index, file)

# load inverted index using pickle
def load_inverted_index(filename):
    with open(filename, 'rb') as file:
        inverted_index = pickle.load(file)
    print(inverted_index)
    return inverted_index

# main
def main():
    # Create unigram inverted index
    dataset_path="./dataset"
    inverted_index=create_inverted_index(dataset_path)
    total_docs=len(os.listdir(dataset_path)) // 2

    # input queries
    N=int(input())
    queries=[]
    for _ in range(N):
        query_sequence_raw = input()
        query_sequence=preprocess_text(query_sequence_raw)
        query_sequence_final=' '.join(query_sequence)
        operations = input()
        queries.append((query_sequence_final, operations))
        # outputquery=query_sequence_final.split()
        # operate=operations.split(', ')
        # printquery=' '.join([f'{term} {op}' if i < len(operate) else term for i, (term, op) in enumerate(zip(outputquery, operate))])
        # print(printquery)
    print(queries)

    # execute queries and print results
        
    for i, query in enumerate(queries, start=1):
        # print(query)
        # print('-+-+-+-')
        result=execute_query(query, inverted_index, total_docs)
        print(f"Query {i}: {query[0]}")
        print(f"Number of documents retrieved for query {i}: {len(result)}")
        print(f"Names of the documents retrieved for query {i}: {' '.join([f'file{doc}.txt' for doc in result])}\n")

if __name__ == "__main__":
    main()
