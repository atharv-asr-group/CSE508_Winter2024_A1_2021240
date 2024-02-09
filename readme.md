q1.
first I have downloaded stopwords(words like is, the, in,a, etc).
then there is function to preprocess the data, it is straight forward as I have given the comments also.
Then there is function to print before and after text of the files, you can change the number of files you want to do this with in the dataset. 
at the end we use the preprocessed text of each file to save it to a new file ending with filename_preprocessed.


q2.
The preprocessed files generated in q1 are used here, here also we have the first function to preprocess the text input given in the command line, done in a similar way as in q1.
then we create the unigram inverted index of the text in preprocessed files given in question 1. The unigram index contain each word and each file/document they are present in stored in a dictionary format. 
Then there are functions that are performing the and, or, and not, or not operations on the sets containing the file numbers the input words are persent in. At the end the result set contain all the file name that pass the query.

q3.
similar to q2 I preprocess the text input, make positional index from the preprocessed file in q1. The result docs set contain the files that have the particular sentence in them, which is the displayed on command line.