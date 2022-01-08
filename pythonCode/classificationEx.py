from keras.datasets import imdb

# Load the data, keeping only 10,000 of the most frequently occuring words
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words = 10000)


word_index = imdb.get_word_index()

for key, value in word_index.items():
    if 1 == value:
        print (key)